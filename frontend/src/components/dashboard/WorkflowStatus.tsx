import React from "react";

interface WorkflowStatusProps {
  activeWorkflows?: number;
  completedWorkflows?: number;
  currentTask?: string;
}

/**
 * WorkflowStatus component displays current workflow information
 */
export const WorkflowStatus: React.FC<WorkflowStatusProps> = ({
  activeWorkflows = 0,
  completedWorkflows = 0,
  currentTask,
}) => {
  return (
    <div className="space-y-4">
      {/* Workflow counts */}
      <div className="grid grid-cols-2 gap-3">
        {/* Active */}
        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {activeWorkflows}
          </div>
          <div className="text-xs text-blue-700 dark:text-blue-300 mt-1">
            Active Workflows
          </div>
        </div>

        {/* Completed */}
        <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
            {completedWorkflows}
          </div>
          <div className="text-xs text-green-700 dark:text-green-300 mt-1">
            Completed
          </div>
        </div>
      </div>

      {/* Current task */}
      {currentTask ? (
        <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
          <div className="flex items-start gap-2">
            <span className="text-yellow-600 dark:text-yellow-400 mt-0.5 flex-shrink-0">
              ⚡
            </span>
            <div className="flex-1 min-w-0">
              <div className="text-xs font-semibold text-yellow-700 dark:text-yellow-300 mb-1">
                Current Task
              </div>
              <div className="text-sm text-yellow-900 dark:text-yellow-100">
                {currentTask}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 text-center">
          <div className="text-sm text-gray-500 dark:text-gray-400">
            No active tasks
          </div>
        </div>
      )}

      {/* Progress indicator */}
      {activeWorkflows > 0 && (
        <div className="space-y-2">
          <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400">
            <span>Workflow Progress</span>
            <span>{Math.round((completedWorkflows / (activeWorkflows + completedWorkflows)) * 100)}%</span>
          </div>
          <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-600 dark:bg-blue-500 transition-all duration-500"
              style={{
                width: `${(completedWorkflows / (activeWorkflows + completedWorkflows)) * 100}%`,
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default WorkflowStatus;


