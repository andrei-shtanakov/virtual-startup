import React, { useEffect, useRef } from "react";
import { TerminalLine } from "../../types/cli";

interface TerminalOutputProps {
  lines: TerminalLine[];
}

/**
 * TerminalOutput component displays terminal output lines
 */
export const TerminalOutput: React.FC<TerminalOutputProps> = ({ lines }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new lines are added
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [lines]);

  const getLineColor = (type: string) => {
    switch (type) {
      case "command":
        return "text-green-400";
      case "output":
        return "text-gray-300";
      case "error":
        return "text-red-400";
      case "success":
        return "text-green-400";
      case "info":
        return "text-blue-400";
      case "system":
        return "text-yellow-400";
      default:
        return "text-gray-300";
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 font-mono text-sm">
      {lines.map((line) => (
        <div key={line.id} className={`mb-1 ${getLineColor(line.type)}`}>
          {line.type === "command" && (
            <span className="text-green-400">
              <span className="text-blue-400">[{formatTime(line.timestamp)}]</span> $
            </span>
          )}{" "}
          <span className="whitespace-pre-wrap break-words">{line.content}</span>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default TerminalOutput;

