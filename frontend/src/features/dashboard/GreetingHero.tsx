import { Card } from "@/components/shared/primitives";
import { Flame, Sparkles, TrendingUp, ArrowRight } from "lucide-react";
import { currentUser } from "@/mocks/seed";
import { Link } from "@tanstack/react-router";

export function GreetingHero() {
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
  const first = currentUser.name.split(" ")[0];

  return (
    <Card className="flex flex-col gap-6 p-6 sm:p-8 sm:flex-row sm:items-center sm:justify-between rounded-xl bg-card border-border/60">
      <div className="min-w-0 flex-1">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">
          {greeting}, {first}
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Here's what's happening with your projects today.
        </p>
        <div className="mt-5 flex items-center gap-4">
          <Link
            to="/projects"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-primary hover:text-primary/80 transition-colors"
          >
            View active projects <ArrowRight size={14} />
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 sm:w-auto shrink-0">
        <MiniStat
          icon={<TrendingUp size={14} />}
          label="Project Progress"
          value="75%"
          progress={75}
        />
        <MiniStat icon={<Flame size={14} />} label="Contribution Streak" value="12 days" />
        <MiniStat icon={<Sparkles size={14} />} label="AI Score" value="96" suffix="/100" />
      </div>
    </Card>
  );
}

function MiniStat({
  icon,
  label,
  value,
  suffix,
  progress,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  suffix?: string;
  progress?: number;
}) {
  return (
    <div className="flex flex-col justify-between gap-2 rounded-lg border border-border/50 bg-muted/20 p-4 sm:min-w-[150px]">
      <div className="flex items-center gap-2 text-muted-foreground">
        {icon}
        <p className="text-[11px] font-medium uppercase tracking-wider">{label}</p>
      </div>
      <div>
        <p className="text-2xl font-semibold tracking-tight text-foreground">
          {value}
          {suffix && (
            <span className="text-sm font-medium text-muted-foreground ml-0.5">{suffix}</span>
          )}
        </p>
        {progress !== undefined && (
          <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-muted/50">
            <div
              className="h-full rounded-full bg-primary transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
