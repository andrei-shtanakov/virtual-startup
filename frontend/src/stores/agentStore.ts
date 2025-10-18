import { create } from "zustand";
import type { Agent, AgentStatus } from "../types/agent";

interface AgentStore {
  agents: Agent[];
  selectedAgentId: number | null;
  loading: boolean;
  error: string | null;

  // Actions
  setAgents: (agents: Agent[]) => void;
  addAgent: (agent: Agent) => void;
  updateAgent: (id: number, updates: Partial<Agent>) => void;
  updateAgentStatus: (id: number, status: AgentStatus) => void;
  selectAgent: (id: number | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  getAgentById: (id: number) => Agent | undefined;
  getAgentByType: (type: string) => Agent | undefined;
}

/**
 * Agent Store - Manages agent state across the application
 */
export const useAgentStore = create<AgentStore>((set, get) => ({
  agents: [],
  selectedAgentId: null,
  loading: false,
  error: null,

  setAgents: (agents) => set({ agents, error: null }),

  addAgent: (agent) =>
    set((state) => ({
      agents: [...state.agents, agent],
    })),

  updateAgent: (id, updates) =>
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, ...updates } : agent
      ),
    })),

  updateAgentStatus: (id, status) =>
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, status } : agent
      ),
    })),

  selectAgent: (id) => set({ selectedAgentId: id }),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),

  getAgentById: (id) => {
    const state = get();
    return state.agents.find((agent) => agent.id === id);
  },

  getAgentByType: (type) => {
    const state = get();
    return state.agents.find((agent) => agent.type === type);
  },
}));

