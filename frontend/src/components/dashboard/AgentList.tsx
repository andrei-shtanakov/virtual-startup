import React from "react";
import { Agent } from "../../types/agent";

interface AgentListProps {
  agents: Agent[];
  loading?: boolean;
}

/**
 * AgentList component displays all agents with their status
 */
export const AgentList: React.FC<AgentListProps> = ({ agents, loading = false }) => {
  const getAgentTypeColor = (type: string) => {
    switch (type) {
      case "driver":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200";
      case "creator":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "generator":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200";
      case "dynamic":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "idle":
        return "text-green-600 dark:text-green-400";
      case "working":
        return "text-yellow-600 dark:text-yellow-400";
      case "waiting":
        return "text-orange-600 dark:text-orange-400";
      default:
        return "text-gray-600 dark:text-gray-400";
    }
  };

  if (loading) {
    return (
      <div className="p-4 text-center text-gray-500 dark:text-gray-400">
        Loading agents...
      </div>
    );
  }

  if (agents.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 dark:text-gray-400">
        No agents available
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {agents.map((agent) => (
        <div
          key={agent.id}
          className="p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 flex-1 min-w-0">
              {/* Agent type badge */}
              <span
                className={`${getAgentTypeColor(
                  agent.type
                )} text-xs font-semibold px-2 py-0.5 rounded uppercase flex-shrink-0`}
              >
                {agent.type}
              </span>

              {/* Agent name */}
              <span className="font-medium text-gray-900 dark:text-white truncate">
                {agent.name}
              </span>
            </div>

            {/* Status indicator */}
            <div className={`flex items-center gap-1 text-sm ${getStatusColor(agent.status)}`}>
              <span className={agent.status === "working" ? "animate-pulse" : ""}>●</span>
              <span className="capitalize">{agent.status}</span>
            </div>
          </div>

          {/* Agent role */}
          <div className="mt-1 text-xs text-gray-600 dark:text-gray-400 truncate">
            {agent.role}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AgentList;

