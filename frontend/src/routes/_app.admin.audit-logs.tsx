import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { auditService } from "@/services";
import type { AuditLog } from "@/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Search, Download } from "lucide-react";
import { format } from "date-fns";

export const Route = createFileRoute("/_app/admin/audit-logs")({
  component: AuditLogsPage,
});

function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState<string>("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const data = await auditService.list({ limit: 100 });
      setLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    if (logs.length === 0) return;
    const header = ["ID", "Actor ID", "Action", "Entity Type", "Entity ID", "IP Address", "Date"];
    const rows = logs.map((log) => [
      log.id,
      log.actor_id || "",
      log.action,
      log.entity_type,
      log.entity_id || "",
      log.ip_address || "",
      new Date(log.created_at).toLocaleString(),
    ]);
    const csvContent =
      "data:text/csv;charset=utf-8," + [header, ...rows].map((e) => e.join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "audit_logs.csv");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleExportJSON = () => {
    if (logs.length === 0) return;
    const dataStr =
      "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(logs, null, 2));
    const link = document.createElement("a");
    link.setAttribute("href", dataStr);
    link.setAttribute("download", "audit_logs.json");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const filteredLogs = logs.filter((log) => {
    const matchesAction = filterAction === "all" || log.action === filterAction;
    const matchesSearch =
      search === "" ||
      log.actor_id?.includes(search) ||
      log.entity_id?.includes(search) ||
      log.action.includes(search);
    return matchesAction && matchesSearch;
  });

  return (
    <Card>
      <CardHeader className="flex flex-row justify-between items-center">
        <CardTitle>System Audit Logs</CardTitle>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleExportCSV}>
            <Download className="w-4 h-4 mr-2" />
            CSV
          </Button>
          <Button variant="outline" size="sm" onClick={handleExportJSON}>
            <Download className="w-4 h-4 mr-2" />
            JSON
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex gap-4 mb-4">
          <div className="relative flex-1">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by ID or Action..."
              className="pl-8"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <Select value={filterAction} onValueChange={setFilterAction}>
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Filter by action" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Actions</SelectItem>
              <SelectItem value="project_created">Project Created</SelectItem>
              <SelectItem value="project_updated">Project Updated</SelectItem>
              <SelectItem value="profile_updated">Profile Updated</SelectItem>
              <SelectItem value="organization_created">Organization Created</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>User</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>Resource</TableHead>
                <TableHead>IP</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center h-24">
                    Loading audit logs...
                  </TableCell>
                </TableRow>
              ) : filteredLogs.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center h-24">
                    No logs found.
                  </TableCell>
                </TableRow>
              ) : (
                filteredLogs.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell className="whitespace-nowrap">
                      {format(new Date(log.created_at), "MMM d, HH:mm:ss")}
                    </TableCell>
                    <TableCell
                      className="font-medium truncate max-w-[120px]"
                      title={log.actor_id ?? ""}
                    >
                      {log.actor_id || "System"}
                    </TableCell>
                    <TableCell>
                      <span className="bg-muted px-2 py-1 rounded-md text-xs font-mono">
                        {log.action}
                      </span>
                    </TableCell>
                    <TableCell>
                      {log.entity_type} {log.entity_id ? `(${log.entity_id})` : ""}
                    </TableCell>
                    <TableCell className="text-muted-foreground font-mono text-sm">
                      {log.ip_address || "N/A"}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
