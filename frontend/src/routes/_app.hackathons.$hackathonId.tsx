import { useState } from "react";
import { createFileRoute, notFound, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { hackathonsService } from "@/services";
import { Card, TagChip, EmptyState, Skeleton } from "@/components/shared/primitives";
import {
  ArrowLeft,
  Trophy,
  Users2,
  Clock,
  Calendar,
  Award,
  GitBranch,
  ExternalLink,
} from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BackButton } from "@/components/shared/BackButton";

type Tab = "overview" | "teams" | "submissions" | "leaderboard";

function getTabFromURL(): Tab {
  const params = new URLSearchParams(window.location.search);
  const tab = params.get("tab");
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

function HackathonDetail() {
  const { hackathonId } = Route.useParams();
  const { data: hackathon, isLoading } = useQuery({
    queryKey: ["hackathon", hackathonId],
    queryFn: () => hackathonsService.get(hackathonId),
  });
  const { data: teams = [] } = useQuery({
    queryKey: ["hackathon-teams", hackathonId],
    queryFn: () => hackathonsService.getTeams(hackathonId),
    enabled: !!hackathonId,
  });
  const [tab, setTab] = useState<Tab>(getTabFromURL);

  const handleTabChange = (value: string) => {
    setTab(value as Tab);
    const url = new URL(window.location.href);
    url.searchParams.set("tab", value);
    window.history.replaceState({}, "", url.toString());
  };

  if (isLoading) {
    return (
      <div className="space-y-4" role="status" aria-busy="true">
        <Skeleton className="h-5 w-32" />
        <Card className="p-4">
          <div className="flex flex-wrap items-start gap-5">
            <Skeleton className="h-24 w-24 shrink-0 rounded-full" />
            <div className="min-w-0 flex-1">
              <Skeleton className="h-7 w-40" />
              <Skeleton className="h-4 w-32" />
              <Skeleton className="mt-2 h-4 w-64" />
              <Skeleton className="mt-2 h-3 w-28" />
            </div>
          </div>
        </Card>
        <div className="grid gap-3 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="p-4">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="mt-2 h-9 w-16" />
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (!hackathon) throw notFound();

  const formatDate = (d: string) =>
    new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

  return (
    <div className="space-y-4">
      <BackButton to="/hackathons" label="Back to hackathons" />

      <Card className="p-4">
        <div className="flex flex-wrap items-start gap-5">
          <span className="grid h-24 w-24 shrink-0 place-items-center rounded-lg bg-primary-soft text-primary">
            <Trophy size={32} />
          </span>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <h1 className="text-[22px] font-bold text-foreground">{hackathon.name}</h1>
              <TagChip
                className={
                  hackathon.status === "completed"
                    ? "text-muted-foreground border-border bg-muted"
                    : "text-primary border-primary/30 bg-primary/10"
                }
              >
                {hackathon.status.replace("_", " ")}
              </TagChip>
            </div>
            {hackathon.theme && (
              <p className="mt-0.5 text-[13px] text-muted-foreground">{hackathon.theme}</p>
            )}
            <p className="mt-2 text-[13px] text-foreground line-clamp-3">{hackathon.description}</p>
            <div className="mt-3 flex flex-wrap gap-3 text-[12px] text-muted-foreground">
              <span className="inline-flex items-center gap-1">
                <Calendar size={12} /> {formatDate(hackathon.starts_at)} —{" "}
                {formatDate(hackathon.ends_at)}
              </span>
              <span className="inline-flex items-center gap-1">
                <Users2 size={12} /> {hackathon.min_team_size}–{hackathon.max_team_size} per team
              </span>
              {hackathon.prize && (
                <TagChip className="text-warning border-warning/30 bg-warning/10">
                  {hackathon.prize}
                </TagChip>
              )}
            </div>
          </div>
          <div className="flex gap-2">
            <button className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-2 text-[13px] font-semibold text-primary-foreground hover:opacity-90">
              Register
            </button>
          </div>
        </div>
      </Card>

      <div className="grid gap-3 lg:grid-cols-3">
        <Card className="p-4">
          <p className="text-[13px] font-semibold text-foreground">Status</p>
          <p className="mt-2 text-[24px] font-bold capitalize text-foreground">
            {hackathon.status.replace("_", " ")}
          </p>
        </Card>
        <Card className="p-4">
          <p className="text-[13px] font-semibold text-foreground">Teams</p>
          <p className="mt-2 text-[24px] font-bold text-foreground">{teams.length}</p>
        </Card>
        <Card className="p-4">
          <p className="text-[13px] font-semibold text-foreground">Team Size</p>
          <p className="mt-2 text-[24px] font-bold text-foreground">
            {hackathon.min_team_size}–{hackathon.max_team_size}
          </p>
        </Card>
      </div>

      <Tabs value={tab} onValueChange={handleTabChange}>
        <TabsList className="overflow-x-auto">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="teams">Teams</TabsTrigger>
          <TabsTrigger value="submissions">Submissions</TabsTrigger>
          <TabsTrigger value="leaderboard">Leaderboard</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <Card className="p-4">
            <p className="text-[13px] font-semibold text-foreground">About</p>
            <p className="mt-2 text-[13px] text-muted-foreground whitespace-pre-wrap">
              {hackathon.description}
            </p>
          </Card>
          {hackathon.website_url && (
            <Card className="mt-3 p-4">
              <a
                href={hackathon.website_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-[13px] font-medium text-primary hover:underline"
              >
                <ExternalLink size={14} /> Visit website
              </a>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="teams">
          {teams.length === 0 ? (
            <Card className="p-8">
              <EmptyState
                title="No teams yet"
                desc="Be the first to create a team for this hackathon."
                action={<Users2 size={20} className="text-muted-foreground" />}
              />
            </Card>
          ) : (
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
              {teams.map((team) => (
                <Card key={team.id} interactive className="p-4">
                  <div className="flex items-start gap-3">
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-muted text-xl">
                      <Users2 size={16} />
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-[14px] font-semibold text-foreground">
                        {team.name}
                      </p>
                      {team.description && (
                        <p className="mt-0.5 line-clamp-2 text-[12px] text-muted-foreground">
                          {team.description}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="mt-3 flex items-center justify-between text-[11px] text-muted-foreground">
                    <span className="inline-flex items-center gap-1">
                      <Users2 size={12} /> {team.member_count} members
                    </span>
                    <button className="rounded-md border border-border px-2 py-1 text-[11px] font-medium hover:bg-muted">
                      Join
                    </button>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="submissions">
          <Card className="p-8">
            <EmptyState
              title="No submissions yet"
              desc="Submissions will appear here once teams start shipping."
              action={<GitBranch size={20} className="text-muted-foreground" />}
            />
          </Card>
        </TabsContent>

        <TabsContent value="leaderboard">
          <Card className="p-8">
            <EmptyState
              title="No scores yet"
              desc="The leaderboard will be populated after judging begins."
              action={<Award size={20} className="text-muted-foreground" />}
            />
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
