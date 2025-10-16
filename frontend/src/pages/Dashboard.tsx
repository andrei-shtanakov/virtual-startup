import React from "react";
import AgentChats from "../components/dashboard/AgentChats";
import StatsPanel from "../components/dashboard/StatsPanel";
import { useAgents } from "../hooks";

/**
 * Dashboard page - Main view with 3 agent chat windows and statistics panel
 */
export const Dashboard: React.FC = () => {
  const { agents, loading: agentsLoading, error } = useAgents();

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-[1920px] mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                🤖 Virtual Startup Dashboard
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Multi-agent AI system powered by AutoGen
              </p>
            </div>

            {/* Connection indicator */}
            <div className="flex items-center gap-4">
              {error && (
                <div className="text-sm text-red-600 dark:text-red-400">
                  ⚠️ {error}
                </div>
              )}
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200">
                <span className="text-green-600 dark:text-green-400">●</span>
                <span className="text-sm font-medium">Live</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-[1920px] mx-auto px-4 py-6">
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 h-[calc(100vh-140px)]">
          {/* Chat windows - 3 columns */}
          <div className="xl:col-span-3">
            {agentsLoading ? (
              <div className="h-full flex items-center justify-center bg-white dark:bg-gray-800 rounded-lg">
                <div className="text-center">
                  <div className="text-4xl mb-4">⏳</div>
                  <p className="text-gray-600 dark:text-gray-400">Loading agents...</p>
                </div>
              </div>
            ) : (
              <AgentChats agents={agents} />
            )}
          </div>

          {/* Stats panel - 1 column */}
          <div className="xl:col-span-1">
            <StatsPanel
              agents={agents}
              agentsLoading={agentsLoading}
              systemStatus="operational"
            />
          </div>
        </div>
      </main>

      {/* Footer info */}
      <div className="fixed bottom-4 left-4 bg-white dark:bg-gray-800 shadow-lg rounded-lg px-4 py-2 border border-gray-200 dark:border-gray-700">
        <div className="text-xs text-gray-600 dark:text-gray-400">
          💡 <strong>Tip:</strong> Chat with agents in real-time
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

