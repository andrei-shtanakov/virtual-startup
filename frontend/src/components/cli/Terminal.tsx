import React, { useState, useCallback } from "react";
import type { TerminalLine, Command } from "../../types/cli";
import TerminalOutput from "./TerminalOutput";
import TerminalInput from "./TerminalInput";
import { useAgents } from "../../hooks";

// Available commands
const COMMANDS: Command[] = [
  {
    name: "/driver",
    description: "Send a message to the Driver agent (CEO)",
    usage: "/driver <message>",
  },
  {
    name: "/creator",
    description: "Send a message to the Creator agent (Researcher)",
    usage: "/creator <message>",
  },
  {
    name: "/generator",
    description: "Send a message to the Generator agent (HR Manager)",
    usage: "/generator <message>",
  },
  {
    name: "/status",
    description: "Show system status",
    usage: "/status",
  },
  {
    name: "/agents",
    description: "List all agents",
    usage: "/agents",
  },
  {
    name: "/help",
    description: "Show available commands",
    usage: "/help",
    aliases: ["/?", "/h"],
  },
  {
    name: "/clear",
    description: "Clear the terminal",
    usage: "/clear",
    aliases: ["/cls"],
  },
];

/**
 * Terminal component - main CLI interface
 */
export const Terminal: React.FC = () => {
  const [lines, setLines] = useState<TerminalLine[]>([
    {
      id: 0,
      type: "system",
      content: "Virtual Startup CLI v1.0.0",
      timestamp: new Date(),
    },
    {
      id: 1,
      type: "info",
      content: "Type /help to see available commands",
      timestamp: new Date(),
    },
  ]);
  const [history, setHistory] = useState<string[]>([]);
  const [processing, setProcessing] = useState(false);
  const { agents } = useAgents();

  const addLine = useCallback((type: TerminalLine["type"], content: string) => {
    setLines((prev) => [
      ...prev,
      {
        id: prev.length,
        type,
        content,
        timestamp: new Date(),
      },
    ]);
  }, []);

  const handleHelp = useCallback(() => {
    addLine("info", "Available commands:");
    COMMANDS.forEach((cmd) => {
      addLine("output", `  ${cmd.usage.padEnd(30)} - ${cmd.description}`);
      if (cmd.aliases && cmd.aliases.length > 0) {
        addLine("output", `    Aliases: ${cmd.aliases.join(", ")}`);
      }
    });
  }, [addLine]);

  const handleStatus = useCallback(async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/status`);
      const data = await response.json();

      addLine("success", "System Status:");
      addLine("output", `  API: ${data.api}`);
      addLine("output", `  Agents Initialized: ${data.agents_initialized}`);
      addLine("output", `  Database: ${data.database}`);
    } catch (error) {
      addLine("error", `Failed to fetch status: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }, [addLine]);

  const handleAgents = useCallback(() => {
    if (agents.length === 0) {
      addLine("info", "No agents found. Initialize agents with /init");
      return;
    }

    addLine("success", `Found ${agents.length} agent(s):`);
    agents.forEach((agent) => {
      addLine(
        "output",
        `  [${agent.id}] ${agent.name.padEnd(15)} | Type: ${agent.type.padEnd(10)} | Status: ${agent.status}`
      );
    });
  }, [agents, addLine]);

  const handleSendToAgent = useCallback(
    async (agentType: "driver" | "creator" | "generator", message: string) => {
      const agent = agents.find((a) => a.type === agentType);

      if (!agent) {
        addLine("error", `${agentType} agent not found. Initialize agents first.`);
        return;
      }

      if (!message.trim()) {
        addLine("error", "Message cannot be empty");
        return;
      }

      addLine("info", `Sending to ${agent.name}...`);
      setProcessing(true);

      try {
        // Send message via API
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/agents/${agent.id}/message`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
          }
        );

        if (!response.ok) {
          throw new Error(`API error: ${response.statusText}`);
        }

        const data = await response.json();

        addLine("success", `Response from ${agent.name}:`);
        addLine("output", data.response || "No response");
      } catch (error) {
        addLine(
          "error",
          `Failed to send message: ${error instanceof Error ? error.message : "Unknown error"}`
        );
      } finally {
        setProcessing(false);
      }
    },
    [agents, addLine]
  );

  const handleClear = useCallback(() => {
    setLines([
      {
        id: 0,
        type: "system",
        content: "Terminal cleared",
        timestamp: new Date(),
      },
    ]);
  }, []);

  const parseAndExecute = useCallback(
    async (input: string) => {
      // Add command to history
      setHistory((prev) => [...prev, input]);

      // Add command to output
      addLine("command", input);

      // Parse command
      const parts = input.trim().split(/\s+/);
      const cmd = parts[0].toLowerCase();
      const args = parts.slice(1).join(" ");

      // Execute command
      switch (cmd) {
        case "/help":
        case "/?":
        case "/h":
          handleHelp();
          break;

        case "/status":
          await handleStatus();
          break;

        case "/agents":
          handleAgents();
          break;

        case "/driver":
          await handleSendToAgent("driver", args);
          break;

        case "/creator":
          await handleSendToAgent("creator", args);
          break;

        case "/generator":
          await handleSendToAgent("generator", args);
          break;

        case "/clear":
        case "/cls":
          handleClear();
          break;

        default:
          addLine("error", `Unknown command: ${cmd}. Type /help for available commands.`);
      }
    },
    [addLine, handleHelp, handleStatus, handleAgents, handleSendToAgent, handleClear]
  );

  return (
    <div className="flex flex-col h-full bg-black rounded-lg shadow-2xl overflow-hidden border border-gray-800">
      <TerminalOutput lines={lines} />
      <TerminalInput onSubmit={parseAndExecute} history={history} disabled={processing} />
    </div>
  );
};

export default Terminal;

