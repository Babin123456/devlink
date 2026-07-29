import { createFileRoute } from "@tanstack/react-router";
import { GreetingHero } from "@/features/dashboard/GreetingHero";
import { StatsRow } from "@/features/dashboard/StatsRow";
import {
  RecentActivity,
  BuilderRequests,
  InviteRequests,
  SuggestedBuilders,
  TrendingProjects,
  AIRecommendations,
  MessagesPreview,
  QuickActions,
  UpcomingDeadlines,
  NotificationsFeed,
} from "@/features/dashboard/sections";

export const Route = createFileRoute("/_app/dashboard")({
  head: () => ({
    meta: [
      { title: "Dashboard — DevLink" },
      {
        name: "description",
        content: "Your DevLink command center: projects, matches, messages and streaks.",
      },
    ],
  }),
  component: Dashboard,
});

function Dashboard() {
  return (
    <div className="mx-auto flex max-w-[1400px] w-full flex-col gap-6 pb-12 pt-2 px-2 sm:px-4">
      <GreetingHero />
      <StatsRow />

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 flex flex-col gap-6">
          <SuggestedBuilders />
          <div className="grid gap-6 sm:grid-cols-2">
            <BuilderRequests />
            <InviteRequests />
          </div>
          <TrendingProjects />
          <div className="grid gap-6 sm:grid-cols-2">
            <MessagesPreview />
            <NotificationsFeed />
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <QuickActions />
          <AIRecommendations />
          <UpcomingDeadlines />
          <RecentActivity />
        </div>
      </div>
    </div>
  );
}
