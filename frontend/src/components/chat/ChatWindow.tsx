import React, { useEffect, useRef } from "react";
import type { Message as MessageType } from "../../types/agent";
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
  const [showScrollButton, setShowScrollButton] = React.useState(false);

  // Handle message reaction
  const handleReaction = (messageId: number, emoji: string) => {
    console.log(`Reaction added to message ${messageId}: ${emoji}`);
    // In a real app, you would send this to the backend
    // For now, just log it
  };

  // Handle message copy
  const handleCopy = (content: string) => {
    console.log("Message copied:", content.substring(0, 50) + "...");
  };

  // Scroll to bottom function
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Check scroll position to show/hide "Jump to bottom" button
  const handleScroll = () => {
    if (messagesContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current;
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;
      setShowScrollButton(!isNearBottom && messages.length > 0);
    }
  };

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
          <span className="flex items-center gap-1.5 text-primary">
            <span className="animate-pulse text-xs">●</span>
            <span className="text-xs">Working</span>
          </span>
        );
      case "waiting":
        return (
          <span className="flex items-center gap-1.5 text-chart-2">
            <span className="text-xs">●</span>
            <span className="text-xs">Waiting</span>
          </span>
        );
      case "idle":
      default:
        return (
          <span className="flex items-center gap-1.5 text-muted-foreground">
            <span className="text-xs">●</span>
            <span className="text-xs">Idle</span>
          </span>
        );
    }
  };

  return (
    <div className="flex flex-col h-full bg-background border border-border rounded-lg overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-card">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Agent info */}
            <h3 className="text-sm font-semibold text-foreground">
              {agentName}
            </h3>
            <span className="text-xs font-mono text-muted-foreground uppercase">
              {agentType}
            </span>
          </div>

          {/* Status indicator */}
          <div className="text-xs font-medium">{getStatusIndicator()}</div>
        </div>
      </div>

      {/* Messages area */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto relative bg-background"
        style={{ minHeight: "200px" }}
        onScroll={handleScroll}
      >
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <div className="text-center space-y-2">
              <p className="text-sm">No messages yet</p>
              <p className="text-xs">
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
                onReaction={handleReaction}
                onCopy={handleCopy}
              />
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="py-4 px-4 bg-accent/10">
                <div className="max-w-3xl mx-auto">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-7 h-7 rounded-sm bg-background border border-border flex items-center justify-center text-xs font-mono font-semibold">
                      A
                    </div>
                    <div className="flex items-center gap-2 pt-1">
                      <div className="flex gap-1">
                        <span className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                        <span className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                        <span className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        Thinking...
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </>
        )}

        {/* Jump to bottom button */}
        {showScrollButton && (
          <button
            onClick={scrollToBottom}
            className="absolute bottom-4 right-4 bg-primary hover:bg-primary/90 text-primary-foreground rounded-full p-2 shadow-lg transition-all hover:scale-105 z-10"
            title="Jump to bottom"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 14l-7 7m0 0l-7-7m7 7V3"
              />
            </svg>
          </button>
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

