import React from "react";
import { Message as MessageType } from "../../types/agent";

interface MessageProps {
  message: MessageType;
  agentName?: string;
}

/**
 * Message component displays a single chat message
 */
export const Message: React.FC<MessageProps> = ({ message, agentName }) => {
  const isOperator = message.sender === "operator";
  const timestamp = new Date(message.timestamp).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div
      className={`flex ${isOperator ? "justify-end" : "justify-start"} mb-4`}
    >
      <div
        className={`max-w-[70%] rounded-lg px-4 py-2 ${
          isOperator
            ? "bg-blue-600 text-white"
            : "bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-gray-100"
        }`}
      >
        {/* Sender name */}
        <div className="text-xs font-semibold mb-1 opacity-75">
          {isOperator ? "You" : agentName || "Agent"}
        </div>

        {/* Message content */}
        <div className="text-sm whitespace-pre-wrap break-words">
          {message.content}
        </div>

        {/* Timestamp */}
        <div
          className={`text-xs mt-1 ${
            isOperator ? "text-blue-200" : "text-gray-500 dark:text-gray-400"
          }`}
        >
          {timestamp}
        </div>
      </div>
    </div>
  );
};

export default Message;

