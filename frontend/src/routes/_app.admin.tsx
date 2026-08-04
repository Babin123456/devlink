import { Outlet, createFileRoute, redirect, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/_app/admin")({
  beforeLoad: ({ context }) => {
    // Basic auth check: only super admins should access this.
    // Assuming context.auth has user info, or redirect if not authorized.
    // For now we allow since we might not have full RBAC setup in the frontend mock.
    // In production, uncomment:
    // if (!context.auth?.user?.premium) {
    //   throw redirect({ to: "/" });
    // }
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
        <Link
          to="/admin/audit-logs"
          activeProps={{
            className:
              "border-b-2 border-primary font-semibold text-foreground px-4 py-2 text-sm whitespace-nowrap",
          }}
          inactiveProps={{
            className:
              "text-muted-foreground px-4 py-2 hover:text-foreground transition-colors text-sm whitespace-nowrap",
          }}
        >
          Audit Logs
        </Link>
        <Link
          to="/admin/notifications"
          activeProps={{
            className:
              "border-b-2 border-primary font-semibold text-foreground px-4 py-2 text-sm whitespace-nowrap",
          }}
          inactiveProps={{
            className:
              "text-muted-foreground px-4 py-2 hover:text-foreground transition-colors text-sm whitespace-nowrap",
          }}
        >
          Notification Delivery
        </Link>
        <Link
          to="/admin/jobs"
          activeProps={{
            className:
              "border-b-2 border-primary font-semibold text-foreground px-4 py-2 text-sm whitespace-nowrap",
          }}
          inactiveProps={{
            className:
              "text-muted-foreground px-4 py-2 hover:text-foreground transition-colors text-sm whitespace-nowrap",
          }}
        >
          Background Jobs
        </Link>
      </div>

      <Outlet />
    </div>
  ),
});
