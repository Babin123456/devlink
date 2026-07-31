import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";

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
        <p className="text-muted-foreground">Manage your platform and view audit logs.</p>
        
        <div className="flex gap-4 border-b pb-2 mt-4">
          <a href="/admin/audit-logs" className="text-blue-600 hover:underline">Audit Logs</a>
          <a href="/admin/notifications" className="text-blue-600 hover:underline">Notifications</a>
          <a href="/admin/maintenance" className="text-blue-600 hover:underline">Maintenance Mode</a>
          <a href="/admin/search-analytics" className="text-blue-600 hover:underline">Search Analytics</a>
        </div>
      </div>
      <Outlet />
    </div>
  ),
});
