import React from "react";
import { Terminal } from "../components/cli";

/**
 * CLI page - Terminal-style interface for interacting with agents
 */
export const CLI: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">
            🖥️ Command Line Interface
          </h1>
          <p className="text-gray-400">
            Interact with AI agents using terminal commands
          </p>
        </div>

        {/* Terminal */}
        <div className="h-[calc(100vh-180px)]">
          <Terminal />
        </div>

        {/* Info */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-blue-400 mb-2">
              🎯 Quick Start
            </h3>
            <ul className="text-xs text-gray-300 space-y-1">
              <li>• Type <code className="text-green-400">/help</code> to see all commands</li>
              <li>• Use <code className="text-green-400">/driver</code>, <code className="text-green-400">/creator</code>, or <code className="text-green-400">/generator</code></li>
              <li>• Check status with <code className="text-green-400">/status</code></li>
            </ul>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-yellow-400 mb-2">
              ⌨️ Keyboard Shortcuts
            </h3>
            <ul className="text-xs text-gray-300 space-y-1">
              <li>• <kbd className="px-1 bg-gray-700 rounded">↑</kbd> / <kbd className="px-1 bg-gray-700 rounded">↓</kbd> - Navigate history</li>
              <li>• <kbd className="px-1 bg-gray-700 rounded">Enter</kbd> - Execute command</li>
              <li>• <kbd className="px-1 bg-gray-700 rounded">Ctrl+L</kbd> - Clear (use /clear)</li>
            </ul>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-green-400 mb-2">
              💡 Examples
            </h3>
            <ul className="text-xs text-gray-300 space-y-1">
              <li><code className="text-green-400">/driver Help me build an API</code></li>
              <li><code className="text-green-400">/creator Research Python frameworks</code></li>
              <li><code className="text-green-400">/agents</code></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CLI;



