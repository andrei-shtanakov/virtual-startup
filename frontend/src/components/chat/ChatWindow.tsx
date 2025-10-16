import React, { useEffect, useRef } from "react";
import { Message as MessageType } from "../../types/agent";
import Message from "./Message";
import ChatInput from "./ChatInput";

interface ChatWindowProps {
  agentId: number;
  agentName: string;
  agentType: "driver" | "creator" | "generator" | "dynamic";
  messages: MessageType[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  agentStatus?: "idle" | "working" | "waiting";
}

/**
 * ChatWindow component - Main chat interface for agent communication
 */
export const ChatWindow: React.FC<ChatWindowProps> = ({
  agentId,
  agentName,
  agentType,
  messages,
  onSendMessage,
  isLoading = false,
  agentStatus = "idle",
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Get agent type badge color
  const getAgentTypeColor = () => {
    switch (agentType) {
      case "driver":
        return "bg-purple-600";
      case "creator":
        return "bg-green-600";
      case "generator":
        return "bg-orange-600";
      case "dynamic":
        return "bg-blue-600";
      default:
        return "bg-gray-600";
    }
  };

  // Get status indicator
  const getStatusIndicator = () => {
    switch (agentStatus) {
      case "working":
        return (
          <span className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400">
            <span className="animate-pulse">●</span> Working
          </span>
        );
      case "waiting":
        return (
          <span className="flex items-center gap-2 text-orange-600 dark:text-orange-400">
            <span>●</span> Waiting
          </span>
        );
      case "idle":
      default:
        return (
          <span className="flex items-center gap-2 text-green-600 dark:text-green-400">
            <span>●</span> Idle
          </span>
        );
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gray-100 dark:bg-gray-900 px-4 py-3 border-b border-gray-300 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Agent type badge */}
            <span
              className={`${getAgentTypeColor()} text-white text-xs font-bold px-2 py-1 rounded uppercase`}
            >
              {agentType}
            </span>

            {/* Agent name */}
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {agentName}
            </h3>
          </div>

          {/* Status indicator */}
          <div className="text-sm font-medium">{getStatusIndicator()}</div>
        </div>

        {/* Agent ID */}
        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          Agent ID: {agentId}
        </div>
      </div>

      {/* Messages area */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-2"
        style={{ minHeight: "200px" }}
      >
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
            <div className="text-center">
              <p className="text-lg mb-2">💬</p>
              <p>No messages yet</p>
              <p className="text-sm mt-1">
                Start a conversation with {agentName}
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <Message
                key={msg.id}
                message={msg}
                agentName={agentName}
              />
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-200 dark:bg-gray-700 rounded-lg px-4 py-2">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                    </div>
                    <span className="text-sm text-gray-600 dark:text-gray-300">
                      {agentName} is thinking...
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input area */}
      <ChatInput
        onSendMessage={onSendMessage}
        disabled={isLoading}
        placeholder={`Message ${agentName}...`}
      />
    </div>
  );
};

export default ChatWindow;

