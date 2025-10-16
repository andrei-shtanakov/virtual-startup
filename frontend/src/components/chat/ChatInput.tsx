import React, { useState, useRef, KeyboardEvent } from "react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

/**
 * ChatInput component for typing and sending messages
 */
export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Type your message...",
}) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSendMessage(trimmedMessage);
      setMessage("");

      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter (without Shift)
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);

    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  const characterCount = message.length;
  const maxChars = 2000;

  return (
    <div className="border-t border-gray-300 dark:border-gray-600 p-4 bg-white dark:bg-gray-800">
      <div className="flex gap-2">
        {/* Textarea */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleInput}
            onKeyDown={handleKeyPress}
            placeholder={placeholder}
            disabled={disabled}
            maxLength={maxChars}
            rows={1}
            className={`
              w-full px-3 py-2 rounded-lg border resize-none
              focus:outline-none focus:ring-2 focus:ring-blue-500
              dark:bg-gray-700 dark:border-gray-600 dark:text-white
              ${disabled ? "bg-gray-100 cursor-not-allowed" : "bg-white"}
            `}
            style={{ maxHeight: "150px", minHeight: "40px" }}
          />

          {/* Character count */}
          {characterCount > 0 && (
            <div
              className={`absolute bottom-1 right-2 text-xs ${
                characterCount > maxChars * 0.9
                  ? "text-red-500"
                  : "text-gray-400"
              }`}
            >
              {characterCount}/{maxChars}
            </div>
          )}
        </div>

        {/* Send button */}
        <button
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          className={`
            px-6 py-2 rounded-lg font-medium transition-colors
            ${
              disabled || !message.trim()
                ? "bg-gray-300 text-gray-500 cursor-not-allowed dark:bg-gray-600"
                : "bg-blue-600 text-white hover:bg-blue-700"
            }
          `}
        >
          Send
        </button>
      </div>

      {/* Helper text */}
      <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
        Press <kbd className="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">Enter</kbd> to send,{" "}
        <kbd className="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">Shift + Enter</kbd> for new line
      </div>
    </div>
  );
};

export default ChatInput;

