import React, { useState } from "react";
import { Copy, Check } from "lucide-react";
import type { Message as MessageType } from "../../types/agent";

interface MessageProps {
  message: MessageType;
  agentName?: string;
  onReaction?: (messageId: number, emoji: string) => void;
  onCopy?: (content: string) => void;
}

/**
 * Message - Minimal ChatGPT-style message component
 */
export const Message: React.FC<MessageProps> = ({ message, agentName, onCopy }) => {
  const [copied, setCopied] = useState(false);

  const isUser = message.sender === "operator";
  const timestamp = new Date(message.timestamp).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    if (onCopy) onCopy(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className={`group py-4 px-4 hover:bg-accent/30 transition-colors ${
        isUser ? "" : "bg-accent/10"
      }`}
    >
      <div className="max-w-3xl mx-auto">
        {/* Sender */}
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-7 h-7 rounded-sm bg-background border border-border flex items-center justify-center text-xs font-mono font-semibold">
            {isUser ? "U" : "A"}
          </div>

          <div className="flex-1 min-w-0">
            {/* Name & Time */}
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm font-medium text-foreground">
                {isUser ? "You" : agentName || "Agent"}
              </span>
              <span className="text-xs text-muted-foreground/70 font-mono">
                {timestamp}
              </span>
            </div>

            {/* Content */}
            <div className="text-sm text-foreground leading-relaxed whitespace-pre-wrap break-words">
              {message.content}
            </div>

            {/* Copy button (visible on hover) */}
            <div className="mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                onClick={handleCopy}
                className="inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs text-muted-foreground hover:text-foreground hover:bg-accent/50 transition-colors"
              >
                {copied ? (
                  <>
                    <Check className="h-3 w-3" />
                    <span>Copied</span>
                  </>
                ) : (
                  <>
                    <Copy className="h-3 w-3" />
                    <span>Copy</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;

