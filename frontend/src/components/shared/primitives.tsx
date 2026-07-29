import { cn, getInitials } from "@/lib/utils";
import { Link } from "@tanstack/react-router";
import { useEffect, useState, type ReactNode, type ComponentType } from "react";
import { motion } from "framer-motion";
import { useCardAnimation } from "@/lib/animations";
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
    <div className={cn("flex items-center justify-between px-5 pt-4 pb-3.5", className)}>
      <h3 className="text-[14px] font-bold tracking-tight text-foreground flex items-center gap-2">
        <span className="inline-block h-2 w-2 rounded-full bg-primary/80" />
        {title}
      </h3>
      {action &&
        (actionTo ? (
          <Link
            to={actionTo}
            className="text-[12px] font-semibold text-primary transition-all hover:text-primary/80 hover:underline"
          >
            {action}
          </Link>
        ) : (
          <button className="text-[12px] font-semibold text-primary transition-all hover:text-primary/80 hover:underline">
            {action}
          </button>
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
        "rounded-2xl border border-border/70 bg-card shadow-xs transition-all duration-200",
        interactive && "hover-lift hover:border-primary/40 hover:shadow-card",
        className,
      )}
    >
      {children}
    </As>
  );
}

export function AnimatedCard({
  children,
  className,
  interactive = false,
  index = 0,
}: {
  children?: ReactNode;
  className?: string;
  interactive?: boolean;
  index?: number;
}) {
  const animation = useCardAnimation(index);

  return (
    <motion.div
      variants={animation.variants}
      initial={animation.initial}
      animate={animation.animate}
      custom={animation.custom}
      whileHover={animation.whileHover}
    >
      <Card interactive={interactive} className={cn("will-change-transform", className)}>
        {children}
      </Card>
    </motion.div>
  );
}

export function EmptyState({
  icon: Icon = Sparkles,
  title,
  desc,
  action,
  className,
}: {
  icon?: ComponentType<{ className?: string; size?: number }> | ReactNode;
  title: string;
  desc?: string;
  action?: ReactNode;
  className?: string;
}) {
  const isComponent =
    typeof Icon === "function" ||
    (typeof Icon === "object" && Icon !== null && "render" in (Icon as object));
  const IconComp = isComponent
    ? (Icon as ComponentType<{ className?: string; size?: number }>)
    : null;

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
        "inline-flex items-center rounded-full border border-border/60 bg-muted/80 px-2 py-0.5 text-[11px] font-medium text-muted-foreground transition-colors hover:border-primary/40 hover:bg-primary-soft/40 hover:text-primary",
        className,
      )}
    >
      {children}
    </span>
  );
}

export function StatusDot({ online }: { online?: boolean }) {
  return (
    <span className="relative flex h-2.5 w-2.5">
      {online && (
        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-success opacity-75" />
      )}
      <span
        className={cn(
          "relative inline-flex h-2.5 w-2.5 rounded-full ring-2 ring-card",
          online ? "bg-success" : "bg-muted-foreground/40",
        )}
      />
    </span>
  );
}

export function Avatar({
  src,
  alt,
  size = 32,
  online,
  name,
  className,
}: {
  src?: string | null;
  alt: string;
  size?: number;
  online?: boolean;
  name?: string | null;
  className?: string;
}) {
  const [hasError, setHasError] = useState(false);
  const normalizedSrc = typeof src === "string" ? src.trim() : "";
  const shouldRenderImage = Boolean(normalizedSrc) && !hasError;
  const fallbackLabel = alt || name || "User avatar";

  useEffect(() => {
    setHasError(false);
  }, [normalizedSrc]);

  return (
    <div className={cn("relative shrink-0", className)} style={{ width: size, height: size }}>
      {shouldRenderImage ? (
        <img
          src={normalizedSrc}
          alt={alt}
          width={size}
          height={size}
          onError={() => setHasError(true)}
          className="h-full w-full rounded-full border border-border bg-muted object-cover"
        />
      ) : (
        <div
          aria-label={fallbackLabel}
          className="flex h-full w-full items-center justify-center rounded-full border border-border bg-primary/10 text-[0.7rem] font-semibold uppercase tracking-[0.12em] text-primary"
        >
          {getInitials(name ?? alt)}
        </div>
      )}
      {online !== undefined && (
        <span className="absolute -bottom-0.5 -right-0.5">
          <StatusDot online={online} />
        </span>
      )}
    </div>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn("animate-pulse rounded-xl bg-muted/70", className)} />;
}
