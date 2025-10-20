export type AgentType = "driver" | "creator" | "generator" | "dynamic";
export type AgentStatus = "idle" | "working" | "waiting";
export type MessageSender = "agent" | "operator" | "system";

export interface Agent {
  id: number;
  name: string;
  type: AgentType;
  role: string;
  status: AgentStatus;
  config?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

export interface Message {
  id: number;
  agent_id: number;
  sender: MessageSender;
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

