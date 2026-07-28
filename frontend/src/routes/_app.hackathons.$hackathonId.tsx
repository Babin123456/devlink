import { useState } from "react";
import { createFileRoute, notFound } from "@tanstack/react-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { hackathonsService } from "@/services";
import { Card, TagChip, Skeleton, EmptyState } from "@/components/shared/primitives";
import { Trophy, Users2, Calendar, ExternalLink, CheckCircle2, Award, GitBranch } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BackButton } from "@/components/shared/BackButton";
import { RegisterDialog } from "@/components/hackathons/RegisterDialog";
import { TeamsTab } from "@/components/hackathons/TeamsTab";
import { SubmissionsTab } from "@/components/hackathons/SubmissionsTab";
import { LeaderboardTab } from "@/components/hackathons/LeaderboardTab";

type Tab = "overview" | "teams" | "submissions" | "leaderboard";

function getInitialTab(): Tab {
  if (typeof window === "undefined") return "overview";
  const tab = new URLSearchParams(window.location.search).get("tab");
  if (tab === "overview" || tab === "teams" || tab === "submissions" || tab === "leaderboard")
    return tab;
  return "overview";
}

export const Route = createFileRoute("/_app/hackathons/$hackathonId")({
  head: () => ({
    meta: [
      { title: "Hackathon — DevLink" },
      { name: "description", content: "View hackathon details on DevLink." },
    ],
  }),
  component: HackathonDetail,
});

const STATUS_META: Record<string, { label: string; className: string }> = {
  draft: { label: "Draft", className: "border-border bg-muted text-muted-foreground" },
  registration_open: { label: "Registration open", className: "border-success/30 bg-success/10 text-success" },
  in_progress: { label: "In progress", className: "border-primary/30 bg-primary/10 text-primary" },
  judging: { label: "Judging", className: "border-warning/30 bg-warning/10 text-warning" },
  completed: { label: "Completed", className: "border-border bg-muted text-muted-foreground" },
  cancelled: { label: "Cancelled", className: "border-destructive/30 bg-destructive/10 text-destructive" },
};

