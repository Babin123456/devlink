import { Outlet, useRouterState } from "@tanstack/react-router";
import { AnimatePresence, motion } from "framer-motion";
import { Sidebar } from "./Sidebar";
import { MobileSidebar } from "./MobileSidebar";
import { TopNavbar } from "./TopNavbar";
import { RightPanel } from "./RightPanel";
import { BottomNavigation } from "./BottomNavigation";
import { FAB } from "./FAB";

export function DashboardLayout() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <div className="flex min-h-screen w-full bg-background overflow-hidden">
      {/* ─── Desktop & Tablet Sidebar ─────────────────────────────── */}
      <Sidebar />

      {/* ─── Mobile Slide-out Drawer (secondary / overflow links) ─── */}
      <MobileSidebar />

      {/* ─── Main content column ──────────────────────────────────── */}
      <div className="flex min-w-0 flex-1 flex-col relative h-screen">
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
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* ─── Desktop Right Activity Panel ─────────────────────────── */}
      <RightPanel />

      {/* ─── Mobile-only: Bottom Navigation & FAB ─────────────────── */}
      <BottomNavigation />
      <FAB to="/flares" ariaLabel="Create a new post" />
    </div>
  );
}
