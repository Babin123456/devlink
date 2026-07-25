import { createFileRoute, Outlet, useNavigate } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { projectsService } from "@/services";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Card, TagChip } from "@/components/shared/primitives";
import { Star, GitFork, Users2, Plus, Search, X } from "lucide-react";
import { useEffect, useState } from "react";
import { CreateProjectDialog } from "@/components/projects/CreateProjectDialog";
import { cn } from "@/lib/utils";
import { getRecentlyViewedProjectIds } from "@/lib/recentlyViewedProjects";
import { ProjectFilters } from "@/components/projects/ProjectFilters";

type ProjectsSearch = {
  page?: number;
  q?: string;
  language?: string;
  experience?: string;
  remote?: string;
  paid?: string;
  opensource?: string;
  tech?: string;
};

export const Route = createFileRoute("/_app/projects")({
  validateSearch: (search: Record<string, unknown>): ProjectsSearch => {
    return {
      page: search.page ? Number(search.page) : 1,
      q: search.q as string | undefined,
      language: search.language as string | undefined,
      experience: search.experience as string | undefined,
      remote: search.remote as string | undefined,
      paid: search.paid as string | undefined,
      opensource: search.opensource as string | undefined,
      tech: search.tech as string | undefined,
    };
  },
  head: () => ({
    meta: [
      { title: "Projects — DevLink" },
      { name: "description", content: "Browse and manage your DevLink projects." },
    ],
  }),
  component: ProjectsPage,
});

