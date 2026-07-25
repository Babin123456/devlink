import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  Search,
  X,
  Loader2,
  AlertCircle,
  Building2,
  Hash,
  Code2,
  Users,
  FolderKanban,
  CornerDownLeft,
  ArrowUp,
  ArrowDown,
  Sparkles,
} from "lucide-react";

import { Avatar, Card, NoSearchResultsEmptyState, TagChip } from "@/components/shared/primitives";
import { HighlightText } from "@/components/shared/HighlightText";
import { useGlobalSearch } from "@/hooks/useGlobalSearch";
import { cn } from "@/lib/utils";
import { isBackendConfigured } from "@/api/client";
import {
  SEARCH_CATEGORIES,
  type SearchCategory,
  type SearchSuggestionOrganization,
  type SearchSuggestionProject,
  type SearchSuggestionSkill,
  type SearchSuggestionTag,
  type SearchSuggestionUser,
  type SearchResultOrganization,
  type SearchResultProject,
  type SearchResultSkill,
  type SearchResultTag,
  type SearchResultUser,
} from "@/api/modules/search";

export const Route = createFileRoute("/_app/search")({
  head: () => ({
    meta: [
      { title: "Search — DevLink" },
      {
        name: "description",
        content: "Global search across developers, projects, organizations, skills and tags.",
      },
    ],
  }),
  component: SearchPage,
});

// ---------------------------------------------------------------------
// Category config
// ---------------------------------------------------------------------

interface CategoryConfig {
  label: string;
  icon: typeof Users;
  countKey: keyof SearchCountsLike;
}

type SearchCountsLike = {
  developers: number;
  projects: number;
  organizations: number;
  skills: number;
  tags: number;
  total: number;
};

const CATEGORY_CONFIG: Record<SearchCategory, CategoryConfig> = {
  developers: { label: "Developers", icon: Users, countKey: "developers" },
  projects: { label: "Projects", icon: FolderKanban, countKey: "projects" },
  organizations: { label: "Organizations", icon: Building2, countKey: "organizations" },
  skills: { label: "Skills", icon: Code2, countKey: "skills" },
  tags: { label: "Tags", icon: Hash, countKey: "tags" },
};

// ---------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------

