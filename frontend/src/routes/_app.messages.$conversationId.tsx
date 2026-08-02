import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery, useMutation } from "@tanstack/react-query";
import { messagesService } from "@/services";
import { Card, Avatar, Skeleton } from "@/components/shared/primitives";
import { LoadingButton } from "@/components/shared/LoadingButton";
import { ArrowLeft, Send, Sparkles } from "lucide-react";
import { useState, useCallback, useEffect, useRef } from "react";
import { TypingIndicator } from "@/components/chat/TypingIndicator";
import { builders, conversations } from "@/mocks/seed";
import { cn } from "@/lib/utils";
import { conversationStartersApi, type ConversationStarterResponse } from "@/api";
import { useAuth } from "@/contexts/auth-context";
import { useChatWebSocket } from "@/hooks/useChatWebSocket";
import { useQueryClient } from "@tanstack/react-query";
export const Route = createFileRoute("/_app/messages/$conversationId")({
  head: () => ({ meta: [{ title: "Chat — DevLink" }] }),
  component: Thread,
});

function Thread() {
  const { conversationId } = Route.useParams();
  const existingConversation = conversations.find((c) => c.id === conversationId);
  const contact =
    existingConversation?.with ?? builders.find((builder) => builder.id === conversationId);
  const conv =
    existingConversation ?? (contact ? { id: conversationId, with: contact } : conversations[0]);
  const { data = [] } = useQuery({
    queryKey: ["thread", conversationId],
    queryFn: () => messagesService.thread(conversationId),
  });
  const [text, setText] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Conversation starters state
  const [starters, setStarters] = useState<ConversationStarterResponse | null>(null);
  const [startersError, setStartersError] = useState<string | null>(null);
  const conversationIdRef = useRef(conversationId);

  const startersMutation = useMutation({
    mutationFn: () => conversationStartersApi.generate(conversationId),
    onSuccess: (data) => {
      if (conversationIdRef.current !== conversationId) return;
      setStarters(data);
      setStartersError(null);
    },
    onError: (err) => {
      if (conversationIdRef.current !== conversationId) return;
      setStartersError(err instanceof Error ? err.message : "Failed to load suggestions");
    },
  });

  // Reset starters when switching conversations
  useEffect(() => {
    conversationIdRef.current = conversationId;
    setStarters(null);
    setStartersError(null);
  }, [conversationId]);
  const { user } = useAuth();
  const queryClient = useQueryClient();

  // Use the websocket hook for real-time messaging and typing
  const { isConnected, typingUsers, broadcastMessage, broadcastTyping } = useChatWebSocket(
    conversationId,
    user?.id || "",
    useCallback((msg: any) => {
      // Invalidate thread query when a new message arrives via WS
      queryClient.invalidateQueries({ queryKey: ["thread", conversationId] });
      // Invalidate conversations list to update latest preview/timestamp
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    }, [queryClient, conversationId])
  );

  const themTyping = typingUsers.length > 0;
  const lastTypingPingRef = useRef<number>(0);

  // Notify the server that the local user is typing. Debounced to once
  // per second so we don't hammer the endpoint. Failures are swallowed —
  // the typing indicator is a cosmetic enhancement and must never block
  // message sending.
  const notifyTyping = useCallback(() => {
    const now = Date.now();
    if (now - lastTypingPingRef.current < 1000) return;
    lastTypingPingRef.current = now;
    // Best-effort POST; the endpoint may not exist in every environment
    // (e.g. mock-only frontend builds). Swallow errors so the UI is
    // never broken by a missing/failed typing call.
    fetch(`/api/messages/conversation/${conversationId}/typing`, {
      method: "POST",
      credentials: "include",
    }).catch(() => {
      /* no-op: typing indicator is best-effort */
    });
  }, [conversationId]);

  const clearTyping = useCallback(() => {
    fetch(`/api/messages/conversation/${conversationId}/typing`, {
      method: "DELETE",
      credentials: "include",
    }).catch(() => {
      /* no-op */
    });
  }, [conversationId]);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setText(e.target.value);
      notifyTyping();
    },
    [notifyTyping],
  );

  // Clear typing on unmount.
  useEffect(() => {
    return () => {
      clearTyping();
    };
  }, [clearTyping]);

  const handleSend = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!text.trim() || submitting) return;
      setSubmitting(true);
      clearTyping();
      try {
        // Optimistic UI could be added here, but for simplicity we rely on React Query
        await messagesService.send(conversationId, text);
        setText("");
        // Notify others via WS
        broadcastMessage(text);
        
        // Invalidate queries to reload thread and conversations
        queryClient.invalidateQueries({ queryKey: ["thread", conversationId] });
        queryClient.invalidateQueries({ queryKey: ["conversations"] });
      } catch (err) {
        console.error("Failed to send message", err);
      } finally {
        setSubmitting(false);
      }
    },
    [text, submitting, clearTyping, conversationId, broadcastMessage, queryClient],
  );

  return (
    <div className="grid gap-4 lg:grid-cols-[320px_minmax(0,1fr)]">
      <Card className="hidden lg:block lg:h-[calc(100vh-8rem)] lg:overflow-y-auto">
        <div className="border-b border-border px-4 py-3">
          <p className="text-[14px] font-semibold text-foreground">Conversations</p>
        </div>
        <ul className="divide-y divide-border">
          {conversations.map((c) => (
            <li key={c.id}>
              <Link
                to="/messages/$conversationId"
                params={{ conversationId: c.id }}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 hover:bg-muted/50",
                  c.id === conversationId && "bg-muted/50",
                )}
              >
                <Avatar src={c.with.avatar} alt={c.with.name} size={36} online={c.with.online} />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-[13px] font-semibold text-foreground">
                    {c.with.name}
                  </p>
                  <p className="truncate text-[12px] text-muted-foreground">{c.preview}</p>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </Card>

      <Card className="flex flex-col lg:h-[calc(100vh-8rem)]">
        <div className="flex items-center gap-3 border-b border-border px-4 py-3">
          <Link to="/messages" className="lg:hidden">
            <ArrowLeft size={16} className="text-muted-foreground" />
          </Link>
          <Avatar src={conv.with.avatar} alt={conv.with.name} size={36} online={conv.with.online} />
          <div>
            <p className="text-[13px] font-semibold text-foreground">{conv.with.name}</p>
            <p className="text-[11px] text-muted-foreground">
              {conv.with.online ? "Online" : "Offline"}
            </p>
          </div>
        </div>

        <div className="flex-1 space-y-2 overflow-y-auto p-4">
          {data.length === 0 && (
            <div className="space-y-4">
              <p className="text-center text-[12px] text-muted-foreground">
                No messages yet — say hello 👋
              </p>

              {/* Conversation Starters Section */}
              {!starters && !startersMutation.isPending && !startersError && (
                <button
                  onClick={() => startersMutation.mutate()}
                  className="mx-auto flex items-center gap-2 rounded-md border border-border bg-surface px-4 py-2 text-[12px] text-muted-foreground hover:bg-muted/50 hover:text-foreground"
                >
                  <Sparkles size={14} />
                  Get conversation starters
                </button>
              )}

              {startersMutation.isPending && (
                <div className="space-y-2">
                  <Skeleton className="h-10 w-full" />
                  <Skeleton className="h-10 w-full" />
                  <Skeleton className="h-10 w-3/4" />
                </div>
              )}

              {startersError && (
                <div className="space-y-2">
                  <p className="text-center text-[12px] text-destructive">{startersError}</p>
                  <button
                    onClick={() => {
                      setStartersError(null);
                      startersMutation.mutate();
                    }}
                    className="mx-auto flex items-center gap-2 rounded-md border border-border bg-surface px-4 py-2 text-[12px] text-muted-foreground hover:bg-muted/50 hover:text-foreground"
                  >
                    <Sparkles size={14} />
                    Try again
                  </button>
                </div>
              )}

              {starters && (
                <div className="space-y-2">
                  <p className="text-center text-[11px] text-muted-foreground">
                    Suggestions for {starters.target_user_name}
                  </p>
                  {starters.suggestions.map((suggestion, i) => (
                    <button
                      key={i}
                      onClick={() => setText(suggestion.text)}
                      className="flex w-full items-center justify-between gap-2 rounded-md border border-border bg-surface px-3 py-2 text-left text-[13px] text-foreground hover:bg-muted/50"
                    >
                      <span>{suggestion.text}</span>
                      <span className="shrink-0 rounded-sm bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground">
                        {Math.round(suggestion.confidence * 100)}%
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
          {data.map((m) => (
            <div
              key={m.id}
              className={cn("flex", m.from === "me" ? "justify-end" : "justify-start")}
            >
              <div
                className={cn(
                  "max-w-[75%] rounded-md px-3 py-2 text-[13px]",
                  m.from === "me"
                    ? "bg-primary text-primary-foreground"
                    : "border border-border bg-surface text-foreground",
                )}
              >
                <p>{m.text}</p>
                <p
                  className={cn(
                    "mt-1 text-[10px]",
                    m.from === "me" ? "text-primary-foreground/70" : "text-muted-foreground",
                  )}
                >
                  {m.at}
                </p>
              </div>
            </div>
          ))}

          {/* Typing indicator — shown when the other participant is typing. */}
          {themTyping && (
            <div className="flex justify-start">
              <div className="max-w-[75%] rounded-md border border-border bg-surface px-3 py-2">
                <TypingIndicator />
              </div>
            </div>
          )}
        </div>

        {/* Inline typing label above the input for extra visibility. */}
        {themTyping && (
          <div className="px-4 pt-1">
            <TypingIndicator label={`${conv.with.name} is typing`} />
          </div>
        )}

        <form onSubmit={handleSend} className="flex items-center gap-2 border-t border-border p-3">
          <input
            value={text}
            onChange={handleInputChange}
            placeholder="Type a message…"
            className="min-w-0 flex-1 rounded-md border border-border bg-surface px-3 py-2 text-[13px] outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
          />
          <LoadingButton
            type="submit"
            loading={submitting}
            loadingText=""
            disabled={!text.trim()}
            className="inline-flex items-center gap-1"
          >
            <Send size={14} /> Send
          </LoadingButton>
        </form>
      </Card>
    </div>
  );
}
