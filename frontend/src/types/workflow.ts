export type WorkflowStatus = "active" | "completed" | "failed";
export type TaskStatus = "pending" | "in_progress" | "completed" | "failed";

export interface Workflow {
  id: number;
  name: string;
  description?: string;
  status: WorkflowStatus;
  started_at: string;
  completed_at?: string;
  metadata?: Record<string, unknown>;
}

export interface Task {
  id: number;
  workflow_id: number;
  assigned_to?: number;
  status: TaskStatus;
  description: string;
  result?: string;
  created_at: string;
  completed_at?: string;
}

