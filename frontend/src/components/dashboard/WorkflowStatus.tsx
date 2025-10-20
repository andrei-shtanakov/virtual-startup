import React from "react";
import { motion } from "framer-motion";
import { Workflow, Zap, XCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useLive } from "@/hooks";

export interface WorkflowStats {
  active: number;
  completed: number;
  failed: number;
  currentTask?: string;
}

interface WorkflowStatusProps {
  activeWorkflows?: number;
  completedWorkflows?: number;
  currentTask?: string;
}

/**
 * WorkflowStatus component displays current workflow information with real-time updates
 */
export const WorkflowStatus: React.FC<WorkflowStatusProps> = ({
  activeWorkflows = 0,
  completedWorkflows = 0,
  currentTask,
}) => {
  // Listen to workflow stats updates via Socket.IO
  const { data: stats } = useLive<WorkflowStats>({
    event: "workflow_stats",
    initialData: {
      active: activeWorkflows,
      completed: completedWorkflows,
      failed: 0,
      currentTask,
    },
  });

  const totalWorkflows = stats.active + stats.completed + stats.failed;
  const completionRate = totalWorkflows > 0
    ? Math.round((stats.completed / totalWorkflows) * 100)
    : 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Workflow className="h-4 w-4" />
          Workflows
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Workflow counts */}
        <div className="grid grid-cols-3 gap-2">
          {/* Active */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.2 }}
            className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 text-center"
          >
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {stats.active}
            </div>
            <div className="text-xs text-blue-700 dark:text-blue-300 mt-1">
              Active
            </div>
          </motion.div>

          {/* Completed */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.2, delay: 0.05 }}
            className="p-3 bg-green-100 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800 text-center"
          >
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {stats.completed}
            </div>
            <div className="text-xs text-green-700 dark:text-green-300 mt-1">
              Done
            </div>
          </motion.div>

          {/* Failed */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.2, delay: 0.1 }}
            className="p-3 bg-red-100 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800 text-center"
          >
            <div className="text-2xl font-bold text-red-600 dark:text-red-400">
              {stats.failed}
            </div>
            <div className="text-xs text-red-700 dark:text-red-300 mt-1">
              Failed
            </div>
          </motion.div>
        </div>

        {/* Current task */}
        {stats.currentTask ? (
          <div className="p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
            <div className="flex items-start gap-2">
              <Zap className="h-4 w-4 text-yellow-600 dark:text-yellow-400 mt-0.5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-xs font-semibold text-yellow-700 dark:text-yellow-300 mb-1">
                  Current Task
                </div>
                <div className="text-sm text-yellow-900 dark:text-yellow-100 truncate">
                  {stats.currentTask}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 text-center">
            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <XCircle className="h-4 w-4" />
              <span>No active tasks</span>
            </div>
          </div>
        )}

        {/* Progress indicator */}
        {totalWorkflows > 0 && (
          <div className="space-y-2">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Success Rate</span>
              <span className="font-medium tabular-nums">{completionRate}%</span>
            </div>
            <Progress value={completionRate} />
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default WorkflowStatus;



