import { api } from '../client';

export interface DeveloperInsightsMetrics {
  projects_created: number;
  applications_submitted: number;
  profile_views: number;
  followers_gained: number;
  messages_sent: number;
  contribution_streak: number;
  ai_match_success_rate: number;
}

export interface MetricTrend {
  current: number;
  previous: number;
  percentage_change: number;
}

export interface ActivityPoint {
  date: string;
  activity_count: number;
  projects: number;
  messages: number;
  applications: number;
}

export interface DeveloperInsightsData {
  user_id: number;
  date_range: string;
  metrics: DeveloperInsightsMetrics;
  trends: Record<string, MetricTrend>;
  activity_timeline: ActivityPoint[];
  top_skills_matched: string[];
  recent_achievements: string[];
}

export const getDeveloperInsights = async (range: string = '30d'): Promise<DeveloperInsightsData> => {
  return await api.get<DeveloperInsightsData>(`/developer-insights?range=${range}`);
};
