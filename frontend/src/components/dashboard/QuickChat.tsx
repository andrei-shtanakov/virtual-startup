import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Send, Loader2, Bot } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useLive } from "@/hooks";

export interface ChatMessage {
  id: string;
  timestamp: string;
  sender: "user" | "agent";
  agentName?: string;
  content: string;
}

interface QuickChatProps {
  maxMessages?: number;
}

/**
 * Get relative time string (e.g., "2s ago", "5m ago")
 */
const getRelativeTime = (timestamp: string): string => {
  const now = new Date();
  const past = new Date(timestamp);
  const diffMs = now.getTime() - past.getTime();
  const diffSeconds = Math.floor(diffMs / 1000);
  const diffMinutes = Math.floor(diffMs / 60000);

  if (diffSeconds < 10) return "just now";
  if (diffSeconds < 60) return `${diffSeconds}s ago`;
  if (diffMinutes < 60) return `${diffMinutes}m ago`;
  return past.toLocaleTimeString();
};

/**
 * QuickChat component provides a quick chat interface on the dashboard
 */
export const QuickChat: React.FC<QuickChatProps> = ({ maxMessages = 50 }) => {
  const [inputValue, setInputValue] = useState("");
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Listen to agent responses via Socket.IO
  const { data: messages, isConnected, emit, setData } = useLive<ChatMessage[]>({
    event: "agent_response",
    initialData: [],
    onData: (newMessage: ChatMessage, currentMessages) => {
      // Append new message and limit to maxMessages
      return [...currentMessages, newMessage].slice(-maxMessages);
    },
  });

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handle send message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || !isConnected || isSending) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      timestamp: new Date().toISOString(),
      sender: "user",
      content: inputValue.trim(),
    };

    // Optimistically add user message to UI
    setData((prev) => [...prev, userMessage].slice(-maxMessages));

    // Send to backend via Socket.IO
    console.log("📤 Sending message to backend:", userMessage.content);
    emit("send_message", {
      content: userMessage.content,
      timestamp: userMessage.timestamp,
    });

    // Clear input and set sending state
    setInputValue("");
    setIsSending(true);

    // Reset sending state after a short delay
    setTimeout(() => setIsSending(false), 500);
  };

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <MessageSquare className="h-4 w-4" />
            Quick Chat
          </div>
          {isConnected && (
            <Badge variant="outline" className="bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200 border-green-200 dark:border-green-800">
              Online
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col gap-3 overflow-hidden">
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto pr-2 space-y-3">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-sm text-muted-foreground">
              Start a conversation with your agents
            </div>
          ) : (
            <AnimatePresence initial={false}>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.sender === "user"
                        ? "bg-indigo-600 text-white"
                        : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    }`}
                  >
                    {message.sender === "agent" && message.agentName && (
                      <div className="flex items-center gap-2 mb-1">
                        <Bot className="h-3 w-3 text-indigo-600 dark:text-indigo-400" />
                        <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">
                          {message.agentName}
                        </span>
                      </div>
                    )}
                    <p className="text-sm whitespace-pre-wrap break-words">
                      {message.content}
                    </p>
                    <p
                      className={`text-xs mt-1 ${
                        message.sender === "user"
                          ? "text-indigo-200"
                          : "text-muted-foreground"
                      }`}
                    >
                      {getRelativeTime(message.timestamp)}
                    </p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isConnected ? "Type a message..." : "Connecting..."}
            disabled={!isConnected || isSending}
            className="flex-1"
          />
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || !isConnected || isSending}
            size="icon"
          >
            {isSending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default QuickChat;
