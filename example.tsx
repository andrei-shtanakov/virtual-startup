// App.tsx
import { useState } from "react";

type Agent = { name: string; role: string; active: boolean };

const AGENTS: Agent[] = [
  { name: "Driver", role: "CEO and Task Orchestrator", active: false },
  { name: "Creator", role: "Researcher and Idea Generator", active: false },
  { name: "Generator", role: "HR Manager and Agent Creator", active: true },
];

export default function App() {
  const [tab, setTab] = useState<"chat" | "cli">("chat");
  const [filter, setFilter] = useState("");

  const filtered = AGENTS.filter(a =>
    (a.name + a.role).toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="h-screen w-screen overflow-hidden bg-neutral-50 text-neutral-900 dark:bg-neutral-900 dark:text-neutral-100">
      {/* Top bar */}
      <header className="flex items-center justify-between border-b border-neutral-200 bg-white/60 px-4 py-2 backdrop-blur dark:border-neutral-800 dark:bg-neutral-900/60">
        <h1 className="text-lg font-semibold">Virtual Startup</h1>
        <div className="text-xs opacity-70">System: Operational</div>
      </header>

      {/* Grid layout */}
      <div className="grid h-[calc(100vh-48px)] grid-cols-[minmax(240px,320px)_1fr] grid-rows-[1fr_minmax(160px,auto)] gap-3 p-3">
        {/* Sidebar: Agents */}
        <aside className="row-span-2 overflow-hidden rounded-xl border border-neutral-200 bg-white p-3 shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-sm font-semibold">Agents</h2>
            <span className="text-xs opacity-60">
              Active: {AGENTS.filter(a => a.active).length}/{AGENTS.length}
            </span>
          </div>

          <input
            aria-label="Filter agents"
            className="mb-2 w-full rounded-lg border border-neutral-200 bg-neutral-50 px-2 py-1 text-sm outline-none focus:ring dark:border-neutral-700 dark:bg-neutral-900"
            placeholder="Filter…"
            value={filter}
            onChange={e => setFilter(e.target.value)}
          />

          <div className="h-[calc(100%-70px)] overflow-auto pr-1">
            <table className="w-full border-collapse text-sm">
              <thead className="sticky top-0 z-10 bg-white text-xs text-neutral-500 dark:bg-neutral-950">
                <tr>
                  <th className="w-2"></th>
                  <th className="py-2 text-left font-medium">Agent</th>
                  <th className="py-2 text-left font-medium">Role</th>
                  <th className="py-2 text-left font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(a => (
                  <tr
                    key={a.name}
                    className="border-t border-neutral-100 hover:bg-neutral-50 dark:border-neutral-800 dark:hover:bg-neutral-900"
                  >
                    <td className="pl-1">
                      <span
                        className={`inline-block h-2 w-2 rounded-full ${
                          a.active ? "bg-emerald-500" : "bg-neutral-400"
                        }`}
                        aria-label={a.active ? "active" : "idle"}
                        title={a.active ? "Active" : "Idle"}
                      />
                    </td>
                    <td className="truncate py-2 pr-2 font-medium">{a.name}</td>
                    <td className="max-w-0 truncate py-2 pr-2 text-neutral-600 dark:text-neutral-300">
                      {a.role}
                    </td>
                    <td className="py-2 pr-2">{a.active ? "Active" : "Idle"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </aside>

        {/* Main: Chat / CLI tabs */}
        <main className="overflow-hidden rounded-xl border border-neutral-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <div className="flex items-center gap-2 border-b border-neutral-200 px-3 py-2 text-sm dark:border-neutral-800">
            <button
              onClick={() => setTab("chat")}
              className={`rounded-md px-3 py-1 ${
                tab === "chat"
                  ? "bg-neutral-900 text-white dark:bg-neutral-100 dark:text-neutral-900"
                  : "hover:bg-neutral-100 dark:hover:bg-neutral-900"
              }`}
            >
              Chat
            </button>
            <button
              onClick={() => setTab("cli")}
              className={`rounded-md px-3 py-1 ${
                tab === "cli"
                  ? "bg-neutral-900 text-white dark:bg-neutral-100 dark:text-neutral-900"
                  : "hover:bg-neutral-100 dark:hover:bg-neutral-900"
              }`}
            >
              CLI
            </button>
            <div className="ml-auto text-xs opacity-60">Live</div>
          </div>

          {tab === "chat" ? <ChatPanel /> : <CliPanel />}
        </main>

        {/* Bottom: Activity log or compact CLI */}
        <section className="overflow-auto rounded-xl border border-neutral-200 bg-white p-3 text-sm shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <h3 className="mb-2 text-sm font-semibold">Activity Feed</h3>
          <ul className="space-y-1 text-neutral-600 dark:text-neutral-300">
            <li>No activity yet.</li>
          </ul>
        </section>
      </div>
    </div>
  );
}

function ChatPanel() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-auto p-3">
        <div className="text-sm opacity-60">Start a conversation…</div>
      </div>
      <form
        className="flex gap-2 border-t border-neutral-200 p-3 dark:border-neutral-800"
        onSubmit={e => e.preventDefault()}
      >
        <input
          className="flex-1 rounded-lg border border-neutral-200 bg-neutral-50 px-3 py-2 text-sm outline-none focus:ring dark:border-neutral-700 dark:bg-neutral-900"
          placeholder="Type a message…"
        />
        <button
          className="rounded-lg bg-neutral-900 px-4 py-2 text-sm text-white hover:opacity-90 dark:bg-neutral-100 dark:text-neutral-900"
          type="submit"
        >
          Send
        </button>
      </form>
    </div>
  );
}

function CliPanel() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-auto p-3 font-mono text-sm">
        $ Type /help to see available commands
      </div>
      <form
        className="flex gap-2 border-t border-neutral-200 p-3 dark:border-neutral-800"
        onSubmit={e => e.preventDefault()}
      >
        <input
          className="flex-1 rounded-lg border border-neutral-200 bg-neutral-50 px-3 py-2 font-mono text-sm outline-none focus:ring dark:border-neutral-700 dark:bg-neutral-900"
          placeholder="Type a command…"
        />
        <button
          className="rounded-lg bg-neutral-900 px-4 py-2 text-sm text-white hover:opacity-90 dark:bg-neutral-100 dark:text-neutral-900"
          type="submit"
        >
          Run
        </button>
      </form>
    </div>
  );
}
