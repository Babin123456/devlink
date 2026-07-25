import { cn } from "@/lib/utils";
import { Link } from "@tanstack/react-router";
import type { ReactNode, ComponentType } from "react";
import { FolderKanban, BellOff, MessageSquareDashed, UserX, SearchX, Sparkles } from "lucide-react";

export function SectionHeader({
  title,
  action,
  actionTo,
  className,
}: {
  title: string;
  action?: string;
  actionTo?: string;
  className?: string;
}) {
  return (
    <div className={cn("flex items-center justify-between px-4 pt-4 pb-3", className)}>
      <h3 className="text-[14px] font-semibold text-foreground">{title}</h3>
      {action &&
        (actionTo ? (
          <Link to={actionTo} className="text-[12px] font-medium text-primary hover:underline">
            {action}
          </Link>
        ) : (
          <button className="text-[12px] font-medium text-primary hover:underline">{action}</button>
        ))}
    </div>
  );
}

export function Card({
  children,
  className,
  as: As = "div",
  interactive = false,
}: {
  children?: ReactNode;
  className?: string;
  as?: "div" | "article" | "section";
  interactive?: boolean;
}) {
  return (
    <As
      className={cn(
        "rounded-md border border-border bg-card shadow-soft",
        interactive && "transition-shadow hover:shadow-card",
        className,
      )}
    >
      {children}
    </As>
  );
}

export function EmptyState({
  icon: Icon = Sparkles,
  title,
  desc,
  action,
  className,
}: {
  icon?: ComponentType<{ className?: string }> | ReactNode;
  title: string;
  desc?: string;
  action?: ReactNode;
  className?: string;
}) {
  const isComponent =
    typeof Icon === "function" ||
    (typeof Icon === "object" && Icon !== null && "render" in (Icon as object));
  const IconComp = isComponent ? (Icon as ComponentType<{ className?: string }>) : null;

  return (
    <div
      className={cn("flex flex-col items-center justify-center py-12 px-4 text-center", className)}
    >
      <div className="relative mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-primary/20 bg-primary/10 text-primary shadow-sm transition-transform hover:scale-105">
        {IconComp ? (
          <IconComp className="h-7 w-7 text-primary" />
        ) : (
          <div className="text-2xl">{Icon as ReactNode}</div>
        )}
      </div>
      <h3 className="text-[15px] font-semibold tracking-tight text-foreground">{title}</h3>
      {desc && (
        <p className="mt-1.5 max-w-sm text-[13px] leading-relaxed text-muted-foreground">{desc}</p>
      )}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

export function NoProjectsEmptyState({
  title = "No projects found",
  desc = "There are no projects available right now. Create a new project to start collaborating!",
  action,
}: {
  title?: string;
  desc?: string;
  action?: ReactNode;
}) {
  return <EmptyState icon={FolderKanban} title={title} desc={desc} action={action} />;
}

export function NoNotificationsEmptyState({
  title = "No notifications yet",
  desc = "You're all caught up! Updates and notifications will appear here as they arrive.",
}: {
  title?: string;
  desc?: string;
}) {
  return <EmptyState icon={BellOff} title={title} desc={desc} />;
}

export function NoMessagesEmptyState({
  title = "No messages",
  desc = "Your inbox is empty. Connect with other developers or start a conversation from a profile.",
  action,
}: {
  title?: string;
  desc?: string;
  action?: ReactNode;
}) {
  return <EmptyState icon={MessageSquareDashed} title={title} desc={desc} action={action} />;
}

export function NoConnectionsEmptyState({
  title = "No connections found",
  desc = "We couldn't find any developers matching your filter criteria.",
  action,
}: {
  title?: string;
  desc?: string;
  action?: ReactNode;
}) {
  return <EmptyState icon={UserX} title={title} desc={desc} action={action} />;
}

export function NoSearchResultsEmptyState({
  title = "No results found",
  desc = "No matching items found for your search query. Try searching with different keywords.",
  action,
}: {
  title?: string;
  desc?: string;
  action?: ReactNode;
}) {
  return <EmptyState icon={SearchX} title={title} desc={desc} action={action} />;
}

export function TagChip({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border border-border bg-muted px-1.5 py-0.5 text-[11px] font-medium text-muted-foreground",
        className,
      )}
    >
      {children}
    </span>
  );
}

export function StatusDot({ online }: { online?: boolean }) {
  return (
    <span
      className={cn(
        "inline-block h-2 w-2 rounded-full ring-2 ring-card",
        online ? "bg-success" : "bg-muted-foreground/40",
      )}
    />
  );
}

export function Avatar({
  src,
  alt,
  size = 32,
  online,
}: {
  src: string;
  alt: string;
  size?: number;
  online?: boolean;
}) {
  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <img
        src={src}
        alt={alt}
        width={size}
        height={size}
        className="h-full w-full rounded-full border border-border bg-muted object-cover"
      />
      {online !== undefined && (
        <span className="absolute -bottom-0.5 -right-0.5">
          <StatusDot online={online} />
        </span>
      )}
    </div>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn("animate-pulse rounded-md bg-muted", className)} />;
}
