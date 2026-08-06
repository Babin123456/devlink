import { useState } from "react";
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
  Sparkles,
} from "lucide-react";
import { Link } from "@tanstack/react-router";
import { cn } from "@/lib/utils";
import { motion, useReducedMotion } from "framer-motion";
import { containerVariants, cardEntrance, cardHover } from "@/lib/animations";

export function RecentActivity() {
  return (
    <Card className="border-border/60 rounded-2xl bg-card shadow-sm hover:shadow-md transition-shadow duration-200 flex flex-col h-full">
      <div className="px-5 pt-5 pb-2 font-semibold flex items-center gap-2 text-sm">
        Recent Activity
      </div>
      <div className="flex-1 overflow-hidden">
        <ActivityFeed
          queryKey={["activities", "recent"]}
          queryFn={() => activitiesService.list(5)}
        />
      </div>
    </Card>
  );
}

export function CollaborationRequests() {
  const [activeTab, setActiveTab] = useState<"builders" | "invites">("builders");

  const { data: builderReqs = [] } = useQuery({
    queryKey: ["builder-requests"],
    queryFn: dashboardService.builderRequests,
  });

  const { data: inviteReqs = [] } = useQuery({
    queryKey: ["invite-requests"],
    queryFn: dashboardService.inviteRequests,
  });

  return (
    <Card className="border-border/60 rounded-2xl bg-card shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center justify-between border-b border-border/40 px-5 py-3">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab("builders")}
            className={cn(
              "text-xs font-semibold pb-1 border-b-2 transition-all cursor-pointer",
              activeTab === "builders"
                ? "border-primary text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground"
            )}
          >
            Builder Connections ({builderReqs.length})
          </button>
          <button
            onClick={() => setActiveTab("invites")}
            className={cn(
              "text-xs font-semibold pb-1 border-b-2 transition-all cursor-pointer",
              activeTab === "invites"
                ? "border-primary text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground"
            )}
          >
            Project Invites ({inviteReqs.length})
          </button>
        </div>
        <span className="text-[10px] uppercase font-bold tracking-wider text-muted-foreground">Requests</span>
      </div>

      <div className="min-h-[220px]">
        {activeTab === "builders" ? (
          builderReqs.length === 0 ? (
            <div className="p-8 text-center text-xs text-muted-foreground">No connection requests</div>
          ) : (
            <ul className="divide-y divide-border/40">
              {builderReqs.slice(0, 3).map((r) => (
                <li key={r.id} className="px-5 py-4 transition-colors hover:bg-muted/10">
                  <div className="flex items-start gap-3">
                    <Avatar src={r.builder.avatar} alt={r.builder.name} size={40} />
                    <div className="min-w-0 flex-1">
                      <div className="flex justify-between items-start">
                        <p className="text-sm font-semibold text-foreground">{r.builder.name}</p>
                        <span className="text-xs font-bold text-success bg-success/15 px-1.5 py-0.5 rounded border border-success/20">
                          {r.builder.matchScore}% Match
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground">{r.builder.role}</p>
                      <div className="mt-2 flex flex-wrap gap-1.5">
                        {r.builder.skills.slice(0, 3).map((s) => (
                          <TagChip key={s}>{s}</TagChip>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="mt-3 flex gap-2">
                    <button className="flex-1 rounded-md bg-foreground px-3 py-1.5 text-xs font-medium text-background hover:bg-foreground/90 transition-colors cursor-pointer">
                      Accept
                    </button>
                    <button className="flex-1 rounded-md border border-border bg-surface px-3 py-1.5 text-xs font-medium text-foreground hover:bg-muted transition-colors cursor-pointer">
                      Decline
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )
        ) : (
          inviteReqs.length === 0 ? (
            <div className="p-8 text-center text-xs text-muted-foreground">No project invites</div>
          ) : (
            <ul className="divide-y divide-border/40">
              {inviteReqs.slice(0, 3).map((r) => (
                <li
                  key={r.id}
                  className="flex items-center gap-4 px-5 py-4 transition-colors hover:bg-muted/10"
                >
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold text-foreground">{r.project}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">{r.role}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Due in {r.dueDays} days · By {r.by}
                    </p>
                  </div>
                  <div className="flex gap-2 shrink-0">
                    <button className="flex items-center justify-center h-8 w-8 rounded-md bg-success/10 text-success hover:bg-success/20 transition-colors cursor-pointer">
                      <Check size={14} />
                    </button>
                    <button className="flex items-center justify-center h-8 w-8 rounded-md bg-destructive/10 text-destructive hover:bg-destructive/20 transition-colors cursor-pointer">
                      <X size={14} />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )
        )}
      </div>
    </Card>
  );
}

export function RecommendedBuilders() {
  const { data = [] } = useQuery({ queryKey: ["suggested"], queryFn: buildersService.suggested });

  // AI top match Rahul Verma
  const aiMatch = {
    name: "Rahul Verma",
    role: "Full Stack Developer",
    avatar: "https://api.dicebear.com/9.x/notionists-neutral/svg?seed=Rahul",
    matchScore: 93,
    insight: "Recommended backend expert for your AI Chatbot project",
  };

  return (
    <Card className="border-border/60 rounded-2xl bg-card shadow-sm hover:shadow-md transition-shadow duration-200">
      <SectionHeader title="Recommended Builders & AI Insights" action="View All" actionTo="/builders" />
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 p-5 pt-2">
        {/* Left Column: AI Top Match (col-span-5) */}
        <div className="lg:col-span-5 flex flex-col justify-between rounded-xl border-2 border-primary/20 bg-primary/5 p-4 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 group-hover:bg-primary/20 transition-colors"></div>
          <div className="relative z-10 flex flex-col h-full justify-between gap-4">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold uppercase tracking-widest text-primary">
                  AI Recommended Match
                </span>
                <span className="text-xs font-bold text-success flex items-center gap-1 bg-success/15 px-2 py-0.5 rounded-full border border-success/20">
                  <Sparkles size={11} className="text-success animate-pulse" /> {aiMatch.matchScore}% Match
                </span>
              </div>
              <div className="flex items-center gap-3">
                <Avatar
                  src={aiMatch.avatar}
                  alt={aiMatch.name}
                  size={44}
                  className="shadow-sm border border-primary/20"
                />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold text-foreground">{aiMatch.name}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{aiMatch.role}</p>
                </div>
              </div>
              <p className="text-xs text-foreground/80 mt-3 leading-relaxed">
                {aiMatch.insight}
              </p>
            </div>
            <button className="w-full rounded-lg bg-foreground px-3 py-2 text-xs font-semibold text-background hover:bg-foreground/90 transition-colors shadow-sm flex items-center justify-center gap-1.5 cursor-pointer mt-2">
              <Check size={14} /> Invite Rahul to Project
            </button>
          </div>
        </div>

        {/* Right Column: Other Suggestions (col-span-7) */}
        <div className="lg:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.slice(0, 2).map((b) => {
            const visibleSkills = b.skills.slice(0, 2);
            const hiddenSkillsCount = b.skills.length - visibleSkills.length;
            return (
              <div
                key={b.id}
                className="flex flex-col justify-between rounded-xl border border-border/60 bg-surface p-4 hover:border-border hover:shadow-xs transition-all"
              >
                <div>
                  <div className="flex items-start justify-between gap-2">
                    <Avatar
                      src={b.avatar}
                      alt={b.name}
                      size={40}
                      online={b.online}
                      className="shadow-sm"
                    />
                    <span className="inline-flex items-center rounded-full bg-success/10 px-2 py-0.5 text-[10px] font-bold text-success border border-success/20">
                      {b.matchScore}% Match
                    </span>
                  </div>
                  <div className="mt-3">
                    <p className="text-sm font-semibold text-foreground">{b.name}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {b.role} · {b.country}
                    </p>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-1 items-start content-start">
                    {visibleSkills.map((s) => (
                      <TagChip key={s}>{s}</TagChip>
                    ))}
                    {hiddenSkillsCount > 0 && (
                      <span className="inline-flex items-center rounded-md border border-border/50 bg-muted/30 px-1.5 py-0.5 text-[9px] font-medium text-muted-foreground">
                        +{hiddenSkillsCount}
                      </span>
                    )}
                  </div>
                </div>
                <div className="mt-4 flex w-full gap-2">
                  <button className="flex-1 rounded-lg bg-primary px-2.5 py-1.5 text-xs font-semibold text-primary-foreground hover:bg-primary/90 transition-colors shadow-sm cursor-pointer">
                    Connect
                  </button>
                  <button className="flex-1 rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs font-semibold text-foreground hover:bg-muted transition-colors cursor-pointer">
                    Message
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </Card>
  );
}

export function TrendingProjects() {
  const { data = [] } = useQuery({ queryKey: ["trending"], queryFn: projectsService.trending });
  return (
    <Card className="border-border/60 rounded-2xl bg-card shadow-sm hover:shadow-md transition-shadow duration-200">
      <SectionHeader title="Trending Projects" action="View All" actionTo="/projects" />
      <ul className="divide-y divide-border/40">
        {data.slice(0, 4).map((p) => (
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

// AIRecommendations removed as it is now integrated into RecommendedBuilders

export function MessagesPreview() {
  const { data = [] } = useQuery({
    queryKey: ["conversations"],
    queryFn: messagesService.conversations,
  });
  return (
    <Card className="border-border/60 rounded-2xl bg-card shadow-sm hover:shadow-md transition-shadow duration-200">
      <SectionHeader title="Messages" action="View All" actionTo="/messages" />
      <ul className="divide-y divide-border/40">
        {data.slice(0, 4).map((c) => (
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
      <div className="grid grid-cols-2 gap-4">
        {actions.map((a) => (
          <Link
            key={a.label}
            to={a.to}
            className="group flex flex-col items-start gap-4 rounded-2xl border border-border/60 bg-card p-5 transition-all hover:border-border hover:shadow-md hover:-translate-y-0.5"
          >
            <span className="flex items-center justify-center h-10 w-10 rounded-xl bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
              <a.icon size={20} />
            </span>
            <span className="text-sm font-semibold text-foreground">{a.label}</span>
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
    <Card className="border-border/60 rounded-2xl bg-card shadow-sm hover:shadow-md transition-shadow duration-200">
      <SectionHeader title="Deadlines" action="Calendar" />
      <ul className="divide-y divide-border/40">
        {data.slice(0, 3).map((d) => (
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

// NotificationsFeed removed as notifications are accessible in the navbar notification center and redundant with recent activities feed
