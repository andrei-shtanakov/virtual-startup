import { useState, useEffect, useCallback, useRef } from "react";
import { Socket } from "socket.io-client";
import { socket } from "../services/socket";
import { Message } from "../types/agent";

interface UseChatProps {
  agentId: number;
  onStatusChange?: (status: "idle" | "working" | "waiting") => void;
}

interface UseChatReturn {
  messages: Message[];
  sendMessage: (content: string) => void;
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  clearMessages: () => void;
}

/**
 * Custom hook for managing chat with an agent via WebSocket
 */
export const useChat = ({ agentId, onStatusChange }: UseChatProps): UseChatReturn => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<Socket>(socket);

  // Load messages from API on mount
  useEffect(() => {
    const loadMessages = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/agents/${agentId}/messages?limit=50`
        );

        if (response.ok) {
          const data = await response.json();
          setMessages(data);
        }
      } catch (err) {
        console.error("Failed to load messages:", err);
      }
    };

    loadMessages();
  }, [agentId]);

  // WebSocket connection management
  useEffect(() => {
    const currentSocket = socketRef.current;

    // Connection handlers
    const handleConnect = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
      setError(null);
    };

    const handleDisconnect = () => {
      console.log("WebSocket disconnected");
      setIsConnected(false);
    };

    const handleConnectError = (err: Error) => {
      console.error("WebSocket connection error:", err);
      setError("Failed to connect to server");
      setIsConnected(false);
    };

    // Message handlers
    const handleAgentResponse = (data: {
      agent_id: number;
      message: string;
      sender: "agent";
      agent_name: string;
    }) => {
      if (data.agent_id === agentId) {
        setIsLoading(false);

        // Add agent message to state
        const newMessage: Message = {
          id: Date.now(), // Temporary ID
          agent_id: agentId,
          sender: "agent",
          content: data.message,
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, newMessage]);
      }
    };

    const handleAgentStatus = (data: {
      agent_id: number;
      status: "idle" | "working" | "waiting" | "busy";
    }) => {
      if (data.agent_id === agentId) {
        // Map 'busy' to 'working'
        const status = data.status === "busy" ? "working" : data.status;

        if (status === "working") {
          setIsLoading(true);
        } else {
          setIsLoading(false);
        }

        // Call status change callback
        if (onStatusChange && (status === "idle" || status === "working" || status === "waiting")) {
          onStatusChange(status);
        }
      }
    };

    const handleError = (data: { error: string; agent_id?: number }) => {
      if (!data.agent_id || data.agent_id === agentId) {
        console.error("WebSocket error:", data.error);
        setError(data.error);
        setIsLoading(false);
      }
    };

    // Register event listeners
    currentSocket.on("connect", handleConnect);
    currentSocket.on("disconnect", handleDisconnect);
    currentSocket.on("connect_error", handleConnectError);
    currentSocket.on("agent_response", handleAgentResponse);
    currentSocket.on("agent_status", handleAgentStatus);
    currentSocket.on("error", handleError);

    // Connect if not already connected
    if (!currentSocket.connected) {
      currentSocket.connect();
    }

    // Cleanup
    return () => {
      currentSocket.off("connect", handleConnect);
      currentSocket.off("disconnect", handleDisconnect);
      currentSocket.off("connect_error", handleConnectError);
      currentSocket.off("agent_response", handleAgentResponse);
      currentSocket.off("agent_status", handleAgentStatus);
      currentSocket.off("error", handleError);
    };
  }, [agentId, onStatusChange]);

  // Send message function
  const sendMessage = useCallback(
    (content: string) => {
      if (!isConnected) {
        setError("Not connected to server");
        return;
      }

      if (!content.trim()) {
        return;
      }

      // Add user message to state immediately
      const userMessage: Message = {
        id: Date.now(),
        agent_id: agentId,
        sender: "operator",
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      // Send via WebSocket
      socketRef.current.emit("send_message", {
        agent_id: agentId,
        message: content.trim(),
      });
    },
    [agentId, isConnected]
  );

  // Clear messages function
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    sendMessage,
    isConnected,
    isLoading,
    error,
    clearMessages,
  };
};

export default useChat;

