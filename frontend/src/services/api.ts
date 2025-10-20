import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const agentService = {
  getAll: () => api.get("/agents"),
  getById: (id: number) => api.get(`/agents/${id}`),
  getMessages: (id: number) => api.get(`/agents/${id}/messages`),
  sendMessage: (id: number, message: string) =>
    api.post(`/agents/${id}/message`, { message }),
};

export const workflowService = {
  getAll: () => api.get("/workflows"),
  getById: (id: number) => api.get(`/workflows/${id}`),
  create: (data: { name: string; description?: string }) =>
    api.post("/workflows", data),
  getStatus: (id: number) => api.get(`/workflows/${id}/status`),
};

export const statsService = {
  getAgentStats: () => api.get("/stats/agents"),
  getWorkflowStats: () => api.get("/stats/workflows"),
  getOverview: () => api.get("/stats/overview"),
};

export default api;



