import React, { useState } from "react";
import { ChatWindow } from "../components/chat";
import { useChat } from "../hooks";

/**
 * ChatDemo page - Test the chat interface with a single agent
 */
export const ChatDemo: React.FC = () => {
  const [selectedAgent, setSelectedAgent] = useState({
    id: 1,
    name: "Driver",
    type: "driver" as const,
  });

  const [agentStatus, setAgentStatus] = useState<"idle" | "working" | "waiting">("idle");

  const { messages, sendMessage, isConnected, isLoading, error } = useChat({
    agentId: selectedAgent.id,
    onStatusChange: setAgentStatus,
  });

  // Mock agents for selector
  const availableAgents = [
    { id: 1, name: "Driver (CEO)", type: "driver" as const },
    { id: 2, name: "Creator (Researcher)", type: "creator" as const },
    { id: 3, name: "Generator (HR)", type: "generator" as const },
  ];

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            💬 Chat Interface Demo
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Test the chat interface with AI agents
          </p>
        </div>

        {/* Connection status */}
        <div className="mb-4 flex items-center gap-4">
          <div
            className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
              isConnected
                ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
            }`}
          >
            <span>{isConnected ? "●" : "○"}</span>
            <span className="font-medium">
              {isConnected ? "Connected" : "Disconnected"}
            </span>
          </div>

          {/* Agent selector */}
          <select
            value={selectedAgent.id}
            onChange={(e) => {
              const agent = availableAgents.find(
                (a) => a.id === Number(e.target.value)
              );
              if (agent) {
                setSelectedAgent(agent);
              }
            }}
            className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          >
            {availableAgents.map((agent) => (
              <option key={agent.id} value={agent.id}>
                {agent.name}
              </option>
            ))}
          </select>
        </div>

        {/* Error message */}
        {error && (
          <div className="mb-4 p-4 bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 rounded-lg">
            <p className="text-red-800 dark:text-red-200 font-medium">
              ⚠️ Error: {error}
            </p>
          </div>
        )}

        {/* Chat window */}
        <div className="h-[600px]">
          <ChatWindow
            agentId={selectedAgent.id}
            agentName={selectedAgent.name}
            agentType={selectedAgent.type}
            messages={messages}
            onSendMessage={sendMessage}
            isLoading={isLoading}
            agentStatus={agentStatus}
          />
        </div>

        {/* Info panel */}
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
          <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
            ℹ️ How to use:
          </h3>
          <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
            <li>• Select an agent from the dropdown above</li>
            <li>• Type a message in the input field at the bottom</li>
            <li>• Press Enter to send (Shift+Enter for new line)</li>
            <li>• Watch the agent status indicator (Idle/Working/Waiting)</li>
            <li>• Messages are auto-saved and persist on reload</li>
          </ul>
        </div>

        {/* Debug info */}
        <details className="mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <summary className="cursor-pointer font-semibold text-gray-900 dark:text-white">
            🐛 Debug Info
          </summary>
          <div className="mt-2 text-xs text-gray-700 dark:text-gray-300 font-mono">
            <p>Agent ID: {selectedAgent.id}</p>
            <p>Agent Name: {selectedAgent.name}</p>
            <p>Agent Type: {selectedAgent.type}</p>
            <p>Connected: {String(isConnected)}</p>
            <p>Loading: {String(isLoading)}</p>
            <p>Status: {agentStatus}</p>
            <p>Messages: {messages.length}</p>
            <p>API URL: {import.meta.env.VITE_API_URL}</p>
          </div>
        </details>
      </div>
    </div>
  );
};

export default ChatDemo;