function SearchPage() {
  const {
    query,
    debouncedQuery,
    category,
    loading,
    error,
    suggestions,
    results,
    setQuery,
    setCategory,
    clear,
  } = useGlobalSearch({ debounceMs: 250, limit: 20, enableAutocomplete: true });

  // Keyboard navigation state — index into the flat list of suggestion rows.
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Flatten the autocomplete suggestions into a single keyboard-navigable list.
  const flatSuggestions = useMemo(() => {
    if (!suggestions) return [] as FlatSuggestion[];
    const out: FlatSuggestion[] = [];
    suggestions.users.forEach((u) =>
      out.push({ kind: "user", id: u.id, label: u.name, sublabel: `@${u.username}`, data: u }),
    );
    suggestions.projects.forEach((p) =>
      out.push({ kind: "project", id: p.id, label: p.title, sublabel: p.tagline ?? "", data: p }),
    );
    suggestions.organizations.forEach((o) =>
      out.push({
        kind: "organization",
        id: o.id,
        label: o.name,
        sublabel: o.organization_type ?? "",
        data: o,
      }),
    );
    suggestions.skills.forEach((s) =>
      out.push({ kind: "skill", id: s.id, label: s.name, sublabel: s.category ?? "", data: s }),
    );
    suggestions.tags.forEach((t) =>
      out.push({
        kind: "tag",
        id: t.name,
        label: t.name,
        sublabel: `${t.project_count} project${t.project_count === 1 ? "" : "s"}`,
        data: t,
      }),
    );
    return out;
  }, [suggestions]);

  // Reset active index whenever the suggestion list changes.
  useEffect(() => {
    setActiveIndex(-1);
  }, [flatSuggestions.length]);

  const showSuggestions =
    debouncedQuery.trim().length > 0 &&
    suggestions !== null &&
    flatSuggestions.length > 0 &&
    // Hide the dropdown while the user has already pressed Enter / a category is selected
    !category;

  const counts = results?.counts ?? null;
  const trimmedQuery = query.trim();

  // -------------------------------------------------------------------
  // Keyboard navigation
  // -------------------------------------------------------------------

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((i) => Math.min(i + 1, flatSuggestions.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      if (activeIndex >= 0 && activeIndex < flatSuggestions.length) {
        e.preventDefault();
        const picked = flatSuggestions[activeIndex];
        navigateToSuggestion(picked);
      }
    } else if (e.key === "Escape") {
      if (query) {
        e.preventDefault();
        clear();
        inputRef.current?.focus();
      }
    }
  };

  const navigateToSuggestion = (s: FlatSuggestion) => {
    // Use TanStack Router navigation by pushing the destination.
    switch (s.kind) {
      case "user":
        window.location.href = `/builders/${s.id}`;
        break;
      case "project":
        window.location.href = `/projects/${s.id}`;
        break;
      case "organization":
        window.location.href = `/organizations/${s.id}`;
        break;
      case "skill":
      case "tag":
        // Skills/tags have no dedicated page — drop into the query and run a full search.
        setQuery(s.label);
        inputRef.current?.focus();
        break;
    }
  };

  // -------------------------------------------------------------------
  // Render
  // -------------------------------------------------------------------

  const backendConfigured = isBackendConfigured();

  return (
    <div className="space-y-4" ref={containerRef}>
      {/* Search input */}
      <div className="relative">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
        />
        <input
          ref={inputRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search DevLink… (developers, projects, orgs, skills, tags)"
          className="w-full rounded-md border border-border bg-surface py-2.5 pl-10 pr-10 text-[14px] outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
          autoFocus
          aria-label="Global search"
          aria-autocomplete="list"
          aria-expanded={showSuggestions}
          aria-controls="search-suggestions-list"
        />
        {loading && (
          <Loader2
            size={16}
            className="absolute right-10 top-1/2 -translate-y-1/2 animate-spin text-muted-foreground"
            aria-label="Searching"
          />
        )}
        {query && !loading && (
          <button
            type="button"
            onClick={() => {
              clear();
              inputRef.current?.focus();
            }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            aria-label="Clear search"
          >
            <X size={16} />
          </button>
        )}

        {/* Autocomplete dropdown */}
        {showSuggestions && (
          <div
            id="search-suggestions-list"
            role="listbox"
            className="absolute left-0 right-0 top-full z-30 mt-1 overflow-hidden rounded-md border border-border bg-popover shadow-lg"
          >
            {flatSuggestions.map((s, i) => (
              <button
                key={`${s.kind}-${s.id}`}
                type="button"
                role="option"
                aria-selected={i === activeIndex}
                onMouseEnter={() => setActiveIndex(i)}
                onClick={() => navigateToSuggestion(s)}
                className={cn(
                  "flex w-full items-center gap-3 px-3 py-2 text-left text-[13px] transition-colors",
                  i === activeIndex ? "bg-muted" : "hover:bg-muted/60",
                )}
              >
                <SuggestionIcon kind={s.kind} />
                <div className="min-w-0 flex-1">
                  <p className="truncate font-medium text-foreground">
                    <HighlightText text={s.label} query={debouncedQuery} />
                  </p>
                  {s.sublabel && (
                    <p className="truncate text-[12px] text-muted-foreground">{s.sublabel}</p>
                  )}
                </div>
              </button>
            ))}
            <div className="flex items-center justify-between border-t border-border bg-surface/50 px-3 py-1.5 text-[11px] text-muted-foreground">
              <span className="flex items-center gap-1.5">
                <kbd className="rounded border border-border bg-card px-1 py-0.5 text-[10px]">
                  <ArrowUp size={10} className="inline" />
                </kbd>
                <kbd className="rounded border border-border bg-card px-1 py-0.5 text-[10px]">
                  <ArrowDown size={10} className="inline" />
                </kbd>
                to navigate
              </span>
              <span className="flex items-center gap-1.5">
                <kbd className="rounded border border-border bg-card px-1 py-0.5 text-[10px]">
                  <CornerDownLeft size={10} className="inline" />
                </kbd>
                to select
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Backend not configured banner */}
      {!backendConfigured && (
        <Card className="flex items-start gap-3 border-warning/30 bg-warning/5 p-3">
          <AlertCircle size={16} className="mt-0.5 shrink-0 text-warning" />
          <p className="text-[12px] text-muted-foreground">
            The backend API is not configured — search will return empty results. Set{" "}
            <code className="rounded bg-muted px-1 py-0.5 text-[11px]">VITE_API_BASE_URL</code> in
            your environment to enable global search.
          </p>
        </Card>
      )}

      {/* Error banner */}
      {error && (
        <Card className="flex items-start gap-3 border-destructive/30 bg-destructive/5 p-3">
          <AlertCircle size={16} className="mt-0.5 shrink-0 text-destructive" />
          <div className="flex-1">
            <p className="text-[13px] font-medium text-foreground">Search failed</p>
            <p className="mt-0.5 text-[12px] text-muted-foreground">{error}</p>
          </div>
          <button
            type="button"
            onClick={() => setQuery(query)}
            className="rounded-md border border-border bg-surface px-2.5 py-1 text-[12px] font-medium text-foreground hover:bg-muted"
          >
            Retry
          </button>
        </Card>
      )}

      {/* Category filter tabs */}
      <div className="flex flex-wrap items-center gap-1 rounded-md border border-border bg-surface p-0.5">
        <CategoryTab
          label="All"
          icon={Sparkles}
          active={category === null}
          count={counts?.total ?? 0}
          loading={loading}
          onClick={() => setCategory(null)}
        />
        {SEARCH_CATEGORIES.map((cat) => {
          const cfg = CATEGORY_CONFIG[cat];
          return (
            <CategoryTab
              key={cat}
              label={cfg.label}
              icon={cfg.icon}
              active={category === cat}
              count={counts ? counts[cfg.countKey] : 0}
              loading={loading}
              onClick={() => setCategory(cat)}
            />
          );
        })}
      </div>

      {/* Body: results / empty states / loading skeletons */}
      <SearchBody
        query={trimmedQuery}
        debouncedQuery={debouncedQuery.trim()}
        loading={loading}
        results={results}
        category={category}
        onClear={clear}
      />
    </div>
  );
}

// ---------------------------------------------------------------------
// Category tab
// ---------------------------------------------------------------------

function CategoryTab({
  label,
  icon: Icon,
  active,
  count,
  loading,
  onClick,
}: {
  label: string;
  icon: typeof Users;
  active: boolean;
  count: number;
  loading: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "flex items-center gap-1.5 rounded px-3 py-1.5 text-[12px] font-medium transition-colors",
        active
          ? "bg-primary text-primary-foreground"
          : "text-muted-foreground hover:text-foreground",
      )}
    >
      <Icon size={13} />
      {label}
      <span
        className={cn(
          "ml-0.5 rounded-full px-1.5 py-0.5 text-[10px] font-semibold",
          active ? "bg-primary-foreground/20" : "bg-muted text-muted-foreground",
        )}
      >
        {loading ? "…" : count}
      </span>
    </button>
  );
}

// ---------------------------------------------------------------------
// Suggestion icon
// ---------------------------------------------------------------------

type FlatSuggestion =
  | { kind: "user"; id: string; label: string; sublabel: string; data: SearchSuggestionUser }
  | { kind: "project"; id: string; label: string; sublabel: string; data: SearchSuggestionProject }
  | {
      kind: "organization";
      id: string;
      label: string;
      sublabel: string;
      data: SearchSuggestionOrganization;
    }
  | { kind: "skill"; id: string; label: string; sublabel: string; data: SearchSuggestionSkill }
  | { kind: "tag"; id: string; label: string; sublabel: string; data: SearchSuggestionTag };

function SuggestionIcon({ kind }: { kind: FlatSuggestion["kind"] }) {
  const map = {
    user: Users,
    project: FolderKanban,
    organization: Building2,
    skill: Code2,
    tag: Hash,
  } as const;
  const Icon = map[kind];
  return (
    <span className="grid h-7 w-7 shrink-0 place-items-center rounded-md bg-muted text-muted-foreground">
      <Icon size={14} />
    </span>
  );
}

// ---------------------------------------------------------------------
// Search body — handles loading / empty / results states
// ---------------------------------------------------------------------

function SearchBody({
  query,
  debouncedQuery,
  loading,
  results,
  category,
  onClear,
}: {
  query: string;
  debouncedQuery: string;
  loading: boolean;
  results: ReturnType<typeof useGlobalSearch>["results"];
  category: SearchCategory | null;
  onClear: () => void;
}) {
  // Idle (no query) state.
  if (!query) {
    return (
      <Card className="py-10">
        <NoSearchResultsEmptyState
          title="Search DevLink"
          desc="Find developers, projects, organizations, skills and tags across the entire platform."
        />
      </Card>
    );
  }

  // Loading skeleton.
  if (loading && !results) {
    return <SearchSkeleton />;
  }

  // No results at all.
  if (results && results.counts.total === 0) {
    return (
      <Card className="py-8">
        <NoSearchResultsEmptyState
          title="No results found"
          desc={`No matches for "${query}". Try different keywords or clear your search.`}
          action={
            <button
              onClick={onClear}
              className="rounded-md border border-border bg-surface px-3 py-1.5 text-[12px] font-medium text-foreground hover:bg-muted"
            >
              Clear search
            </button>
          }
        />
      </Card>
    );
  }

  if (!results) {
    return null;
  }

  // Compose visible sections based on category filter.
  const showAll = category === null;
  const sections: React.ReactNode[] = [];

  if (showAll || category === "developers") {
    sections.push(
      <DevelopersSection
        key="developers"
        users={results.users}
        query={debouncedQuery}
        showAll={showAll}
      />,
    );
  }
  if (showAll || category === "projects") {
    sections.push(
      <ProjectsSection
        key="projects"
        projects={results.projects}
        query={debouncedQuery}
        showAll={showAll}
      />,
    );
  }
  if (showAll || category === "organizations") {
    sections.push(
      <OrganizationsSection
        key="organizations"
        organizations={results.organizations}
        query={debouncedQuery}
        showAll={showAll}
      />,
    );
  }
  if (showAll || category === "skills") {
    sections.push(
      <SkillsSection
        key="skills"
        skills={results.skills}
        query={debouncedQuery}
        showAll={showAll}
      />,
    );
  }
  if (showAll || category === "tags") {
    sections.push(
      <TagsSection key="tags" tags={results.tags} query={debouncedQuery} showAll={showAll} />,
    );
  }

  return <div className="space-y-4">{sections}</div>;
}

// ---------------------------------------------------------------------
// Per-category sections
// ---------------------------------------------------------------------

function SectionHeader({
  title,
  count,
  onSeeAll,
}: {
  title: string;
  count: number;
  onSeeAll?: () => void;
}) {
  return (
    <div className="flex items-center justify-between">
      <h2 className="text-[14px] font-semibold text-foreground">
        {title} <span className="text-muted-foreground">({count})</span>
      </h2>
      {onSeeAll && (
        <button
          type="button"
          onClick={onSeeAll}
          className="text-[12px] font-medium text-primary hover:underline"
        >
          See all
        </button>
      )}
    </div>
  );
}

function DevelopersSection({
  users,
  query,
  showAll,
}: {
  users: SearchResultUser[];
  query: string;
  showAll: boolean;
}) {
  if (users.length === 0) return null;
  const visible = showAll ? users.slice(0, 6) : users;
  return (
    <div className="space-y-2">
      <SectionHeader title="Developers" count={users.length} />
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {visible.map((u) => (
          <Link key={u.id} to="/builders/$builderId" params={{ builderId: u.id }}>
            <Card interactive className="flex items-center gap-3 p-3">
              <Avatar src={u.profile_image ?? ""} alt={u.name} size={40} />
              <div className="min-w-0 flex-1">
                <p className="truncate text-[13px] font-semibold text-foreground">
                  <HighlightText text={u.name} query={query} />
                </p>
                <p className="truncate text-[12px] text-muted-foreground">
                  <HighlightText text={`@${u.username}`} query={query} />
                  {u.role && ` · ${u.role}`}
                </p>
                {u.headline && (
                  <p className="truncate text-[11px] text-muted-foreground">{u.headline}</p>
                )}
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}

function ProjectsSection({
  projects,
  query,
  showAll,
}: {
  projects: SearchResultProject[];
  query: string;
  showAll: boolean;
}) {
  if (projects.length === 0) return null;
  const visible = showAll ? projects.slice(0, 6) : projects;
  return (
    <div className="space-y-2">
      <SectionHeader title="Projects" count={projects.length} />
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {visible.map((p) => (
          <Link key={p.id} to="/projects/$projectId" params={{ projectId: p.id }}>
            <Card interactive className="p-4">
              <div className="flex items-start gap-3">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-muted text-xl">
                  {p.logo_url ? (
                    <img
                      src={p.logo_url}
                      alt=""
                      className="h-full w-full rounded-md object-cover"
                    />
                  ) : (
                    "🚀"
                  )}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-[13px] font-semibold text-foreground">
                    <HighlightText text={p.title} query={query} />
                  </p>
                  {p.tagline && (
                    <p className="truncate text-[12px] text-muted-foreground">
                      <HighlightText text={p.tagline} query={query} />
                    </p>
                  )}
                  {p.tags.length > 0 && (
                    <div className="mt-1.5 flex flex-wrap gap-1">
                      {p.tags.slice(0, 3).map((t) => (
                        <TagChip key={t} className="text-[11px]">
                          {t}
                        </TagChip>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}

function OrganizationsSection({
  organizations,
  query,
  showAll,
}: {
  organizations: SearchResultOrganization[];
  query: string;
  showAll: boolean;
}) {
  if (organizations.length === 0) return null;
  const visible = showAll ? organizations.slice(0, 6) : organizations;
  return (
    <div className="space-y-2">
      <SectionHeader title="Organizations" count={organizations.length} />
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {visible.map((o) => (
          <Link key={o.id} to="/organizations/$orgId" params={{ orgId: o.id }}>
            <Card interactive className="p-4">
              <div className="flex items-start gap-3">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-muted text-xl">
                  {o.logo_url ? (
                    <img
                      src={o.logo_url}
                      alt=""
                      className="h-full w-full rounded-md object-cover"
                    />
                  ) : (
                    <Building2 size={18} />
                  )}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="flex items-center gap-1.5 truncate text-[13px] font-semibold text-foreground">
                    <HighlightText text={o.name} query={query} />
                    {o.verified && (
                      <span className="rounded bg-primary/10 px-1 text-[10px] font-bold text-primary">
                        ✓
                      </span>
                    )}
                  </p>
                  <p className="truncate text-[12px] text-muted-foreground">
                    {o.organization_type && `${o.organization_type} · `}
                    {o.members_count} member{o.members_count === 1 ? "" : "s"}
                  </p>
                  {o.location && (
                    <p className="truncate text-[11px] text-muted-foreground">{o.location}</p>
                  )}
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}

function SkillsSection({
  skills,
  query,
  showAll,
}: {
  skills: SearchResultSkill[];
  query: string;
  showAll: boolean;
}) {
  if (skills.length === 0) return null;
  const visible = showAll ? skills.slice(0, 12) : skills;
  return (
    <div className="space-y-2">
      <SectionHeader title="Skills" count={skills.length} />
      <Card className="p-4">
        <div className="flex flex-wrap gap-2">
          {visible.map((s) => (
            <TagChip key={s.id} className="text-[12px]">
              <HighlightText text={s.name} query={query} />
              {s.category && (
                <span className="ml-1 text-[10px] text-muted-foreground">· {s.category}</span>
              )}
            </TagChip>
          ))}
        </div>
      </Card>
    </div>
  );
}

function TagsSection({
  tags,
  query,
  showAll,
}: {
  tags: SearchResultTag[];
  query: string;
  showAll: boolean;
}) {
  if (tags.length === 0) return null;
  const visible = showAll ? tags.slice(0, 12) : tags;
  return (
    <div className="space-y-2">
      <SectionHeader title="Tags" count={tags.length} />
      <Card className="p-4">
        <div className="flex flex-wrap gap-2">
          {visible.map((t) => (
            <TagChip key={t.name} className="text-[12px]">
              <Hash size={10} className="mr-0.5 inline" />
              <HighlightText text={t.name} query={query} />
              <span className="ml-1 text-[10px] text-muted-foreground">· {t.project_count}</span>
            </TagChip>
          ))}
        </div>
      </Card>
    </div>
  );
}

// ---------------------------------------------------------------------
// Loading skeleton
// ---------------------------------------------------------------------

function SearchSkeleton() {
  return (
    <div className="space-y-4">
      {[0, 1, 2].map((i) => (
        <div key={i} className="space-y-2">
          <div className="h-4 w-32 animate-pulse rounded bg-muted" />
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {[0, 1, 2].map((j) => (
              <Card key={j} className="p-4">
                <div className="flex items-start gap-3">
                  <div className="h-10 w-10 animate-pulse rounded-md bg-muted" />
                  <div className="flex-1 space-y-1.5">
                    <div className="h-3 w-3/4 animate-pulse rounded bg-muted" />
                    <div className="h-2.5 w-1/2 animate-pulse rounded bg-muted" />
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
