import { Outlet, createFileRoute, Link } from "@tanstack/react-router";

const tabActiveProps = {
  className:
    "border-b-2 border-primary font-semibold text-foreground px-4 py-2 text-sm whitespace-nowrap",
};

const tabInactiveProps = {
  className:
    "text-muted-foreground px-4 py-2 hover:text-foreground transition-colors text-sm whitespace-nowrap",
};

/**
 * Every admin sub-route, in the order they appear in the tab strip.
 *
 * Kept as data rather than as repeated JSX because the strip had already
 * drifted: pages were added under /admin without a matching tab, so the only
 * way to reach them was to type the URL.
 */
const ADMIN_TABS = [
  { to: "/admin/audit-logs", label: "Audit Logs" },
  { to: "/admin/notifications", label: "Notification Delivery" },
  { to: "/admin/jobs", label: "Background Jobs" },
  { to: "/admin/maintenance", label: "Maintenance Mode" },
  { to: "/admin/search-analytics", label: "Search Analytics" },
  { to: "/admin/community-stats", label: "Community Stats" },
  { to: "/admin/api-request-analytics", label: "API Request Analytics" },
] as const;

export const Route = createFileRoute("/_app/admin")({
  beforeLoad: () => {
    // Access to this section is still enforced server-side only. Once the
    // frontend carries the signed-in user's roles in route context, the
    // super-admin check belongs here so we stop rendering an empty console to
    // people who will only get 403s from every panel inside it.
  },
  component: () => (
    <div className="flex flex-col gap-6 w-full max-w-7xl mx-auto p-4 md:p-8">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Admin Console</h1>
        <p className="text-muted-foreground">
          Manage your platform, view audit logs, and monitor background tasks.
        </p>
      </div>

      <div className="flex border-b border-border gap-2 md:gap-4 overflow-x-auto scrollbar-none">
        {ADMIN_TABS.map((tab) => (
          <Link
            key={tab.to}
            to={tab.to}
            activeProps={tabActiveProps}
            inactiveProps={tabInactiveProps}
          >
            {tab.label}
          </Link>
        ))}
      </div>

      <Outlet />
    </div>
  ),
});
