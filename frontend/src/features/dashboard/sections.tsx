import { ActivityFeed } from "@/components/activity/ActivityFeed";
import { Card, SectionHeader, TagChip, Avatar } from "@/components/shared/primitives";
import { useQuery } from "@tanstack/react-query";
import {
  activitiesService,
  dashboardService,
  buildersService,
  projectsService,
  flaresService,
  messagesService,
  notificationsService,
} from "@/services";
import {
  Check,
  X,
  Star,
  MessageCircle,
  FolderPlus,
  Flame,
  Users2,
  FileText,
  BarChart3,
  Trophy,
  ArrowRight,
} from "lucide-react";
import { Link } from "@tanstack/react-router";
import { cn } from "@/lib/utils";
import { motion, useReducedMotion } from "framer-motion";
import { containerVariants, cardEntrance, cardHover } from "@/lib/animations";

export function RecentActivity() {
  return (
    <Card className="border-border/60">
      <div className="px-5 pt-4 pb-2 font-semibold flex items-center gap-2 text-sm">
        Recent Activity
      </div>
      <ActivityFeed
        queryKey={["activities", "recent"]}
        queryFn={() => activitiesService.list(20)}
      />
    </Card>
  );
}

export function BuilderRequests() {
  const { data = [] } = useQuery({
    queryKey: ["builder-requests"],
    queryFn: dashboardService.builderRequests,
  });
  return (
    <Card className="border-border/60">
      <SectionHeader title="Builder Requests" action="View All" />
      <ul className="divide-y divide-border/40">
        {data.map((r) => (
          <li key={r.id} className="px-5 py-4 transition-colors hover:bg-muted/20">
            <div className="flex items-start gap-3">
              <Avatar src={r.builder.avatar} alt={r.builder.name} size={40} />
              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold text-foreground">{r.builder.name}</p>
                <p className="text-xs text-muted-foreground">{r.builder.role}</p>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {r.builder.skills.slice(0, 3).map((s) => (
                    <TagChip key={s}>{s}</TagChip>
                  ))}
                </div>
                <p className="mt-2 text-xs text-muted-foreground">
                  {r.builder.yearsExp} yrs exp ·{" "}
                  <span className="font-medium text-success">{r.builder.matchScore}% Match</span>
                </p>
              </div>
            </div>
            <div className="mt-3 flex gap-2">
              <button className="flex-1 rounded-md bg-foreground px-3 py-1.5 text-xs font-medium text-background hover:bg-foreground/90 transition-colors">
                Accept
              </button>
              <button className="flex-1 rounded-md border border-border bg-surface px-3 py-1.5 text-xs font-medium text-foreground hover:bg-muted transition-colors">
                Decline
              </button>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function InviteRequests() {
  const { data = [] } = useQuery({
    queryKey: ["invite-requests"],
    queryFn: dashboardService.inviteRequests,
  });
  return (
    <Card className="border-border/60">
      <SectionHeader title="Invite Requests" action="View All" />
      <ul className="divide-y divide-border/40">
        {data.map((r) => (
          <li
            key={r.id}
            className="flex items-center gap-4 px-5 py-4 transition-colors hover:bg-muted/20"
          >
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-foreground">{r.project}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{r.role}</p>
              <p className="text-xs text-muted-foreground mt-1">
                Due in {r.dueDays} days · By {r.by}
              </p>
            </div>
            <div className="flex flex-col gap-2 shrink-0">
              <button className="flex items-center justify-center h-8 w-8 rounded-md bg-success/10 text-success hover:bg-success/20 transition-colors">
                <Check size={14} />
              </button>
              <button className="flex items-center justify-center h-8 w-8 rounded-md bg-destructive/10 text-destructive hover:bg-destructive/20 transition-colors">
                <X size={14} />
              </button>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function SuggestedBuilders() {
  const { data = [] } = useQuery({ queryKey: ["suggested"], queryFn: buildersService.suggested });
  const prefersReducedMotion = useReducedMotion();

  return (
    <Card className="border-border/60 bg-card">
      <SectionHeader title="Suggested Builders" action="View All" actionTo="/builders" />
      <motion.div
        className="grid grid-cols-1 gap-4 p-5 pt-2 sm:grid-cols-2 lg:grid-cols-3"
        variants={containerVariants}
        initial={prefersReducedMotion ? undefined : "hidden"}
        animate={prefersReducedMotion ? undefined : "visible"}
      >
        {data.map((b, i) => (
          <motion.div
            key={b.id}
            variants={prefersReducedMotion ? undefined : cardEntrance}
            custom={i}
            className="flex flex-col rounded-xl border border-border/60 bg-surface p-4 hover:border-border transition-colors shadow-sm"
          >
            <div className="flex items-start justify-between">
              <Avatar src={b.avatar} alt={b.name} size={48} online={b.online} />
              <span className="inline-flex items-center rounded-full bg-success/10 px-2 py-0.5 text-[10px] font-semibold text-success">
                {b.matchScore}% Match
              </span>
            </div>
            <div className="mt-3">
              <p className="text-sm font-semibold text-foreground">{b.name}</p>
              <p className="text-xs text-muted-foreground mt-0.5">
                {b.role} · {b.country}
              </p>
            </div>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {b.skills.slice(0, 2).map((s) => (
                <TagChip key={s}>{s}</TagChip>
              ))}
            </div>
            <div className="mt-auto pt-4 flex w-full gap-2">
              <button className="flex-1 rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground hover:bg-primary/90 transition-colors">
                Connect
              </button>
              <button className="flex-1 rounded-md border border-border bg-surface px-3 py-1.5 text-xs font-medium text-foreground hover:bg-muted transition-colors">
                Message
              </button>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </Card>
  );
}

export function TrendingProjects() {
  const { data = [] } = useQuery({ queryKey: ["trending"], queryFn: projectsService.trending });
  return (
    <Card className="border-border/60">
      <SectionHeader title="Trending Projects" action="View All" actionTo="/projects" />
      <ul className="divide-y divide-border/40">
        {data.map((p) => (
          <li
            key={p.id}
            className="flex items-center gap-4 px-5 py-4 transition-colors hover:bg-muted/20"
          >
            <div className="flex items-center justify-center h-10 w-10 shrink-0 rounded-lg bg-muted text-lg border border-border/50">
              {p.icon}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-foreground">{p.name}</p>
              <p className="truncate text-xs text-muted-foreground mt-0.5">{p.stack.join(" · ")}</p>
            </div>
            <div className="flex items-center gap-3 text-xs font-medium text-muted-foreground">
              <span className="flex items-center gap-1.5">
                <Star size={14} className="text-muted-foreground" /> {p.stars}
              </span>
              <span className="flex items-center gap-1.5">
                <MessageCircle size={14} className="text-muted-foreground" /> {p.forks}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function AIRecommendations() {
  return (
    <Card className="relative overflow-hidden border-border/60">
      <SectionHeader title="AI Insights" />
      <div className="space-y-4 px-5 pb-5">
        <p className="text-sm text-foreground leading-relaxed">
          You need a <span className="font-semibold">Backend Developer</span> for your project{" "}
          <span className="font-semibold text-primary">AI Chatbot</span>
        </p>
        <div className="rounded-xl border border-primary/20 bg-primary/5 p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-primary mb-3">
            Top Match
          </p>
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-3">
              <Avatar
                src="https://api.dicebear.com/9.x/notionists-neutral/svg?seed=Rahul"
                alt="Rahul"
                size={40}
              />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-semibold text-foreground">Rahul Verma</p>
                <p className="text-xs text-muted-foreground">Full Stack Developer</p>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-success">93% Match</span>
              <button className="rounded-md bg-foreground px-3 py-1.5 text-xs font-medium text-background hover:bg-foreground/90 transition-colors">
                Invite
              </button>
            </div>
          </div>
        </div>
        <div className="rounded-xl bg-muted/40 p-4 border border-border/50">
          <p className="text-xs font-semibold text-foreground">Why this match?</p>
          <ul className="mt-3 space-y-2 text-xs text-muted-foreground">
            <li className="flex items-center gap-2">
              <Check size={14} className="text-success" /> Skills match 90%
            </li>
            <li className="flex items-center gap-2">
              <Check size={14} className="text-success" /> Past experience in AI
            </li>
            <li className="flex items-center gap-2">
              <Check size={14} className="text-success" /> Available this week
            </li>
          </ul>
        </div>
      </div>
    </Card>
  );
}

export function MessagesPreview() {
  const { data = [] } = useQuery({
    queryKey: ["conversations"],
    queryFn: messagesService.conversations,
  });
  return (
    <Card className="border-border/60">
      <SectionHeader title="Messages" action="View All" actionTo="/messages" />
      <ul className="divide-y divide-border/40">
        {data.map((c) => (
          <li key={c.id}>
            <Link
              to="/messages/$conversationId"
              params={{ conversationId: c.id }}
              className="flex items-center gap-3 px-5 py-3.5 transition-colors hover:bg-muted/20"
            >
              <Avatar src={c.with.avatar} alt={c.with.name} size={36} online={c.with.online} />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-semibold text-foreground">{c.with.name}</p>
                <p className="truncate text-xs text-muted-foreground mt-0.5">{c.preview}</p>
              </div>
              <span className="text-xs text-muted-foreground">{c.ago}</span>
            </Link>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function QuickActions() {
  const actions = [
    {
      icon: FolderPlus,
      label: "New Project",
      to: "/projects" as const,
    },
    {
      icon: Users2,
      label: "Find Builder",
      to: "/builders" as const,
    },
    {
      icon: Flame,
      label: "Create Flare",
      to: "/flares" as const,
    },
    {
      icon: Trophy,
      label: "Hackathons",
      to: "/hackathons" as const,
    },
  ];
  return (
    <Card className="border-border/60 bg-transparent shadow-none border-none">
      <div className="grid grid-cols-2 gap-3">
        {actions.map((a) => (
          <Link
            key={a.label}
            to={a.to}
            className="group flex items-center gap-3 rounded-xl border border-border/60 bg-card p-4 transition-all hover:border-border hover:bg-muted/20"
          >
            <span className="flex items-center justify-center h-8 w-8 rounded-md bg-muted text-muted-foreground group-hover:text-foreground group-hover:bg-muted/80 transition-colors">
              <a.icon size={16} />
            </span>
            <span className="text-sm font-medium text-foreground">{a.label}</span>
          </Link>
        ))}
      </div>
    </Card>
  );
}

export function UpcomingDeadlines() {
  const { data = [] } = useQuery({ queryKey: ["deadlines"], queryFn: dashboardService.deadlines });
  const sevTint = {
    danger: "text-destructive font-medium",
    warning: "text-warning font-medium",
    info: "text-info font-medium",
  } as const;
  return (
    <Card className="border-border/60">
      <SectionHeader title="Deadlines" action="Calendar" />
      <ul className="divide-y divide-border/40">
        {data.map((d) => (
          <li
            key={d.id}
            className="flex items-center gap-3 px-5 py-3.5 transition-colors hover:bg-muted/20"
          >
            <div className="h-2 w-2 rounded-full bg-border" />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-foreground">{d.project}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{d.milestone}</p>
            </div>
            <span className={cn("whitespace-nowrap text-xs", sevTint[d.severity])}>
              In {d.dueDays}d
            </span>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function NotificationsFeed() {
  const { data = [] } = useQuery({
    queryKey: ["notifications"],
    queryFn: notificationsService.list,
  });
  return (
    <Card className="border-border/60">
      <SectionHeader title="Notifications" action="View All" actionTo="/notifications" />
      <ul className="divide-y divide-border/40">
        {data.map((n) => (
          <li
            key={n.id}
            className="flex items-start gap-3 px-5 py-3.5 transition-colors hover:bg-muted/20"
          >
            <span
              className={cn(
                "mt-1.5 h-2 w-2 shrink-0 rounded-full",
                n.unread ? "bg-primary" : "bg-transparent",
              )}
            />
            <div className="min-w-0 flex-1">
              <p className="text-sm text-foreground">{n.text}</p>
              <p className="text-xs text-muted-foreground mt-1">{n.ago}</p>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}
