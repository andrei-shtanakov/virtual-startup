import React, { useState, useRef, KeyboardEvent } from "react";

interface TerminalInputProps {
  onSubmit: (command: string) => void;
  history: string[];
  disabled?: boolean;
}

/**
 * TerminalInput component handles user input with command history
 */
export const TerminalInput: React.FC<TerminalInputProps> = ({
  onSubmit,
  history,
  disabled = false,
}) => {
  const [input, setInput] = useState("");
  const [historyIndex, setHistoryIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = () => {
    if (input.trim() && !disabled) {
      onSubmit(input.trim());
      setInput("");
      setHistoryIndex(-1);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = historyIndex + 1;
        if (newIndex < history.length) {
          setHistoryIndex(newIndex);
          setInput(history[history.length - 1 - newIndex]);
        }
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setInput(history[history.length - 1 - newIndex]);
      } else if (historyIndex === 0) {
        setHistoryIndex(-1);
        setInput("");
      }
    } else if (e.key === "Tab") {
      e.preventDefault();
      // Auto-complete could be implemented here
    }
  };

  return (
    <div className="border-t border-gray-700 p-4 bg-gray-900">
      <div className="flex items-center gap-2 font-mono text-sm">
        <span className="text-green-400">$</span>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Type a command... (try /help)"
          className="flex-1 bg-transparent text-gray-300 outline-none placeholder-gray-600 disabled:opacity-50"
          autoFocus
        />
      </div>
      <div className="mt-2 text-xs text-gray-500">
        Press ↑/↓ for history | Type <span className="text-blue-400">/help</span> for commands
      </div>
    </div>
  );
};

export default TerminalInput;