function HackathonDetail() {
  const { hackathonId } = Route.useParams();
  const queryClient = useQueryClient();
  const [tab, setTab] = useState<Tab>(getInitialTab);
  const [registerOpen, setRegisterOpen] = useState(false);
  // Track registration locally — persists as long as user stays on page
  const [registered, setRegistered] = useState(() =>
    hackathonsService.isRegistered(hackathonId),
  );

  const { data: hackathon, isLoading } = useQuery({
    queryKey: ["hackathon", hackathonId],
    queryFn: () => hackathonsService.get(hackathonId),
  });

  const { data: teams = [] } = useQuery({
    queryKey: ["hackathon-teams", hackathonId],
    queryFn: () => hackathonsService.getTeams(hackathonId),
    enabled: !!hackathonId,
  });

  function handleTabChange(value: string) {
    setTab(value as Tab);
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("tab", value);
      window.history.replaceState({}, "", url.toString());
    }
  }

  function handleRegistered() {
    setRegistered(true);
    setRegisterOpen(false);
    queryClient.invalidateQueries({ queryKey: ["hackathon", hackathonId] });
  }

  // ── Loading ──────────────────────────────────────────────────────────────
  if (isLoading) {
    return (
      <div className="space-y-4" aria-busy="true">
        <Skeleton className="h-5 w-32" />
        <Card className="p-6">
          <div className="flex flex-wrap gap-5">
            <Skeleton className="h-20 w-20 shrink-0 rounded-xl" />
            <div className="flex-1 space-y-2">
              <Skeleton className="h-7 w-48" />
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-4 w-64" />
            </div>
          </div>
        </Card>
        <div className="grid gap-3 sm:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="h-20 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (!hackathon) throw notFound();

  const fmt = (d: string) =>
    new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

  const statusMeta = STATUS_META[hackathon.status] ?? {
    label: hackathon.status.replace(/_/g, " "),
    className: "border-border bg-muted text-muted-foreground",
  };
  const canRegister = !registered && hackathon.status !== "completed" && hackathon.status !== "cancelled";

  return (
    <div className="space-y-4">
      <BackButton to="/hackathons" label="Back to hackathons" />

      {/* Hero */}
      <Card className="p-4 sm:p-6">
        <div className="flex flex-wrap items-start gap-4">
          <span className="grid h-16 w-16 shrink-0 place-items-center rounded-xl bg-primary-soft text-primary">
            <Trophy size={28} />
          </span>

          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-[20px] font-bold text-foreground sm:text-[22px]">
                {hackathon.name}
              </h1>
              <TagChip className={statusMeta.className}>{statusMeta.label}</TagChip>
            </div>
            {hackathon.theme && (
              <p className="mt-0.5 text-[13px] text-muted-foreground">{hackathon.theme}</p>
            )}
            <p className="mt-2 line-clamp-3 text-[13px] text-foreground/80">
              {hackathon.description}
            </p>
            <div className="mt-3 flex flex-wrap gap-3 text-[12px] text-muted-foreground">
              <span className="inline-flex items-center gap-1">
                <Calendar size={12} />
                {fmt(hackathon.starts_at)} — {fmt(hackathon.ends_at)}
              </span>
              <span className="inline-flex items-center gap-1">
                <Users2 size={12} />
                {hackathon.min_team_size}–{hackathon.max_team_size} per team
              </span>
              {hackathon.prize && (
                <TagChip className="border-warning/30 bg-warning/10 text-warning">
                  🏆 {hackathon.prize}
                </TagChip>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex shrink-0 flex-wrap items-start gap-2">
            {registered ? (
              <span className="inline-flex items-center gap-1.5 rounded-md border border-success/30 bg-success/10 px-3 py-2 text-[13px] font-semibold text-success">
                <CheckCircle2 size={14} /> Registered
              </span>
            ) : canRegister ? (
              <button
                onClick={() => setRegisterOpen(true)}
                className="rounded-md bg-primary px-4 py-2 text-[13px] font-semibold text-primary-foreground hover:opacity-90"
              >
                Register now
              </button>
            ) : null}
            {hackathon.website_url && (
              <a
                href={hackathon.website_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 rounded-md border border-border px-3 py-2 text-[13px] font-medium text-foreground hover:bg-muted"
              >
                <ExternalLink size={13} /> Website
              </a>
            )}
          </div>
        </div>
      </Card>

      {/* Stats */}
      <div className="grid gap-3 sm:grid-cols-3">
        <Card className="p-4">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">Status</p>
          <p className="mt-1 text-[18px] font-bold capitalize text-foreground">
            {hackathon.status.replace(/_/g, " ")}
          </p>
        </Card>
        <Card className="p-4">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">Teams</p>
          <p className="mt-1 text-[18px] font-bold text-foreground">{teams.length}</p>
        </Card>
        <Card className="p-4">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">Team size</p>
          <p className="mt-1 text-[18px] font-bold text-foreground">
            {hackathon.min_team_size}–{hackathon.max_team_size}
          </p>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={tab} onValueChange={handleTabChange}>
        <TabsList className="w-full overflow-x-auto sm:w-auto">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="teams">
            Teams
            {teams.length > 0 && (
              <span className="ml-1.5 rounded-full bg-primary/15 px-1.5 py-0.5 text-[10px] font-bold text-primary">
                {teams.length}
              </span>
            )}
          </TabsTrigger>
          <TabsTrigger value="submissions">Submissions</TabsTrigger>
          <TabsTrigger value="leaderboard">Leaderboard</TabsTrigger>
        </TabsList>

        {/* ── Overview ── */}
        <TabsContent value="overview" className="mt-3 space-y-3">
          <Card className="p-4">
            <h2 className="text-[13px] font-semibold text-foreground">About this hackathon</h2>
            <p className="mt-2 whitespace-pre-wrap text-[13px] leading-relaxed text-muted-foreground">
              {hackathon.description}
            </p>
          </Card>

          <div className="grid gap-3 sm:grid-cols-2">
            <Card className="p-4">
              <h2 className="text-[13px] font-semibold text-foreground">Schedule</h2>
              <dl className="mt-2 space-y-2 text-[13px]">
                <div className="flex items-center justify-between gap-2">
                  <dt className="text-muted-foreground">Starts</dt>
                  <dd className="font-medium text-foreground">{fmt(hackathon.starts_at)}</dd>
                </div>
                <div className="flex items-center justify-between gap-2">
                  <dt className="text-muted-foreground">Ends</dt>
                  <dd className="font-medium text-foreground">{fmt(hackathon.ends_at)}</dd>
                </div>
              </dl>
            </Card>
            <Card className="p-4">
              <h2 className="text-[13px] font-semibold text-foreground">Team rules</h2>
              <dl className="mt-2 space-y-2 text-[13px]">
                <div className="flex items-center justify-between gap-2">
                  <dt className="text-muted-foreground">Minimum</dt>
                  <dd className="font-medium text-foreground">{hackathon.min_team_size} member{hackathon.min_team_size !== 1 ? "s" : ""}</dd>
                </div>
                <div className="flex items-center justify-between gap-2">
                  <dt className="text-muted-foreground">Maximum</dt>
                  <dd className="font-medium text-foreground">{hackathon.max_team_size} members</dd>
                </div>
                {hackathon.prize && (
                  <div className="flex items-center justify-between gap-2">
                    <dt className="text-muted-foreground">Prize pool</dt>
                    <dd className="font-medium text-warning">{hackathon.prize}</dd>
                  </div>
                )}
              </dl>
            </Card>
          </div>

          {!registered && canRegister && (
            <Card className="flex items-center justify-between gap-4 p-4">
              <div>
                <p className="text-[13px] font-semibold text-foreground">Ready to join?</p>
                <p className="text-[12px] text-muted-foreground">
                  Register to form or join a team and submit your project.
                </p>
              </div>
              <button
                onClick={() => setRegisterOpen(true)}
                className="shrink-0 rounded-md bg-primary px-4 py-2 text-[13px] font-semibold text-primary-foreground hover:opacity-90"
              >
                Register now
              </button>
            </Card>
          )}
        </TabsContent>

        {/* ── Teams ── */}
        <TabsContent value="teams" className="mt-3">
          <TeamsTab hackathonId={hackathonId} maxTeamSize={hackathon.max_team_size} />
        </TabsContent>

        {/* ── Submissions ── */}
        <TabsContent value="submissions" className="mt-3">
          <SubmissionsTab hackathonId={hackathonId} teams={teams} />
        </TabsContent>

        {/* ── Leaderboard ── */}
        <TabsContent value="leaderboard" className="mt-3">
          <LeaderboardTab hackathonId={hackathonId} />
        </TabsContent>
      </Tabs>

      {/* Register dialog */}
      <RegisterDialog
        hackathonId={hackathonId}
        hackathonName={hackathon.name}
        open={registerOpen}
        onOpenChange={setRegisterOpen}
        onRegistered={handleRegistered}
      />
    </div>
  );
}
