import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { flaresService } from "@/services";
import { Card, TagChip, Avatar } from "@/components/shared/primitives";
import { Markdown } from "@/components/shared/Markdown";
import { PostComposer } from "@/components/shared/PostComposer/PostComposer";
import { BookmarkToggleButton } from "@/components/shared/BookmarkToggleButton";
import {
  Heart,
  MessageCircle,
  Send,
  Flame,
  Calendar,
  Clock,
  Edit,
  Trash,
  BookOpen,
} from "lucide-react";
import { useState, useCallback } from "react";
import { currentUser } from "@/mocks/seed";
import type { Flare } from "@/mocks/seed";
import { toast } from "sonner";
import { useToggleLike, useLikedFlares } from "@/hooks/useLike";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/_app/flares")({
  head: () => ({
    meta: [
      { title: "Flares — DevLink Community" },
      { name: "description", content: "Community feed of updates, tips and asks from builders." },
    ],
  }),
  component: FlaresPage,
});

function FlareCard({
  flare,
  isDraft = false,
  onEdit,
  onDelete,
  onPublish,
}: {
  flare: Flare;
  isDraft?: boolean;
  onEdit?: (flare: Flare) => void;
  onDelete?: (id: string) => void;
  onPublish?: (id: string) => void;
}) {
  const { data: likedMap } = useLikedFlares();
  const toggleLike = useToggleLike(flare.id);
  const isLiked = likedMap?.[flare.id] ?? false;

  return (
    <Card className={cn("p-4 transition-all", isDraft && "border-amber-500/10 hover:border-amber-500/20")}>
      <div className="flex items-start gap-3">
        <Avatar
          src={flare.author?.avatar}
          alt={flare.author?.name}
          size={40}
          online={flare.author?.online}
        />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <p className="text-[13px] font-semibold text-foreground">{flare.author?.name}</p>
              <p className="text-[12px] text-muted-foreground">
                @{flare.author?.handle}
                {flare.ago && ` · ${flare.ago}`}
              </p>
            </div>
            {isDraft && (
              <span
                className={cn(
                  "rounded-full px-2 py-0.5 text-[10px] font-semibold flex items-center gap-1",
                  flare.status === "scheduled"
                    ? "bg-amber-500/10 text-amber-500"
                    : "bg-muted text-muted-foreground",
                )}
              >
                {flare.status === "scheduled" ? (
                  <>
                    <Clock size={10} /> Scheduled
                  </>
                ) : (
                  "Draft"
                )}
              </span>
            )}
          </div>

          {flare.status === "scheduled" && flare.publish_at && (
            <p className="mt-1 text-[11px] text-amber-500/80 flex items-center gap-1 font-medium">
              <Calendar size={11} /> Will publish on: {new Date(flare.publish_at).toLocaleString()}
            </p>
          )}

          <div className="mt-2">
            <Markdown content={flare.content} />
          </div>

          <div className="mt-2 flex flex-wrap gap-1">
            {flare.tags?.map((t) => (
              <TagChip key={t}>#{t}</TagChip>
            ))}
          </div>

          <div className="mt-3 flex items-center justify-between gap-4 text-[12px] text-muted-foreground border-t border-border/40 pt-3">
            {!isDraft ? (
              <div className="flex items-center gap-4">
                <button
                  className={cn(
                    "inline-flex items-center gap-1 transition-colors",
                    isLiked ? "text-destructive" : "hover:text-destructive",
                  )}
                  onClick={() => toggleLike.mutate()}
                  disabled={toggleLike.isPending}
                  aria-label={isLiked ? "Unlike this flare" : "Like this flare"}
                  aria-pressed={isLiked}
                >
                  <Heart size={12} className={isLiked ? "fill-current" : ""} /> {flare.likes}
                </button>
                <button className="inline-flex items-center gap-1 hover:text-primary">
                  <MessageCircle size={12} /> {flare.comments}
                </button>
                <BookmarkToggleButton targetType="flare" targetId={flare.id} />
              </div>
            ) : (
              <div className="flex items-center justify-between w-full">
                <button
                  onClick={() => onPublish?.(flare.id)}
                  className="text-[11px] font-semibold text-primary hover:underline flex items-center gap-1"
                >
                  <Send size={11} /> Publish Now
                </button>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onEdit?.(flare)}
                    className="p-1 hover:bg-muted rounded text-muted-foreground hover:text-foreground transition-colors"
                    title="Edit Draft"
                  >
                    <Edit size={12} />
                  </button>
                  <button
                    onClick={() => onDelete?.(flare.id)}
                    className="p-1 hover:bg-destructive-soft rounded text-muted-foreground hover:text-destructive transition-colors"
                    title="Delete Draft"
                  >
                    <Trash size={12} />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
}

function FlaresPage() {
  const { data = [] } = useQuery({ queryKey: ["flares"], queryFn: flaresService.list });
  const [localFlares, setLocalFlares] = useState<Flare[]>([]);
  const { data: feedPosts = [], refetch: refetchFeed } = useQuery({
    queryKey: ["flares"],
    queryFn: flaresService.list,
  });

  const { data: draftPosts = [], refetch: refetchDrafts } = useQuery({
    queryKey: ["flares-drafts"],
    queryFn: flaresService.drafts,
  });

  const [activeTab, setActiveTab] = useState<"feed" | "drafts">("feed");
  const [content, setContent] = useState("");
  const [isScheduling, setIsScheduling] = useState(false);
  const [publishAt, setPublishAt] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Edit draft states
  const [editingPost, setEditingPost] = useState<Flare | null>(null);
  const [editContent, setEditContent] = useState("");

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_280px]">
      <div className="space-y-4">
        <PostComposer
          placeholder="Share an update, a tip, or ask the community…"
          onPost={async (content, attachments) => {
            try {
              await new Promise((r) => setTimeout(r, 600));
              const newFlare: Flare = {
                id: `local-${Date.now()}`,
                author: {
                  ...builders[0],
                  name: currentUser.name,
                  handle: currentUser.handle,
                  avatar: currentUser.avatar,
                },
                content: content || (attachments.length > 0 ? `Shared ${attachments.length} attachment(s)` : ""),
                tags: Array.from(new Set(content.match(/#(\w+)/g)?.map((t) => t.slice(1)) ?? [])),
                likes: 0,
                comments: 0,
                ago: "just now",
              };
              setLocalFlares((prev) => [newFlare, ...prev]);
              toast.success("Flare posted");
            } catch (e) {
              console.error(e);
            }
          }}
        />
        {feed.map((f) => (
          <FlareCard key={f.id} flare={f} />
        ))}
  const handlePost = async (status: "published" | "draft") => {
    if (!content.trim() || submitting) return;
    setSubmitting(true);
    try {
      const tags = Array.from(new Set(content.match(/#(\w+)/g)?.map((t) => t.slice(1)) ?? []));
      await flaresService.create({
        content,
        tags,
        status: isScheduling ? "scheduled" : status,
        publish_at: isScheduling && publishAt ? publishAt : undefined,
      });

      toast.success(
        isScheduling
          ? "Flare scheduled successfully"
          : status === "draft"
            ? "Saved as draft"
            : "Flare posted",
      );
      setContent("");
      setIsScheduling(false);
      setPublishAt("");
      refetchFeed();
      refetchDrafts();
    } catch (err: any) {
      toast.error(err.message || "Failed to create flare");
    } finally {
      setSubmitting(false);
    }
  };

  const handlePublishNow = async (id: string) => {
    try {
      await flaresService.update(id, { status: "published", publish_at: undefined });
      toast.success("Flare published successfully");
      refetchFeed();
      refetchDrafts();
    } catch (err: any) {
      toast.error("Failed to publish draft");
    }
  };

  const handleDeleteDraft = async (id: string) => {
    try {
      await flaresService.remove(id);
      toast.success("Draft deleted");
      refetchFeed();
      refetchDrafts();
    } catch (err: any) {
      toast.error("Failed to delete draft");
    }
  };

  const startEditDraft = (flare: Flare) => {
    setEditingPost(flare);
    setEditContent(flare.content);
  };

  const handleSaveEdit = async () => {
    if (!editingPost || !editContent.trim()) return;
    try {
      const tags = Array.from(new Set(editContent.match(/#(\w+)/g)?.map((t) => t.slice(1)) ?? []));
      await flaresService.update(editingPost.id, {
        content: editContent,
        tags,
      });
      toast.success("Draft updated");
      setEditingPost(null);
      refetchDrafts();
    } catch (err: any) {
      toast.error("Failed to update draft");
    }
  };

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_280px]">
      <div className="space-y-4">
        {/* Compose Card */}
        <Card className="p-4 border-primary/10 bg-gradient-to-b from-card to-card/95 shadow-sm">
          <div className="flex items-start gap-3">
            <Avatar src={currentUser.avatar} alt={currentUser.name} size={40} />
            <div className="min-w-0 flex-1">
              <MarkdownEditor
                value={content}
                onChange={setContent}
                placeholder="Share an update, a tip, or ask the community…"
                rows={3}
              />
              <div className="mt-3 flex flex-wrap items-center justify-between gap-3 border-t border-border/40 pt-3">
                <div className="flex items-center gap-3">
                  <label className="inline-flex items-center gap-1.5 text-[11px] font-medium text-muted-foreground hover:text-foreground cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={isScheduling}
                      onChange={(e) => setIsScheduling(e.target.checked)}
                      className="rounded border-border bg-muted text-primary focus:ring-primary/20"
                    />
                    Publish later
                  </label>
                  {isScheduling && (
                    <input
                      type="datetime-local"
                      value={publishAt}
                      onChange={(e) => setPublishAt(e.target.value)}
                      className="rounded border border-border bg-surface px-2 py-1 text-[11px] text-foreground outline-none focus:border-primary"
                    />
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {!isScheduling && (
                    <button
                      disabled={!content.trim() || submitting}
                      onClick={() => handlePost("draft")}
                      className="rounded-md border border-border bg-surface px-3 py-1.5 text-[12px] font-semibold text-foreground hover:bg-muted transition-colors disabled:opacity-50"
                    >
                      Save Draft
                    </button>
                  )}
                  <LoadingButton
                    disabled={!content.trim() || (isScheduling && !publishAt) || submitting}
                    loading={submitting}
                    loadingText={isScheduling ? "Scheduling..." : "Posting..."}
                    onClick={() => handlePost("published")}
                    size="sm"
                    className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-1.5 text-[12px] font-semibold text-primary-foreground hover:opacity-90 disabled:opacity-50"
                  >
                    <Send size={12} /> {isScheduling ? "Schedule" : "Post"}
                  </LoadingButton>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Tab Navigation */}
        <div className="flex border-b border-border">
          <button
            onClick={() => setActiveTab("feed")}
            className={cn(
              "px-4 py-2 text-[13px] font-semibold border-b-2 transition-colors flex items-center gap-1.5",
              activeTab === "feed"
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground",
            )}
          >
            <BookOpen size={14} /> Community Feed
          </button>
          <button
            onClick={() => setActiveTab("drafts")}
            className={cn(
              "px-4 py-2 text-[13px] font-semibold border-b-2 transition-colors flex items-center gap-1.5",
              activeTab === "drafts"
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground",
            )}
          >
            <Clock size={14} /> My Drafts & Scheduled ({draftPosts.length})
          </button>
        </div>

        {/* Edit Draft Block */}
        {editingPost && (
          <Card className="p-4 border-amber-500/20 bg-amber-500/5">
            <p className="text-[12px] font-semibold text-amber-500 mb-2 flex items-center gap-1">
              <Edit size={12} /> Editing Draft
            </p>
            <MarkdownEditor value={editContent} onChange={setEditContent} rows={3} />
            <div className="mt-3 flex items-center justify-end gap-2">
              <button
                onClick={() => setEditingPost(null)}
                className="rounded-md border border-border bg-surface px-3 py-1.5 text-[11px] font-semibold text-foreground hover:bg-muted transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveEdit}
                disabled={!editContent.trim()}
                className="rounded-md bg-amber-500 px-3 py-1.5 text-[11px] font-semibold text-white hover:bg-amber-600 transition-colors disabled:opacity-50"
              >
                Save Draft
              </button>
            </div>
          </Card>
        )}

        {/* Feed Posts List */}
        {activeTab === "feed" ? (
          feedPosts.length > 0 ? (
            feedPosts.map((f) => <FlareCard key={f.id} flare={f} />)
          ) : (
            <p className="text-center py-8 text-xs text-muted-foreground">No feed posts found.</p>
          )
        ) : draftPosts.length > 0 ? (
          draftPosts.map((f) => (
            <FlareCard
              key={f.id}
              flare={f}
              isDraft
              onPublish={handlePublishNow}
              onDelete={handleDeleteDraft}
              onEdit={startEditDraft}
            />
          ))
        ) : (
          <p className="text-center py-8 text-xs text-muted-foreground">No drafts or scheduled posts found.</p>
        )}
      </div>

      <aside className="space-y-4">
        <Card className="p-4">
          <p className="flex items-center gap-1.5 text-[13px] font-semibold text-foreground">
            <Flame size={14} className="text-warning" /> Trending tags
          </p>
          <div className="mt-3 flex flex-wrap gap-1">
            {[
              "react",
              "typescript",
              "ml",
              "designsystems",
              "postgres",
              "webgpu",
              "wasm",
              "rust",
            ].map((t) => (
              <TagChip key={t}>#{t}</TagChip>
            ))}
          </div>
        </Card>
        <Card className="p-4">
          <p className="text-[13px] font-semibold text-foreground">Community guidelines</p>
          <p className="mt-2 text-[12px] text-muted-foreground">
            Be kind, credit sources, no spam. Ship generously.
          </p>
        </Card>
      </aside>
    </div>
  );
}