function ProjectsPage() {
  const search = Route.useSearch();
  const page = search.page || 1;
  const navigate = useNavigate({ from: "/projects" });
  const ITEMS_PER_PAGE = 6;
  
  const [createOpen, setCreateOpen] = useState(false);
  const [recentProjectIds, setRecentProjectIds] = useState<string[]>([]);
  
  // Use local state for q so we can type without lagging the URL update
  const [q, setQ] = useState(search.q || "");

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      navigate({
        search: (prev: any) => ({ ...prev, q: q || undefined }),
        replace: true,
      });
    }, 300);
    return () => clearTimeout(timeoutId);
  }, [q, navigate]);

  useEffect(() => {
    setRecentProjectIds(getRecentlyViewedProjectIds());
  }, []);

  // Pass API-supported params
  const { data = [], isLoading } = useQuery({
    queryKey: ["projects", search],
    queryFn: () => projectsService.list(search as any),
  });

  const recentlyViewed = recentProjectIds
    .map((id) => data.find((project) => project.id === id))
    .filter((project): project is NonNullable<typeof project> => Boolean(project));

  // Local filter for search text (q) if backend doesn't support 'q' param natively for projects list yet
  const filtered = data.filter((p) => {
    if (q && !p.name?.toLowerCase().includes(q.toLowerCase()) && !p.title?.toLowerCase().includes(q.toLowerCase())) return false;
    return true;
  });

  const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
  const paginated = filtered.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  const resetFilters = () => {
    setQ("");
    navigate({
      search: () => ({}),
      replace: true,
    });
  };

  const hasActiveFilters = Object.keys(search).filter(k => k !== 'page').length > 0 || q !== "";

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-[22px] font-bold tracking-tight text-foreground">Projects</h1>
          <p className="text-[13px] text-muted-foreground">
            Everything you're building, in one place.
          </p>
        </div>
        <button
          onClick={() => setCreateOpen(true)}
          className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-2 text-[13px] font-semibold text-primary-foreground hover:opacity-90"
        >
          <Plus size={14} /> New project
        </button>
        <CreateProjectDialog open={createOpen} onOpenChange={setCreateOpen} />
      </div>

      {recentlyViewed.length > 0 && (
        <section className="space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="text-[15px] font-semibold text-foreground">Recently Viewed Projects</h2>
            <span className="text-[11px] text-muted-foreground">Your latest project visits</span>
          </div>

          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {recentlyViewed.map((project) => (
              <a key={project.id} href={`/projects/${project.id}`} className="block">
                <Card interactive className="p-4">
                  <div className="flex items-start gap-3">
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-muted text-xl">
                      {project.icon}
                    </span>

                    <div className="min-w-0 flex-1">
                      <p className="truncate text-[14px] font-semibold text-foreground">
                        {project.name || project.title}
                      </p>
                      <p className="mt-0.5 line-clamp-2 text-[12px] text-muted-foreground">
                        {project.description}
                      </p>
                    </div>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-1">
                    {(project.stack || []).slice(0, 3).map((tech: string) => (
                      <TagChip key={tech}>{tech}</TagChip>
                    ))}
                  </div>
                </Card>
              </a>
            ))}
          </div>
        </section>
      )}

      {/* Advanced Filters */}
      <ProjectFilters />

      <Card className="p-4">
        <div className="flex flex-wrap items-center gap-2">
          <div className="relative min-w-0 flex-1">
            <Search
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
            />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search projects..."
              className="w-full rounded-md border border-border bg-surface py-[7px] pl-9 pr-3 text-[13px] outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>
      </Card>

      {isLoading ? (
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i} className="h-40 animate-pulse" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="mb-3 grid h-12 w-12 place-items-center rounded-full bg-muted text-muted-foreground">
            🔍
          </div>
          <p className="text-[14px] font-semibold text-foreground">
            No projects match your filters
          </p>
          <p className="mt-1 text-[13px] text-muted-foreground">
            Try adjusting or resetting your filters.
          </p>
          {hasActiveFilters && (
            <button
              onClick={resetFilters}
              className="mt-3 text-[13px] font-medium text-primary hover:underline inline-flex items-center gap-1"
            >
              <X size={13} /> Reset filters
            </button>
          )}
        </div>
      ) : (
        <>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {paginated.map((p) => (
              <a key={p.id} href={`/projects/${p.id}`} className="block">
                <Card interactive className="p-4">
                  <div className="flex items-start gap-3">
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-muted text-xl">
                      {p.icon || '🚀'}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-[14px] font-semibold text-foreground">{p.name || p.title}</p>
                      <p className="mt-0.5 line-clamp-2 text-[12px] text-muted-foreground">
                        {p.description}
                      </p>
                    </div>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-1">
                    {(p.stack || []).map((s: string) => (
                      <TagChip key={s}>{s}</TagChip>
                    ))}
                    {p.difficulty && (
                      <TagChip
                        className={cn(
                          p.difficulty === "beginner"
                            ? "border-success/30 bg-success/10 text-success"
                            : p.difficulty === "intermediate"
                              ? "border-warning/30 bg-warning/10 text-warning"
                              : "border-destructive/30 bg-destructive/10 text-destructive",
                        )}
                      >
                        {p.difficulty}
                      </TagChip>
                    )}
                  </div>
                  <div className="mt-3">
                    <div className="mb-1 flex items-center justify-between text-[11px] text-muted-foreground">
                      <span>Progress</span>
                      <span>{p.progress || 0}%</span>
                    </div>
                    <div className="h-1 overflow-hidden rounded-full bg-muted">
                      <div className="h-full bg-primary" style={{ width: `${p.progress || 0}%` }} />
                    </div>
                  </div>
                  <div className="mt-3 flex items-center justify-between text-[11px] text-muted-foreground">
                    <span className="inline-flex items-center gap-1">
                      <Users2 size={12} /> {p.members || p.team_size || 1}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <Star size={12} /> {p.stars || 0}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <GitFork size={12} /> {p.forks || 0}
                    </span>
                    <span
                      className={`rounded-md px-1.5 py-0.5 text-[10px] font-semibold uppercase ${
                        p.status === "active" || p.status === "completed"
                          ? "bg-success/10 text-success"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {p.status || "IDEA"}
                    </span>
                  </div>
                </Card>
              </a>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="mt-8 flex justify-center">
               <Pagination>
                 <PaginationContent>
                   <PaginationItem>
                     <PaginationPrevious
                       href={`/projects?page=${Math.max(1, page - 1)}`}
                       aria-disabled={page === 1}
                       className={page === 1 ? "pointer-events-none opacity-50" : ""}
                     />
                   </PaginationItem>
                   {Array.from({ length: totalPages }).map((_, i) => (
                     <PaginationItem key={i}>
                       <PaginationLink
                         href={`/projects?page=${i + 1}`}
                         isActive={page === i + 1}
                       >
                         {i + 1}
                       </PaginationLink>
                     </PaginationItem>
                   ))}
                   <PaginationItem>
                     <PaginationNext
                       href={`/projects?page=${Math.min(totalPages, page + 1)}`}
                       aria-disabled={page === totalPages}
                       className={page === totalPages ? "pointer-events-none opacity-50" : ""}
                     />
                   </PaginationItem>
                 </PaginationContent>
               </Pagination>
            </div>
          )}
        </>
      )}
    </div>
  );
}
