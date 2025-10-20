/**
 * Activity log entry type
 */
export interface ActivityLog {
  id: string;
  timestamp: string;
  type: "info" | "success" | "warning" | "error";
  message: string;
  agent?: {
    id: number;
    name: string;
  };
  metadata?: Record<string, any>;
}

export type ActivityLogType = ActivityLog["type"];
