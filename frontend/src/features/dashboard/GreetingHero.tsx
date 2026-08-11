import { Card } from "@/components/shared/primitives";
import {
  Folder,
  Users2,
  Calendar,
  ArrowRight,
  Plus,
  TrendingUp,
  Flame,
  Sparkles,
} from "lucide-react";
import { currentUser } from "@/mocks/seed";
import { Link } from "@tanstack/react-router";

export function GreetingHero() {
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
  const first = currentUser.name.split(" ")[0];

  return (
    <Card className="flex flex-col gap-6 p-6 sm:flex-row sm:items-center sm:justify-between rounded-2xl bg-card border-border/60 shadow-sm relative overflow-hidden">
      <div className="min-w-0 flex-1 flex flex-col gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            {greeting}, {first}! 👋
          </h1>
          <p className="mt-1 text-[15px] text-muted-foreground">
            Here's what's happening with your workspace today.
          </p>
        </div>

        {/* Inline Stats Badges Row */}
        <div className="flex flex-wrap gap-3">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl border border-border bg-surface text-xs font-semibold text-foreground shadow-2xs">
            <Folder size={14} className="text-primary" />
            <span>2 Active Projects</span>
          </div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl border border-border bg-surface text-xs font-semibold text-foreground shadow-2xs">
            <Users2 size={14} className="text-emerald-500" />
            <span>3 Pending Invites</span>
          </div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl border border-border bg-surface text-xs font-semibold text-foreground shadow-2xs">
            <Calendar size={14} className="text-violet-500" />
            <span>5 Tasks Due</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-3">
          <Link
            to="/projects"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground shadow-[0_4px_12px_rgba(5,183,215,0.25)] transition-all duration-300 hover:bg-primary/95 hover:shadow-[0_6px_20px_rgba(5,183,215,0.4)] hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] cursor-pointer"
          >
            Continue Working <ArrowRight size={14} />
          </Link>
          <Link
            to="/projects"
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-border bg-surface px-5 py-2.5 text-sm font-semibold text-foreground transition-all duration-300 hover:bg-muted hover:border-foreground/10 hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] cursor-pointer"
          >
            Create Project <Plus size={14} />
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 sm:flex sm:w-auto sm:flex-row sm:shrink-0">
        <MiniStat icon={<TrendingUp size={14} />} label="Progress" value="75%" progress={75} />
        <MiniStat icon={<Flame size={14} />} label="Streak" value="12d" />
        <MiniStat icon={<Sparkles size={14} />} label="AI Score" value="96" />
      </div>

      {/* SVG Laptop/Plant Illustration */}
      <svg
        width="180"
        height="130"
        viewBox="0 0 180 130"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="shrink-0 hidden md:block select-none"
      >
        {/* Laptop screen background */}
        <rect
          x="25"
          y="15"
          width="130"
          height="85"
          rx="6"
          fill="#F8FAFC"
          stroke="#E2E8F0"
          strokeWidth="2"
        />
        {/* Screen Content - Code lines */}
        <rect x="35" y="27" width="50" height="4" rx="2" fill="#05B7D7" />
        <rect x="35" y="37" width="70" height="4" rx="2" fill="#94A3B8" />
        <rect x="35" y="47" width="40" height="4" rx="2" fill="#94A3B8" />
        <rect x="35" y="57" width="60" height="4" rx="2" fill="#05B7D7" />

        {/* Small floating UI card on screen */}
        <rect
          x="90"
          y="40"
          width="55"
          height="45"
          rx="4"
          fill="white"
          stroke="#CBD5E1"
          strokeWidth="1.5"
        />
        <circle cx="102" cy="52" r="5" fill="#05B7D7" />
        <rect x="112" y="49" width="25" height="3" rx="1.5" fill="#64748B" />
        <rect x="112" y="55" width="18" height="2.5" rx="1" fill="#94A3B8" />

        {/* Laptop Base */}
        <path
          d="M10 102C10 100.895 10.8954 100 12 100H168C169.105 100 170 100.895 170 102V105C170 106.105 169.105 107 168 107H12C10.8954 107 10 106.105 10 105V102Z"
          fill="#CBD5E1"
        />
        {/* Trackpad notch */}
        <path
          d="M75 100H105V102C105 103.105 104.105 104 103 104H77C75.8954 104 75 103.105 75 102V100Z"
          fill="#94A3B8"
        />

        {/* Desk Surface line */}
        <line
          x1="5"
          y1="120"
          x2="175"
          y2="120"
          stroke="#E2E8F0"
          strokeWidth="2"
          strokeLinecap="round"
        />

        {/* Plant Pot */}
        <path
          d="M152 120L150 110H162L160 120H152Z"
          fill="#E2E8F0"
          stroke="#CBD5E1"
          strokeWidth="1.5"
        />
        {/* Leaves */}
        <path d="M156 110C156 102 153 96 150 94C153 96 156 102 156 110Z" fill="#10B981" />
        <path d="M156 110C156 100 162 94 165 92C162 94 156 100 156 110Z" fill="#10B981" />
        <path d="M156 110C152 108 147 106 145 102C147 106 152 108 156 110Z" fill="#10B981" />
      </svg>
    </Card>
  );
}

function MiniStat({
  icon,
  label,
  value,
  progress,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  progress?: number;
}) {
  return (
    <div className="flex flex-col justify-between gap-1.5 rounded-xl border border-border/50 bg-muted/20 p-3 sm:min-w-[130px] sm:shrink-0">
      <div className="flex items-center gap-1.5 text-muted-foreground">
        {icon}
        <p className="text-[10px] font-medium uppercase tracking-wider truncate">{label}</p>
      </div>
      <div>
        <p className="text-lg font-semibold tracking-tight text-foreground">{value}</p>
        {progress !== undefined && (
          <div className="mt-1.5 h-1 w-full overflow-hidden rounded-full bg-muted/50">
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
