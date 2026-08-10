import React, { useState, useEffect } from 'react';
import { 
  FolderPlus, 
  Send, 
  Eye, 
  UserPlus, 
  MessageSquare, 
  Flame, 
  Sparkles, 
  TrendingUp, 
  Calendar,
  AlertCircle,
  RefreshCw
} from 'lucide-react';
import { getDeveloperInsights, DeveloperInsightsData } from '../../api/modules/developerInsights';

export const DeveloperInsightsDashboard: React.FC = () => {
  const [dateRange, setDateRange] = useState<string>('30d');
  const [data, setData] = useState<DeveloperInsightsData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInsights = async (range: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await getDeveloperInsights(range);
      setData(res);
    } catch (err: unknown) {
      const errorObj = err as { message?: string };
      setError(errorObj?.message || 'Failed to load developer insights.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInsights(dateRange);
  }, [dateRange]);

  const ranges = [
    { label: '7 Days', value: '7d' },
    { label: '30 Days', value: '30d' },
    { label: '90 Days', value: '90d' },
    { label: '1 Year', value: '1y' },
    { label: 'All Time', value: 'all' },
  ];

  return (
    <div className="w-full space-y-6 p-6 bg-white dark:bg-slate-900/40 text-slate-900 dark:text-slate-100 rounded-xl border border-slate-200 dark:border-slate-800 backdrop-blur-sm shadow-sm dark:shadow-none">
      {/* Header & Date Range Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-900 dark:text-white">
            <Sparkles className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            Developer Insights Dashboard
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Personalized summary of your activity, engagement metrics, and AI match performance on DevLink.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-slate-100 dark:bg-slate-800/80 p-1 rounded-lg border border-slate-200 dark:border-slate-700">
          <Calendar className="w-4 h-4 text-slate-500 dark:text-slate-400 ml-2 hidden sm:inline-block" />
          {ranges.map((r) => (
            <button
              key={r.value}
              onClick={() => setDateRange(r.value)}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                dateRange === r.value
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700/50'
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 animate-pulse">
          {[...Array(7)].map((_, i) => (
            <div key={i} className="h-32 bg-slate-100 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700/50 p-4 space-y-3">
              <div className="h-4 bg-slate-200 dark:bg-slate-700/50 rounded w-1/2"></div>
              <div className="h-8 bg-slate-200 dark:bg-slate-700/50 rounded w-3/4"></div>
              <div className="h-3 bg-slate-200 dark:bg-slate-700/50 rounded w-1/3"></div>
            </div>
          ))}
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="p-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/50 rounded-xl text-red-700 dark:text-red-200 flex flex-col items-center gap-3 text-center">
          <AlertCircle className="w-8 h-8 text-red-500 dark:text-red-400" />
          <p className="font-semibold text-lg">{error}</p>
          <button
            onClick={() => fetchInsights(dateRange)}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 dark:bg-red-800/50 hover:bg-red-700 dark:hover:bg-red-800 text-white text-sm rounded-lg border border-red-500 dark:border-red-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" /> Try Again
          </button>
        </div>
      )}

      {/* Main Content */}
      {!loading && !error && data && (
        <div className="space-y-6">
          {Object.values(data.metrics).every((val) => val === 0) ? (
            <div className="p-12 text-center bg-slate-50 dark:bg-slate-800/20 rounded-xl border border-slate-200 dark:border-slate-800 space-y-3">
              <Sparkles className="w-12 h-12 text-slate-400 dark:text-slate-500 mx-auto" />
              <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-300">No Activity Recorded</h3>
              <p className="text-sm text-slate-500">
                You haven't recorded any metrics for this date range yet.
              </p>
            </div>
          ) : (
            <>
              {/* Metrics Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Projects Created</span>
                    <div className="p-2 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-lg">
                      <FolderPlus className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.projects_created}</span>
                    <div className="flex items-center gap-1 mt-1 text-xs text-emerald-600 dark:text-emerald-400">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>+{data.trends.projects_created?.percentage_change}% vs prev period</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Applications Submitted</span>
                    <div className="p-2 bg-purple-500/10 text-purple-600 dark:text-purple-400 rounded-lg">
                      <Send className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.applications_submitted}</span>
                    <div className="flex items-center gap-1 mt-1 text-xs text-emerald-600 dark:text-emerald-400">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>+{data.trends.applications_submitted?.percentage_change}% vs prev period</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Profile Views</span>
                    <div className="p-2 bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 rounded-lg">
                      <Eye className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.profile_views}</span>
                    <div className="flex items-center gap-1 mt-1 text-xs text-emerald-600 dark:text-emerald-400">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>+{data.trends.profile_views?.percentage_change}% vs prev period</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Followers Gained</span>
                    <div className="p-2 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-lg">
                      <UserPlus className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.followers_gained}</span>
                    <div className="flex items-center gap-1 mt-1 text-xs text-emerald-600 dark:text-emerald-400">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>+{data.trends.followers_gained?.percentage_change}% vs prev period</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Messages Sent</span>
                    <div className="p-2 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-lg">
                      <MessageSquare className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.messages_sent}</span>
                    <div className="flex items-center gap-1 mt-1 text-xs text-emerald-600 dark:text-emerald-400">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>+{data.trends.messages_sent?.percentage_change}% vs prev period</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Contribution Streak</span>
                    <div className="p-2 bg-orange-500/10 text-orange-600 dark:text-orange-400 rounded-lg">
                      <Flame className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.contribution_streak} days</span>
                    <div className="flex items-center gap-1 mt-1 text-xs text-orange-600 dark:text-orange-400 font-semibold">
                      <span>Active Streak 🔥</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 bg-slate-50 dark:bg-gradient-to-br dark:from-slate-800/80 dark:to-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-slate-300 dark:hover:border-slate-700 transition-all sm:col-span-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">AI Match Success Rate</span>
                    <div className="p-2 bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 rounded-lg">
                      <Sparkles className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="mt-3 flex items-baseline justify-between">
                    <span className="text-3xl font-extrabold text-slate-900 dark:text-white">{data.metrics.ai_match_success_rate}%</span>
                    <span className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">Based on skill vector fit</span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full mt-3 overflow-hidden">
                    <div
                      className="bg-indigo-600 dark:bg-indigo-500 h-full rounded-full transition-all duration-500"
                      style={{ width: `${data.metrics.ai_match_success_rate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};
