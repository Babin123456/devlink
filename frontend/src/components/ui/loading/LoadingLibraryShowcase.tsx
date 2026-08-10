import React, { useState } from 'react';
import { SkeletonCard } from './SkeletonCard';
import { SkeletonTable } from './SkeletonTable';
import { SkeletonProfile } from './SkeletonProfile';
import { Spinner } from './Spinner';
import { ProgressBar } from './ProgressBar';
import { FullPageLoader } from './FullPageLoader';
import { Sparkles } from 'lucide-react';

type TabType = 'card' | 'table' | 'profile' | 'spinner' | 'progress' | 'full';

export const LoadingLibraryShowcase: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('card');
  const [progressVal, setProgressVal] = useState<number>(65);

  const tabs: { key: TabType; label: string }[] = [
    { key: 'card', label: 'Skeleton Card' },
    { key: 'table', label: 'Skeleton Table' },
    { key: 'profile', label: 'Skeleton Profile' },
    { key: 'spinner', label: 'Spinner' },
    { key: 'progress', label: 'Progress Bar' },
    { key: 'full', label: 'Full Page Loader' },
  ];

  return (
    <div className="w-full max-w-5xl mx-auto p-6 bg-slate-900/60 border border-slate-800 rounded-xl space-y-6 text-slate-100 backdrop-blur-md">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-400" />
            Reusable Loading State Library
          </h2>
          <p className="text-sm text-slate-400">
            Standardized accessible loading skeletons, spinners, progress indicators, and full-page loaders.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-3.5 py-1.5 text-xs font-semibold rounded-lg border transition-all ${
              activeTab === tab.key
                ? 'bg-indigo-600 border-indigo-500 text-white shadow-sm'
                : 'bg-slate-800/40 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="p-6 bg-slate-950/60 border border-slate-800 rounded-xl">
        {activeTab === 'card' && <SkeletonCard count={3} />}
        {activeTab === 'table' && <SkeletonTable rows={4} columns={4} />}
        {activeTab === 'profile' && <SkeletonProfile />}
        {activeTab === 'spinner' && (
          <div className="flex items-center gap-6 py-6">
            <Spinner size="sm" label="Small spinner" />
            <Spinner size="md" label="Medium spinner" />
            <Spinner size="lg" label="Large spinner" />
            <Spinner size="xl" label="Extra large spinner" />
          </div>
        )}
        {activeTab === 'progress' && (
          <div className="space-y-6 max-w-md py-4">
            <ProgressBar progress={progressVal} showLabel={true} />
            <ProgressBar indeterminate={true} />
            <div className="flex gap-2">
              <button
                onClick={() => setProgressVal((p) => Math.max(0, p - 15))}
                className="px-3 py-1 bg-slate-800 text-xs rounded border border-slate-700"
              >
                - 15%
              </button>
              <button
                onClick={() => setProgressVal((p) => Math.min(100, p + 15))}
                className="px-3 py-1 bg-indigo-600 text-xs rounded border border-indigo-500"
              >
                + 15%
              </button>
            </div>
          </div>
        )}
        {activeTab === 'full' && (
          <div className="p-8 text-center space-y-4">
            <p className="text-xs text-slate-400">Click below to toggle Full Page Loader for 3 seconds.</p>
            <button
              onClick={() => {
                const el = document.getElementById('full-page-demo');
                if (el) el.style.display = 'flex';
                setTimeout(() => {
                  if (el) el.style.display = 'none';
                }, 3000);
              }}
              className="px-4 py-2 bg-indigo-600 text-white text-xs font-semibold rounded-lg shadow-sm hover:bg-indigo-500 transition-colors"
            >
              Trigger Full Page Loader (3s)
            </button>

            <div id="full-page-demo" style={{ display: 'none' }}>
              <FullPageLoader message="Simulating full application loading state..." />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
