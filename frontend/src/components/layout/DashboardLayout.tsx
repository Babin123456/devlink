import { Outlet, useRouterState } from "@tanstack/react-router";
import { AnimatePresence, motion } from "framer-motion";
import { Sidebar } from "./Sidebar";
import { MobileSidebar } from "./MobileSidebar";
import { TopNavbar } from "./TopNavbar";
import { RightPanel } from "./RightPanel";
import { BottomNavigation } from "./BottomNavigation";
import { FAB } from "./FAB";
import { SectionErrorBoundary } from "@/components/errors/SectionErrorBoundary";

export function DashboardLayout() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <div
      className="grid h-screen w-full bg-background overflow-hidden
      grid-cols-1 
      md:grid-cols-[max-content_1fr] 
      xl:grid-cols-[max-content_1fr_max-content]"
    >
      {/* ─── Desktop & Tablet Sidebar ─────────────────────────────── */}
      <Sidebar />

      {/* ─── Mobile Slide-out Drawer (secondary / overflow links) ─── */}
      <MobileSidebar />

      {/* ─── Main content column ──────────────────────────────────── */}
      <div className="flex min-w-0 flex-col relative h-screen overflow-hidden">
        <TopNavbar />

        <main
          className={[
            "flex-1 overflow-y-auto",
            // On mobile add bottom padding so bottom nav never obscures content
            "pb-16 md:pb-0",
          ].join(" ")}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={pathname}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.18, ease: "easeOut" }}
              className="mx-auto w-full max-w-[1400px] px-4 py-6 sm:px-6"
            >
              <SectionErrorBoundary sectionName="Page View">
                <Outlet />
              </SectionErrorBoundary>
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* ─── Desktop Right Activity Panel ─────────────────────────── */}
      <SectionErrorBoundary sectionName="Right Activity Panel">
        <RightPanel />
      </SectionErrorBoundary>

      {/* ─── Mobile-only: Bottom Navigation & FAB ─────────────────── */}
      <BottomNavigation />
      <FAB to="/flares" ariaLabel="Create a new post" />
    </div>
  );
}
