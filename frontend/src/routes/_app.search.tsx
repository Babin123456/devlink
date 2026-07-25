import { createFileRoute, Link, useSearch } from "@tanstack/react-router";
import { Card, TagChip, Avatar, NoSearchResultsEmptyState } from "@/components/shared/primitives";
import { builders, projects, flares } from "@/mocks/seed";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Search, X } from "lucide-react";
import { SkillSuggestionDropdown } from "@/components/search/SkillSuggestionDropdown";

const tabs = ["Developers", "Projects", "Skills", "Flares"] as const;
type Tab = (typeof tabs)[number];

interface SearchParams {
  q?: string;
  tab?: Tab;
}

export const Route = createFileRoute("/_app/search")({
  validateSearch: (search: Record<string, unknown>): SearchParams => ({
    q: typeof search.q === "string" ? search.q : undefined,
    tab:
      typeof search.tab === "string" && tabs.includes(search.tab as Tab)
        ? (search.tab as Tab)
        : undefined,
  }),
  head: () => ({
    meta: [
      { title: "Search — DevLink" },
      {
        name: "description",
        content: "Global search across developers, projects, skills and flares.",
      },
    ],
  }),
  component: SearchPage,
});

function SearchPage() {
  const searchParams = useSearch({ from: "/_app/search" }) as SearchParams;
  const [q, setQ] = useState(searchParams.q || "");
  const [tab, setTab] = useState<Tab>(searchParams.tab || "Developers");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  useEffect(() => {
    if (searchParams.q !== undefined) {
      setQ(searchParams.q);
    }
    if (searchParams.tab !== undefined) {
      setTab(searchParams.tab);
    }
  }, [searchParams.q, searchParams.tab]);

  const handleSelectSkill = (skillName: string) => {
    setQ(skillName);
    setTab("Skills");
    setIsDropdownOpen(false);
  };

  const devs = builders.filter((b) =>
    (b.name + b.skills.join(" ")).toLowerCase().includes(q.toLowerCase()),
  );
  const projs = projects.filter((p) =>
    (p.name + p.stack.join(" ")).toLowerCase().includes(q.toLowerCase()),
  );
  const skillSet = Array.from(new Set(builders.flatMap((b) => b.skills))).filter((s) =>
    s.toLowerCase().includes(q.toLowerCase()),
  );
  const fls = flares.filter((f) => f.content.toLowerCase().includes(q.toLowerCase()));

  return (
    <div className="space-y-4">
      <div className="relative">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground z-10"
        />

        <input
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setIsDropdownOpen(true);
          }}
          onFocus={() => setIsDropdownOpen(true)}
          placeholder="Search DevLink…"
          className="w-full rounded-md border border-border bg-surface py-2.5 pl-10 pr-10 text-[14px] outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
          autoFocus
        />

        {q && (
          <button
            type="button"
            onClick={() => setQ("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground z-10"
            aria-label="Clear search"
          >
            <X size={16} />
          </button>
        )}

        <SkillSuggestionDropdown
          query={q}
          isOpen={isDropdownOpen}
          onSelectSkill={handleSelectSkill}
          onClose={() => setIsDropdownOpen(false)}
        />
      </div>

      <div className="flex items-center gap-1 rounded-md border border-border bg-surface p-0.5">
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={cn(
              "rounded px-3 py-1.5 text-[12px] font-medium transition-colors",
              tab === t
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Developers" &&
        (devs.length === 0 ? (
          <Card className="py-8">
            <NoSearchResultsEmptyState
              title="No developers found"
              desc={
                q
                  ? `No developers matching "${q}" were found.`
                  : "Search for developers by name or skill."
              }
              action={
                q ? (
                  <button
                    onClick={() => setQ("")}
                    className="rounded-md border border-border bg-surface px-3 py-1.5 text-[12px] font-medium text-foreground hover:bg-muted"
                  >
                    Clear search
                  </button>
                ) : undefined
              }
            />
          </Card>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {devs.map((b) => (
              <Link key={b.id} to="/builders/$builderId" params={{ builderId: b.id }}>
                <Card interactive className="flex items-center gap-3 p-3">
                  <Avatar src={b.avatar} alt={b.name} size={40} />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-[13px] font-semibold text-foreground">{b.name}</p>
                    <p className="truncate text-[12px] text-muted-foreground">{b.role}</p>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        ))}

      {tab === "Projects" &&
        (projs.length === 0 ? (
          <Card className="py-8">
            <NoSearchResultsEmptyState
              title="No projects found"
              desc={
                q
                  ? `No projects matching "${q}" were found.`
                  : "Search for projects by name or stack."
              }
              action={
                q ? (
                  <button
                    onClick={() => setQ("")}
                    className="rounded-md border border-border bg-surface px-3 py-1.5 text-[12px] font-medium text-foreground hover:bg-muted"
                  >
                    Clear search
                  </button>
                ) : undefined
              }
            />
          </Card>
        ) : (
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {projs.map((p) => (
              <Link key={p.id} to="/projects/$projectId" params={{ projectId: p.id }}>
                <Card interactive className="p-4">
                  <div className="flex items-start gap-3">
                    <span className="grid h-10 w-10 place-items-center rounded-md bg-muted text-xl">
                      {p.icon}
                    </span>
                    <div className="min-w-0">
                      <p className="truncate text-[13px] font-semibold text-foreground">{p.name}</p>
                      <p className="truncate text-[12px] text-muted-foreground">
                        {p.stack.join(" · ")}
                      </p>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        ))}

      {tab === "Skills" &&
        (skillSet.length === 0 ? (
          <Card className="py-8">
            <NoSearchResultsEmptyState
              title="No skills found"
              desc={
                q
                  ? `No skills matching "${q}" were found.`
                  : "Search for specific developer skills."
              }
              action={
                q ? (
                  <button
                    onClick={() => setQ("")}
                    className="rounded-md border border-border bg-surface px-3 py-1.5 text-[12px] font-medium text-foreground hover:bg-muted"
                  >
                    Clear search
                  </button>
                ) : undefined
              }
            />
          </Card>
        ) : (
          <Card className="p-4">
            <div className="flex flex-wrap gap-2">
              {skillSet.map((s) => (
                <TagChip key={s} className="text-[12px]">
                  {s}
                </TagChip>
              ))}
            </div>
          </Card>
        ))}

      {tab === "Flares" &&
        (fls.length === 0 ? (
          <Card className="py-8">
            <NoSearchResultsEmptyState
              title="No flares found"
              desc={
                q
                  ? `No community flares matching "${q}" were found.`
                  : "Search community announcements and updates."
              }
              action={
                q ? (
                  <button
                    onClick={() => setQ("")}
                    className="rounded-md border border-border bg-surface px-3 py-1.5 text-[12px] font-medium text-foreground hover:bg-muted"
                  >
                    Clear search
                  </button>
                ) : undefined
              }
            />
          </Card>
        ) : (
          <div className="space-y-3">
            {fls.map((f) => (
              <Card key={f.id} className="p-4">
                <p className="text-[13px] font-semibold text-foreground">{f.author.name}</p>
                <p className="mt-1 text-[13px] text-foreground">{f.content}</p>
              </Card>
            ))}
          </div>
        ))}
    </div>
  );
}
