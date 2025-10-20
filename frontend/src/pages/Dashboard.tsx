import React from "react";
import { Loader2, Activity, Zap } from "lucide-react";
import AgentList from "../components/dashboard/AgentList";
import StatsPanel from "../components/dashboard/StatsPanel";
import ActivityLogs from "../components/dashboard/ActivityLogs";
import QuickChat from "../components/dashboard/QuickChat";
import { useAgents } from "../hooks";

/**
 * Dashboard page - Minimalist terminal-style overview
 */
export const Dashboard: React.FC = () => {
  const { agents, loading: agentsLoading, error, isConnected } = useAgents();

  return (
    <div className="h-full bg-background">
      <div className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Status Banner */}
        {error && (
          <div className="px-4 py-3 rounded-md border border-destructive/20 bg-destructive/10">
            <div className="flex items-center gap-2 text-sm text-destructive">
              <Activity className="h-4 w-4" />
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Stats Panel */}
          <div className="lg:col-span-1">
            <StatsPanel
              agents={agents}
              agentsLoading={agentsLoading}
              systemStatus="operational"
            />
          </div>

          {/* Agent List */}
          <div className="lg:col-span-1">
            {agentsLoading ? (
              <div className="h-full flex items-center justify-center bg-card rounded-lg border border-border p-8">
                <div className="text-center space-y-3">
                  <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto" />
                  <p className="text-sm text-muted-foreground">Loading agents...</p>
                </div>
              </div>
            ) : (
              <div className="bg-card rounded-lg border border-border">
                <div className="p-4 border-b border-border">
                  <div className="flex items-center gap-2">
                    <Zap className="h-4 w-4 text-primary" />
                    <h2 className="text-sm font-semibold text-foreground">
                      Active Agents
                    </h2>
                  </div>
                </div>
                <div className="p-4">
                  <AgentList agents={agents} />
                </div>
              </div>
            )}
          </div>

          {/* Activity & Chat */}
          <div className="lg:col-span-1 space-y-6">
            <div className="h-[350px]">
              <ActivityLogs maxLogs={50} />
            </div>

            <div className="h-[350px]">
              <QuickChat maxMessages={50} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;



