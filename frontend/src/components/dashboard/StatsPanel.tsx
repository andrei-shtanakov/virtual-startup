import React from "react";
import type { Agent } from "../../types/agent";
import AgentList from "./AgentList";
import WorkflowStatus from "./WorkflowStatus";

interface StatsPanelProps {
  agents: Agent[];
  agentsLoading?: boolean;
  systemStatus?: "operational" | "degraded" | "down";
}

/**
 * StatsPanel component displays system statistics and agent information
 */
export const StatsPanel: React.FC<StatsPanelProps> = ({
  agents,
  agentsLoading = false,
  systemStatus = "operational",
}) => {
  // Calculate agent statistics
  const totalAgents = agents.length;
  const activeAgents = agents.filter((a) => a.status === "working").length;
  const idleAgents = agents.filter((a) => a.status === "idle").length;

  // Get system status color
  const getStatusColor = () => {
    switch (systemStatus) {
      case "operational":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "degraded":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "down":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gray-100 dark:bg-gray-900 px-4 py-3 border-b border-gray-300 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          📊 System Overview
        </h3>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* System Status */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            System Status
          </h4>
          <div
            className={`${getStatusColor()} px-3 py-2 rounded-lg text-center font-medium flex items-center justify-center gap-2`}
          >
            <span className={systemStatus === "operational" ? "text-green-600 dark:text-green-400" : ""}>
              {systemStatus === "operational" ? "●" : "○"}
            </span>
            <span className="capitalize">{systemStatus}</span>
          </div>
        </div>

        {/* Agent Statistics */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Agent Statistics
          </h4>
          <div className="grid grid-cols-3 gap-2">
            {/* Total */}
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 text-center">
              <div className="text-xl font-bold text-blue-600 dark:text-blue-400">
                {totalAgents}
              </div>
              <div className="text-xs text-blue-700 dark:text-blue-300 mt-1">
                Total
              </div>
            </div>

            {/* Active */}
            <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800 text-center">
              <div className="text-xl font-bold text-yellow-600 dark:text-yellow-400">
                {activeAgents}
              </div>
              <div className="text-xs text-yellow-700 dark:text-yellow-300 mt-1">
                Active
              </div>
            </div>

            {/* Idle */}
            <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800 text-center">
              <div className="text-xl font-bold text-green-600 dark:text-green-400">
                {idleAgents}
              </div>
              <div className="text-xs text-green-700 dark:text-green-300 mt-1">
                Idle
              </div>
            </div>
          </div>
        </div>

        {/* Workflow Status */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Workflows
          </h4>
          <WorkflowStatus
            activeWorkflows={0}
            completedWorkflows={0}
            currentTask={undefined}
          />
        </div>

        {/* Agent List */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            All Agents ({agents.length})
          </h4>
          <AgentList agents={agents} loading={agentsLoading} />
        </div>
      </div>
    </div>
  );
};

export default StatsPanel;

