import React, { useState } from "react";
import { ChatWindow } from "../chat";
import { useChat } from "../../hooks";
import { Agent } from "../../types/agent";

interface AgentChatsProps {
  agents: Agent[];
}

/**
 * AgentChats component displays three chat windows for the core agents
 */
export const AgentChats: React.FC<AgentChatsProps> = ({ agents }) => {
  // Find core agents
  const driverAgent = agents.find((a) => a.type === "driver");
  const creatorAgent = agents.find((a) => a.type === "creator");
  const generatorAgent = agents.find((a) => a.type === "generator");

  // State for each agent's status
  const [driverStatus, setDriverStatus] = useState<"idle" | "working" | "waiting">("idle");
  const [creatorStatus, setCreatorStatus] = useState<"idle" | "working" | "waiting">("idle");
  const [generatorStatus, setGeneratorStatus] = useState<"idle" | "working" | "waiting">("idle");

  // Chat hooks for each agent
  const driverChat = useChat({
    agentId: driverAgent?.id || 1,
    onStatusChange: setDriverStatus,
  });

  const creatorChat = useChat({
    agentId: creatorAgent?.id || 2,
    onStatusChange: setCreatorStatus,
  });

  const generatorChat = useChat({
    agentId: generatorAgent?.id || 3,
    onStatusChange: setGeneratorStatus,
  });

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
      {/* Driver (CEO) Chat */}
      <div className="h-full min-h-[500px]">
        {driverAgent ? (
          <ChatWindow
            agentId={driverAgent.id}
            agentName={driverAgent.name}
            agentType={driverAgent.type}
            messages={driverChat.messages}
            onSendMessage={driverChat.sendMessage}
            isLoading={driverChat.isLoading}
            agentStatus={driverStatus}
          />
        ) : (
          <div className="h-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">Driver agent not found</p>
          </div>
        )}
      </div>

      {/* Creator (Researcher) Chat */}
      <div className="h-full min-h-[500px]">
        {creatorAgent ? (
          <ChatWindow
            agentId={creatorAgent.id}
            agentName={creatorAgent.name}
            agentType={creatorAgent.type}
            messages={creatorChat.messages}
            onSendMessage={creatorChat.sendMessage}
            isLoading={creatorChat.isLoading}
            agentStatus={creatorStatus}
          />
        ) : (
          <div className="h-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">Creator agent not found</p>
          </div>
        )}
      </div>

      {/* Generator (HR) Chat */}
      <div className="h-full min-h-[500px]">
        {generatorAgent ? (
          <ChatWindow
            agentId={generatorAgent.id}
            agentName={generatorAgent.name}
            agentType={generatorAgent.type}
            messages={generatorChat.messages}
            onSendMessage={generatorChat.sendMessage}
            isLoading={generatorChat.isLoading}
            agentStatus={generatorStatus}
          />
        ) : (
          <div className="h-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">Generator agent not found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentChats;

