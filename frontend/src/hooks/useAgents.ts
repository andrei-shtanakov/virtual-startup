import { useState, useEffect } from "react";
import type { Agent } from "../types/agent";
import { socket, socketService } from "../services/socket";

interface UseAgentsReturn {
  agents: Agent[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  isConnected: boolean;
}

/**
 * Custom hook for fetching all agents from the API with real-time updates
 */
export const useAgents = (): UseAgentsReturn => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const fetchAgents = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${import.meta.env.VITE_API_URL}/agents`);

      if (!response.ok) {
        throw new Error(`Failed to fetch agents: ${response.statusText}`);
      }

      const data = await response.json();
      setAgents(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to fetch agents";
      setError(errorMessage);
      console.error("Error fetching agents:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchAgents();

    // Connect to WebSocket
    socketService.connect();

    // Subscribe to connection state
    const unsubscribe = socketService.onConnectionChange((connected) => {
      setIsConnected(connected);
    });

    // Listen for agent status updates
    const handleAgentStatusUpdate = (data: { agent_id: number; status: string; timestamp?: string }) => {
      console.log("Agent status update:", data);
      setAgents((prevAgents) =>
        prevAgents.map((agent) =>
          agent.id === data.agent_id
            ? { ...agent, status: data.status as Agent["status"], updated_at: data.timestamp || new Date().toISOString() }
            : agent
        )
      );
    };

    // Listen for new agents
    const handleAgentCreated = (agent: Agent) => {
      console.log("New agent created:", agent);
      setAgents((prevAgents) => [...prevAgents, agent]);
    };

    // Listen for agent deletion
    const handleAgentDeleted = (data: { agent_id: number }) => {
      console.log("Agent deleted:", data);
      setAgents((prevAgents) => prevAgents.filter((agent) => agent.id !== data.agent_id));
    };

    // Register event listeners
    socket.on("agent_status_update", handleAgentStatusUpdate);
    socket.on("agent_created", handleAgentCreated);
    socket.on("agent_deleted", handleAgentDeleted);

    // Cleanup
    return () => {
      unsubscribe();
      socket.off("agent_status_update", handleAgentStatusUpdate);
      socket.off("agent_created", handleAgentCreated);
      socket.off("agent_deleted", handleAgentDeleted);
    };
  }, []);

  return {
    agents,
    loading,
    error,
    refetch: fetchAgents,
    isConnected,
  };
};

export default useAgents;

