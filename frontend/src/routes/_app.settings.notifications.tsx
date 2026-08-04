import { createFileRoute } from "@tanstack/react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { useToast } from "@/components/ui/use-toast";

export const Route = createFileRoute("/_app/settings/notifications")({
  component: NotificationSettingsPage,
});

function NotificationSettingsPage() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const { data: preferences, isLoading } = useQuery({
    queryKey: ["notification-preferences"],
    queryFn: async () => {
      const res = await api.get("/api/notifications/preferences");
      return res.data;
    },
  });

  const [formData, setFormData] = useState({
    email_enabled: true,
    websocket_enabled: true,
    database_enabled: true,
    project_updates: true,
    invitations: true,
    role_changes: true,
    marketing_emails: false,
    system_alerts: true,
  });

  useEffect(() => {
    if (preferences) {
      setFormData(preferences);
    }
  }, [preferences]);

  const updateMutation = useMutation({
    mutationFn: async (newData: typeof formData) => {
      await api.put("/api/notifications/preferences", newData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notification-preferences"] });
      toast({
        title: "Preferences updated",
        description: "Your notification settings have been saved successfully.",
      });
    },
    onError: () => {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to update preferences.",
      });
    },
  });

  const handleToggle = (key: keyof typeof formData) => {
    const newData = { ...formData, [key]: !formData[key] };
    setFormData(newData);
    updateMutation.mutate(newData);
  };

  if (isLoading) return <div>Loading preferences...</div>;

  return (
    <div className="space-y-6 max-w-4xl mx-auto p-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Notification Preferences</h2>
        <p className="text-muted-foreground">Manage how and when you receive notifications.</p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Delivery Channels</CardTitle>
            <CardDescription>Choose where you want to receive notifications.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Email Notifications</Label>
                <p className="text-sm text-muted-foreground">
                  Receive updates via your registered email address.
                </p>
              </div>
              <Switch
                checked={formData.email_enabled}
                onCheckedChange={() => handleToggle("email_enabled")}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">In-App Notifications (Database)</Label>
                <p className="text-sm text-muted-foreground">
                  Store notifications in the app notification center.
                </p>
              </div>
              <Switch
                checked={formData.database_enabled}
                onCheckedChange={() => handleToggle("database_enabled")}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Real-time Popups (WebSocket)</Label>
                <p className="text-sm text-muted-foreground">
                  Show instant notification toasts while you are active.
                </p>
              </div>
              <Switch
                checked={formData.websocket_enabled}
                onCheckedChange={() => handleToggle("websocket_enabled")}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Event Triggers</CardTitle>
            <CardDescription>Select which events should trigger a notification.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Project Updates</Label>
                <p className="text-sm text-muted-foreground">
                  When projects you are involved in are updated.
                </p>
              </div>
              <Switch
                checked={formData.project_updates}
                onCheckedChange={() => handleToggle("project_updates")}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Invitations</Label>
                <p className="text-sm text-muted-foreground">
                  When you are invited to a project or team.
                </p>
              </div>
              <Switch
                checked={formData.invitations}
                onCheckedChange={() => handleToggle("invitations")}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Role Changes</Label>
                <p className="text-sm text-muted-foreground">
                  When your permissions or roles are modified.
                </p>
              </div>
              <Switch
                checked={formData.role_changes}
                onCheckedChange={() => handleToggle("role_changes")}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">System Alerts</Label>
                <p className="text-sm text-muted-foreground">
                  Critical security and system notifications.
                </p>
              </div>
              <Switch
                checked={formData.system_alerts}
                onCheckedChange={() => handleToggle("system_alerts")}
                disabled={true} // Usually shouldn't be disabled fully, but just for demo
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Marketing & News</Label>
                <p className="text-sm text-muted-foreground">
                  Occasional updates about DevLink features.
                </p>
              </div>
              <Switch
                checked={formData.marketing_emails}
                onCheckedChange={() => handleToggle("marketing_emails")}
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
