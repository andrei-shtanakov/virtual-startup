import React from "react";
import AgentList from "../components/dashboard/AgentList";
import StatsPanel from "../components/dashboard/StatsPanel";
import { useAgents } from "../hooks";

interface DashboardProps {
  onNavigate?: (page: string) => void;
}

/**
 * Dashboard page - Main view with agent status and statistics
 */
export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const { agents, loading: agentsLoading, error } = useAgents();

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4">
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
                <span className="text-sm font-medium">System Active</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Stats panel - Left side */}
          <div className="lg:col-span-1">
            <StatsPanel
              agents={agents}
              agentsLoading={agentsLoading}
              systemStatus="operational"
            />
          </div>

          {/* Agent list - Right side */}
          <div className="lg:col-span-2">
            {agentsLoading ? (
              <div className="h-full flex items-center justify-center bg-white dark:bg-gray-800 rounded-lg p-8">
                <div className="text-center">
                  <div className="text-4xl mb-4">⏳</div>
                  <p className="text-gray-600 dark:text-gray-400">Loading agents...</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                    Active Agents
                  </h2>
                  <button
                    onClick={() => onNavigate?.("demo")}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                  >
                    💬 Open Chat
                  </button>
                </div>
                <AgentList agents={agents} />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Quick action panel */}
      <div className="fixed bottom-4 left-4 bg-white dark:bg-gray-800 shadow-lg rounded-lg px-4 py-3 border border-gray-200 dark:border-gray-700">
        <div className="text-xs text-gray-600 dark:text-gray-400">
          💡 <strong>Quick Tip:</strong> Use the{" "}
          <button
            onClick={() => onNavigate?.("demo")}
            className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
          >
            Chat Demo
          </button>{" "}
          page to interact with agents
        </div>
      </div>
    </div>
  );
};

export default Dashboard;


