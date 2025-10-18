export interface AgentStats {
  total: number;
  active: number;
  idle: number;
}

export interface WorkflowStats {
  total: number;
  active: number;
  completed: number;
  failed?: number;
}

export interface SystemOverview {
  agents: AgentStats;
  workflows: WorkflowStats;
  status: string;
}


