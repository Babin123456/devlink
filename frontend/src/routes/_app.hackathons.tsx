import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { hackathonsService } from "@/services";
import { Card, TagChip } from "@/components/shared/primitives";
import { Trophy, Users2, Clock } from "lucide-react";

export const Route = createFileRoute("/_app/hackathons")({
  head: () => ({
    meta: [
      { title: "Hackathons — DevLink" },
      { name: "description", content: "Discover hackathons, form teams and ship in a weekend." },
    ],
  }),
  component: HackathonsPage,
});

function HackathonsPage() {
  const { data = [] } = useQuery({ queryKey: ["hackathons"], queryFn: hackathonsService.list });

  const formatDate = (d: string) =>
    new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric" });

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-[22px] font-bold tracking-tight text-foreground">Hackathons</h1>
        <p className="text-[13px] text-muted-foreground">
          Join a jam, build a team, ship something new.
        </p>
      </div>
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {data.map((h) => (
          <Link key={h.id} to="/hackathons/$hackathonId" params={{ hackathonId: h.id }}>
            <Card interactive className="p-4">
              <div className="flex items-start justify-between">
                <span className="grid h-10 w-10 place-items-center rounded-md bg-primary-soft text-primary">
                  <Trophy size={16} />
                </span>
                <TagChip
                  className={
                    h.status === "completed"
                      ? "text-muted-foreground border-border bg-muted"
                      : "text-primary border-primary/30 bg-primary/10"
                  }
                >
                  {h.status.replace("_", " ")}
                </TagChip>
              </div>
              <p className="mt-3 text-[15px] font-semibold text-foreground">{h.name}</p>
              <p className="mt-0.5 text-[12px] text-muted-foreground">{h.theme}</p>
              <div className="mt-3 flex flex-wrap gap-2 text-[11px] text-muted-foreground">
                <span className="inline-flex items-center gap-1">
                  <Clock size={11} /> {formatDate(h.starts_at)}
                </span>
                <span className="inline-flex items-center gap-1">
                  <Users2 size={11} /> {h.min_team_size}–{h.max_team_size}
                </span>
                {h.prize && (
                  <TagChip className="text-warning border-warning/30 bg-warning/10">
                    {h.prize}
                  </TagChip>
                )}
              </div>
              <button className="mt-4 w-full rounded-md bg-primary py-1.5 text-[12px] font-semibold text-primary-foreground hover:opacity-90">
                View details
              </button>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
