import { useId, useRef, useState } from "react";
import { Eye, Pencil, Image as ImageIcon, Video, AtSign, Code2 } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Markdown } from "@/components/shared/Markdown";
import { cn } from "@/lib/utils";

export interface MarkdownEditorProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  rows?: number;
  className?: string;
  textareaClassName?: string;
  autoFocus?: boolean;
}

/**
 * Inserts `text` at the current cursor position (replacing any selection),
 * rather than always appending to the end. Returns the new full value and
 * the cursor offset where the caret should land afterward.
 */
function insertAtCursor(
  current: string,
  selectionStart: number,
  selectionEnd: number,
  insertion: string,
  cursorOffsetFromStart = insertion.length,
): { nextValue: string; nextCursor: number } {
  const before = current.slice(0, selectionStart);
  const after = current.slice(selectionEnd);
  const nextValue = `${before}${insertion}${after}`;
  const nextCursor = selectionStart + cursorOffsetFromStart;
  return { nextValue, nextCursor };
}

/**
 * Write / Preview markdown editor.
 * "Write" is a plain textarea with a lightweight formatting toolbar above it;
 * "Preview" renders the same content through the shared <Markdown> renderer
 * so contributors see exactly what will be published (GFM tables, code
 * blocks, images, lists, headers, etc).
 */
export function MarkdownEditor({
  value,
  onChange,
  placeholder = "Write some markdown…",
  rows = 4,
  className,
  textareaClassName,
  autoFocus,
}: MarkdownEditorProps) {
  const [tab, setTab] = useState<"write" | "preview">("write");
  const previewId = useId();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /**
   * Shared entry point for every toolbar button: reads the textarea's
   * current selection, inserts `insertion` there, updates the value via
   * onChange, then restores focus and places the caret at `cursorOffset`
   * (defaults to right after the inserted text).
   */
  const insertAtCursorInTextarea = (insertion: string, cursorOffset?: number) => {
    const textarea = textareaRef.current;
    if (!textarea) {
      // Fallback: no ref available yet, append to the end.
      onChange(`${value}${insertion}`);
      return;
    }

    const { selectionStart, selectionEnd } = textarea;
    const { nextValue, nextCursor } = insertAtCursor(
      value,
      selectionStart,
      selectionEnd,
      insertion,
      cursorOffset ?? insertion.length,
    );

    onChange(nextValue);

    // Restore focus + caret position after React re-renders the new value.
    requestAnimationFrame(() => {
      textarea.focus();
      textarea.setSelectionRange(nextCursor, nextCursor);
    });
  };

  const handleEmoji = () => insertAtCursorInTextarea("😀");

  const handleImage = () => {
    const snippet = "![Alt text](image-url)";
    // Place caret right after "![" so "Alt text" is easy to overtype.
    insertAtCursorInTextarea(snippet, 2);
  };

  const handleVideo = () => {
    const snippet = "[Watch Video](video-url)";
    // Cursor remains at the end of the inserted markdown.
    insertAtCursorInTextarea(snippet);
  };

  const handleMention = () => insertAtCursorInTextarea("@username");

  const handleCodeBlock = () => {
    const snippet = "```\n\n```";
    // Caret lands on the blank line between the two fences.
    insertAtCursorInTextarea(snippet, 4);
  };

  return (
    <div className={cn("w-full", className)}>
      <Tabs value={tab} onValueChange={(v) => setTab(v as "write" | "preview")}>
        <div className="flex items-center justify-between gap-2">
          <TabsList>
            <TabsTrigger value="write" className="gap-1.5">
              <Pencil size={12} /> Write
            </TabsTrigger>
            <TabsTrigger value="preview" className="gap-1.5">
              <Eye size={12} /> Preview
            </TabsTrigger>
          </TabsList>
          <p className="hidden text-[11px] text-muted-foreground sm:block">
            Markdown supported · **bold** _italic_ `code` [link](url)
          </p>
        </div>

        <TabsContent value="write" className="mt-2">
          {tab === "write" && (
            <div className="mb-1.5 flex items-center gap-1 rounded-md border border-border bg-surface p-1">
              <button
                type="button"
                onClick={handleEmoji}
                aria-label="Insert emoji"
                title="Emoji"
                className="inline-flex h-7 w-7 items-center justify-center rounded text-[14px] hover:bg-muted"
              >
                😀
              </button>
              <button
                type="button"
                onClick={handleImage}
                aria-label="Insert image"
                title="Image"
                className="inline-flex h-7 w-7 items-center justify-center rounded text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <ImageIcon size={14} />
              </button>
              <button
                type="button"
                onClick={handleVideo}
                aria-label="Insert video"
                title="Video"
                className="inline-flex h-7 w-7 items-center justify-center rounded text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <Video size={14} />
              </button>
              <button
                type="button"
                onClick={handleMention}
                aria-label="Insert mention"
                title="Mention"
                className="inline-flex h-7 w-7 items-center justify-center rounded text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <AtSign size={14} />
              </button>
              <button
                type="button"
                onClick={handleCodeBlock}
                aria-label="Insert code block"
                title="Code Block"
                className="inline-flex h-7 w-7 items-center justify-center rounded text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <Code2 size={14} />
              </button>
            </div>
          )}

          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            rows={rows}
            autoFocus={autoFocus}
            className={cn(
              "w-full resize-y rounded-md border border-border bg-surface p-3 font-mono text-[13px] leading-relaxed text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20",
              textareaClassName,
            )}
          />
        </TabsContent>

        <TabsContent value="preview" className="mt-2">
          <div
            id={previewId}
            className="rounded-md border border-dashed border-border bg-surface p-3"
            style={{ minHeight: `${rows * 1.6}em` }}
          >
            {value.trim() ? (
              <Markdown content={value} />
            ) : (
              <p className="text-[13px] text-muted-foreground">Nothing to preview yet.</p>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}