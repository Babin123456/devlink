import { createFileRoute, Link, Outlet, useRouterState } from "@tanstack/react-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { hackathonsService } from "@/services";
import { Card, TagChip, Skeleton } from "@/components/shared/primitives";
import { Trophy, Users2, Clock, Plus, ArrowRight } from "lucide-react";
import { useState } from "react";
import { CreateHackathonDialog } from "@/components/hackathons/CreateHackathonDialog";

export const Route = createFileRoute("/_app/hackathons")({
  head: () => ({
    meta: [
      { title: "Hackathons — DevLink" },
      { name: "description", content: "Discover hackathons, form teams and ship in a weekend." },
    ],
  }),
  component: HackathonsLayout,
});

const STATUS_COLOR: Record<string, string> = {
  registration_open: "text-success border-success/30 bg-success/10",
  in_progress: "text-primary border-primary/30 bg-primary/10",
  judging: "text-warning border-warning/30 bg-warning/10",
  completed: "text-muted-foreground border-border bg-muted",
  cancelled: "text-destructive border-destructive/30 bg-destructive/10",
  draft: "text-muted-foreground border-border bg-muted",
};

// Layout component — shows list on /hackathons, delegates child routes via Outlet
function HackathonsLayout() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  // If we're on a child route (e.g. /hackathons/h1), render the child
  if (pathname !== "/hackathons" && !pathname.endsWith("/hackathons")) {
    return <Outlet />;
  }

  return <HackathonsList />;
}

function HackathonsList() {
  const queryClient = useQueryClient();
  const [createOpen, setCreateOpen] = useState(false);

  const { data = [], isLoading } = useQuery({
    queryKey: ["hackathons"],
    queryFn: hackathonsService.list,
  });

  const formatDate = (d: string) =>
    new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-[22px] font-bold tracking-tight text-foreground">Hackathons</h1>
          <p className="text-[13px] text-muted-foreground">
            Join a jam, build a team, and ship something new.
          </p>
        </div>
        <button
          onClick={() => setCreateOpen(true)}
          className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-2 text-[13px] font-semibold text-primary-foreground hover:opacity-90"
        >
          <Plus size={14} /> Create hackathon
        </button>
      </div>

      {/* Loading skeletons */}
      {isLoading && (
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="h-52 animate-pulse" />
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && data.length === 0 && (
        <Card className="p-12 text-center">
          <div className="mx-auto mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-primary-soft text-primary">
            <Trophy size={22} />
          </div>
          <p className="text-[14px] font-semibold text-foreground">No hackathons yet</p>
          <p className="mt-1 text-[13px] text-muted-foreground">Be the first to create one.</p>
          <button
            onClick={() => setCreateOpen(true)}
            className="mt-4 inline-flex items-center gap-1.5 rounded-md bg-primary px-4 py-2 text-[13px] font-semibold text-primary-foreground hover:opacity-90"
          >
            <Plus size={14} /> Create hackathon
          </button>
        </Card>
      )}

      {/* Hackathon cards */}
      {!isLoading && data.length > 0 && (
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {data.map((h) => (
            <Link
              key={h.id}
              to="/hackathons/$hackathonId"
              params={{ hackathonId: h.id }}
              className="block rounded-2xl focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/50"
            >
              <Card interactive className="flex h-full flex-col p-4">
                {/* Top row */}
                <div className="flex items-start justify-between gap-2">
                  <span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-primary-soft text-primary">
                    <Trophy size={16} />
                  </span>
                  <TagChip className={STATUS_COLOR[h.status] ?? STATUS_COLOR.draft}>
                    {h.status.replace(/_/g, " ")}
                  </TagChip>
                </div>

                {/* Title + theme */}
                <p className="mt-3 line-clamp-1 text-[15px] font-semibold text-foreground">
                  {h.name}
                </p>
                {h.theme && (
                  <p className="mt-0.5 line-clamp-1 text-[12px] text-muted-foreground">
                    {h.theme}
                  </p>
                )}

                {/* Description */}
                <p className="mt-1.5 line-clamp-2 flex-1 text-[12px] text-muted-foreground">
                  {h.description}
                </p>

                {/* Meta */}
                <div className="mt-3 flex flex-wrap gap-2 text-[11px] text-muted-foreground">
                  <span className="inline-flex items-center gap-1">
                    <Clock size={11} /> {formatDate(h.starts_at)}
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <Users2 size={11} /> {h.min_team_size}–{h.max_team_size}
                  </span>
                  {h.prize && (
                    <TagChip className="border-warning/30 bg-warning/10 text-warning">
                      🏆 {h.prize}
                    </TagChip>
                  )}
                </div>

                {/* Footer */}
                <div className="mt-4 flex items-center justify-between border-t border-border/60 pt-3">
                  <span className="text-[12px] font-medium text-primary">View details</span>
                  <ArrowRight size={13} className="text-primary" />
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}

      <CreateHackathonDialog
        open={createOpen}
        onOpenChange={(open) => {
          setCreateOpen(open);
          if (!open) queryClient.invalidateQueries({ queryKey: ["hackathons"] });
        }}
      />
    </div>
  );
}
