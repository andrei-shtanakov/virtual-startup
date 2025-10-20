import React from "react";
import { motion } from "framer-motion";
import { BarChart3, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
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

  return (
    <div className="flex flex-col h-full space-y-4">
      {/* System Status Card */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              System Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <span className={`h-2.5 w-2.5 rounded-full ${
                systemStatus === "operational"
                  ? "bg-emerald-500"
                  : systemStatus === "degraded"
                  ? "bg-yellow-500"
                  : "bg-red-500"
              }`} />
              <p className="text-lg font-semibold capitalize">{systemStatus}</p>
            </div>
            <p className="text-xs text-muted-foreground mt-2">Uptime: 99.98%</p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Agent Statistics Card */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.1 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Agent Statistics
            </CardTitle>
          </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 divide-x divide-border">
            <div className="px-2 text-center">
              <p className="text-2xl font-bold">{totalAgents}</p>
              <p className="text-xs text-muted-foreground">Total</p>
            </div>
            <div className="px-2 text-center">
              <p className="text-2xl font-bold">{activeAgents}</p>
              <p className="text-xs text-muted-foreground">Active</p>
            </div>
            <div className="px-2 text-center">
              <p className="text-2xl font-bold">{idleAgents}</p>
              <p className="text-xs text-muted-foreground">Idle</p>
            </div>
          </div>

            {totalAgents > 0 && (
              <div className="mt-4">
                <div className="mb-1 flex items-center justify-between text-xs">
                  <span>Idle percentage</span>
                  <span className="tabular-nums">{Math.round((idleAgents / totalAgents) * 100)}%</span>
                </div>
                <Progress value={(idleAgents / totalAgents) * 100} />
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Workflow Status */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.2 }}
      >
        <WorkflowStatus
          activeWorkflows={0}
          completedWorkflows={0}
          currentTask={undefined}
        />
      </motion.div>

      {/* Agent List */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>All Agents ({agents.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <AgentList agents={agents} loading={agentsLoading} />
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default StatsPanel;

