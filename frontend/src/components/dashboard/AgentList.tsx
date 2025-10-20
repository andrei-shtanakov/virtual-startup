import React from "react";
import { motion } from "framer-motion";
import { Briefcase, Palette, Factory, Zap, Bot } from "lucide-react";
import type { Agent } from "../../types/agent";

interface AgentListProps {
  agents: Agent[];
  loading?: boolean;
}

// Helper function to get relative time
const getRelativeTime = (timestamp: string): string => {
  const now = new Date();
  const past = new Date(timestamp);
  const diffMs = now.getTime() - past.getTime();
  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);

  if (diffMinutes < 1) return "now";
  if (diffMinutes < 60) return `${diffMinutes}m`;
  if (diffHours < 24) return `${diffHours}h`;
  return past.toLocaleDateString();
};

/**
 * AgentList - Compact terminal-style agent display
 */
export const AgentList: React.FC<AgentListProps> = ({ agents, loading = false }) => {
  const getAgentIcon = (type: string) => {
    const iconClass = "h-4 w-4";
    switch (type) {
      case "driver":
        return <Briefcase className={iconClass} />;
      case "creator":
        return <Palette className={iconClass} />;
      case "generator":
        return <Factory className={iconClass} />;
      case "dynamic":
        return <Zap className={iconClass} />;
      default:
        return <Bot className={iconClass} />;
    }
  };

  const getStatusIndicator = (status: string) => {
    if (status === "working") {
      return (
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
        </span>
      );
    }
    const dotColor = status === "idle" ? "bg-primary" : status === "waiting" ? "bg-chart-2" : "bg-muted-foreground";
    return <span className={`inline-flex h-2 w-2 rounded-full ${dotColor}`} />;
  };

  if (loading) {
    return (
      <div className="p-4 text-center text-sm text-muted-foreground">
        Loading...
      </div>
    );
  }

  if (agents.length === 0) {
    return (
      <div className="p-4 text-center text-sm text-muted-foreground">
        No agents
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {agents.map((agent, index) => (
        <motion.div
          key={agent.id}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.15, delay: index * 0.03 }}
          className="group px-3 py-2.5 rounded-md border border-border bg-accent/30 hover:bg-accent/50 transition-colors cursor-pointer"
        >
          <div className="flex items-center gap-3">
            {/* Icon */}
            <div className="flex-shrink-0 w-7 h-7 rounded-md bg-background border border-border flex items-center justify-center text-muted-foreground">
              {getAgentIcon(agent.type)}
            </div>

            {/* Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                {getStatusIndicator(agent.status)}
                <h3 className="text-sm font-medium text-foreground truncate">
                  {agent.name}
                </h3>
              </div>
              <p className="text-xs text-muted-foreground truncate mt-0.5">
                {agent.role}
              </p>
            </div>

            {/* Status & Time */}
            <div className="flex-shrink-0 text-right">
              <div className="text-xs font-mono text-muted-foreground uppercase">
                {agent.type}
              </div>
              {agent.updated_at && (
                <div className="text-xs font-mono text-muted-foreground/70 mt-0.5">
                  {getRelativeTime(agent.updated_at)}
                </div>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default AgentList;

