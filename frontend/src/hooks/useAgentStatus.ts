import { useState, useEffect, useRef } from "react";
import { Socket } from "socket.io-client";
import { socket } from "../services/socket";

interface AgentStatusData {
  agent_id: number;
  status: "idle" | "working" | "waiting" | "busy";
  name?: string;
  role?: string;
  type?: string;
}

interface UseAgentStatusReturn {
  status: "idle" | "working" | "waiting";
  isConnected: boolean;
  requestStatus: () => void;
}

/**
 * Custom hook for subscribing to agent status updates
 */
export const useAgentStatus = (agentId: number): UseAgentStatusReturn => {
  const [status, setStatus] = useState<"idle" | "working" | "waiting">("idle");
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<Socket>(socket);

  useEffect(() => {
    const currentSocket = socketRef.current;

    // Connection handlers
    const handleConnect = () => {
      console.log(`AgentStatus: Connected for agent ${agentId}`);
      setIsConnected(true);

      // Request current status on connect
      currentSocket.emit("agent_status_request", { agent_id: agentId });
    };

    const handleDisconnect = () => {
      console.log(`AgentStatus: Disconnected for agent ${agentId}`);
      setIsConnected(false);
    };

    // Status handler
    const handleAgentStatus = (data: AgentStatusData) => {
      if (data.agent_id === agentId) {
        // Map 'busy' to 'working'
        const mappedStatus = data.status === "busy" ? "working" : data.status;

        if (mappedStatus === "idle" || mappedStatus === "working" || mappedStatus === "waiting") {
          setStatus(mappedStatus);
        }
      }
    };

    // Register event listeners
    currentSocket.on("connect", handleConnect);
    currentSocket.on("disconnect", handleDisconnect);
    currentSocket.on("agent_status", handleAgentStatus);

    // Connect if not already connected
    if (!currentSocket.connected) {
      currentSocket.connect();
    } else {
      // If already connected, request status immediately
      currentSocket.emit("agent_status_request", { agent_id: agentId });
    }

    // Cleanup
    return () => {
      currentSocket.off("connect", handleConnect);
      currentSocket.off("disconnect", handleDisconnect);
      currentSocket.off("agent_status", handleAgentStatus);
    };
  }, [agentId]);

  // Function to manually request status
  const requestStatus = () => {
    if (isConnected) {
      socketRef.current.emit("agent_status_request", { agent_id: agentId });
    }
  };

  return {
    status,
    isConnected,
    requestStatus,
  };
};

export default useAgentStatus;



