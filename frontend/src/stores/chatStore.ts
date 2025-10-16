import { create } from "zustand";
import { Message } from "../types/agent";

interface ChatState {
  // Messages grouped by agent ID
  messagesByAgent: Record<number, Message[]>;
  // Currently typing status
  typingAgents: Set<number>;
  // Connection status
  connected: boolean;
  // Last error
  error: string | null;
}

interface ChatStore extends ChatState {
  // Actions
  addMessage: (agentId: number, message: Message) => void;
  addMessages: (agentId: number, messages: Message[]) => void;
  setMessages: (agentId: number, messages: Message[]) => void;
  clearMessages: (agentId: number) => void;
  clearAllMessages: () => void;
  setTyping: (agentId: number, isTyping: boolean) => void;
  setConnected: (connected: boolean) => void;
  setError: (error: string | null) => void;
  getMessages: (agentId: number) => Message[];
  isAgentTyping: (agentId: number) => boolean;
}

/**
 * Chat Store - Manages chat messages and state across the application
 */
export const useChatStore = create<ChatStore>((set, get) => ({
  messagesByAgent: {},
  typingAgents: new Set(),
  connected: false,
  error: null,

  addMessage: (agentId, message) =>
    set((state) => ({
      messagesByAgent: {
        ...state.messagesByAgent,
        [agentId]: [...(state.messagesByAgent[agentId] || []), message],
      },
    })),

  addMessages: (agentId, messages) =>
    set((state) => ({
      messagesByAgent: {
        ...state.messagesByAgent,
        [agentId]: [...(state.messagesByAgent[agentId] || []), ...messages],
      },
    })),

  setMessages: (agentId, messages) =>
    set((state) => ({
      messagesByAgent: {
        ...state.messagesByAgent,
        [agentId]: messages,
      },
    })),

  clearMessages: (agentId) =>
    set((state) => {
      const newMessages = { ...state.messagesByAgent };
      delete newMessages[agentId];
      return { messagesByAgent: newMessages };
    }),

  clearAllMessages: () => set({ messagesByAgent: {} }),

  setTyping: (agentId, isTyping) =>
    set((state) => {
      const newTyping = new Set(state.typingAgents);
      if (isTyping) {
        newTyping.add(agentId);
      } else {
        newTyping.delete(agentId);
      }
      return { typingAgents: newTyping };
    }),

  setConnected: (connected) => set({ connected }),

  setError: (error) => set({ error }),

  getMessages: (agentId) => {
    const state = get();
    return state.messagesByAgent[agentId] || [];
  },

  isAgentTyping: (agentId) => {
    const state = get();
    return state.typingAgents.has(agentId);
  },
}));

