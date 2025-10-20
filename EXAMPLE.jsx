import React from "react";
import { motion } from "framer-motion";
import { BarChart3, Bot, Moon, Sun, Wifi, Activity, Rocket, Play, Pause, Trash2, Plus, Send } from "lucide-react";

/**
 * Single-file React dashboard with TailwindCSS and shadcn-like primitives.
 * Replace inline primitives with shadcn/ui imports in your app, e.g.:
 *   import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
 *   import { Button } from "@/components/ui/button";
 *   import { Badge } from "@/components/ui/badge";
 *   import { Progress } from "@/components/ui/progress";
 * This component is framework-agnostic (Vite/Next). Tailwind required.
 */

// --- Minimal shadcn-like primitives (inline for portability) ---
const cn = (...cls: (string | false | null | undefined)[]) => cls.filter(Boolean).join(" ");

function Card({ className, children }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 shadow-sm", className)}>
      {children}
    </div>
  );
}
function CardHeader({ className, children }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("px-5 pt-5", className)}>{children}</div>;
}
function CardTitle({ className, children }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("text-sm font-medium text-slate-500 dark:text-slate-400", className)}>{children}</h3>;
}
function CardContent({ className, children }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("px-5 pb-5", className)}>{children}</div>;
}
function Button({ className, children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "inline-flex items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-900 text-white dark:bg-white dark:text-slate-900 px-3 py-2 text-sm font-medium hover:opacity-90 disabled:opacity-50",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
function GhostButton({ className, children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "inline-flex items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-transparent px-3 py-2 text-sm hover:bg-slate-100 dark:hover:bg-slate-900",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
function Badge({ className, children }: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span className={cn("rounded-full border border-slate-200 dark:border-slate-800 px-2 py-0.5 text-xs", className)}>
      {children}
    </span>
  );
}
function Progress({ value }: { value: number }) {
  return (
    <div className="h-2 w-full rounded-full bg-slate-200 dark:bg-slate-800">
      <div className="h-2 rounded-full bg-indigo-500" style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
    </div>
  );
}

// --- Types ---
 type Agent = { id: number; name: string; role: string; tag: string; status: "Idle" | 
  "Working" | "Waiting" };

// --- Demo data ---
const initialAgents: Agent[] = [
  { id: 1, name: "Driver", role: "CEO & Orchestrator", tag: "DRIVER", status: "Idle" },
  { id: 2, name: "Creator", role: "Research & Ideas", tag: "CREATOR", status: "Idle" },
  { id: 3, name: "Generator", role: "HR & Agent Builder", tag: "GENERATOR", status: "Idle" },
];

export default function Dashboard() {
  const [dark, setDark] = React.useState<boolean>(true);
  const [system] = React.useState<string>("Operational");
  const [uptime] = React.useState<string>("99.98%");
  const [agents, setAgents] = React.useState<Agent[]>(initialAgents);
  const [workflows, setWorkflows] = React.useState({ active: 0, completed: 0, failed: 0 });
  const [logs, setLogs] = React.useState<string[]>(["System booted", "All agents idle"]);
  const [query, setQuery] = React.useState("");
  const [chat, setChat] = React.useState({ agentId: 1, text: "" });

  React.useEffect(() => {
    if (dark) document.documentElement.classList.add("dark");
    else document.documentElement.classList.remove("dark");
  }, [dark]);

  const activeCount = agents.filter(a => a.status !== "Idle").length;
  const idleCount = agents.filter(a => a.status === "Idle").length;
  const idlePercent = Math.round((idleCount / Math.max(1, agents.length)) * 100);

  const filtered = agents.filter(a => {
    const q = query.toLowerCase();
    return !q || a.name.toLowerCase().includes(q) || a.role.toLowerCase().includes(q);
  });

  function log(line: string) {
    setLogs(prev => [time() + " • " + line, ...prev]);
  }
  function time() {
    return new Date().toLocaleTimeString();
  }

  function toggle(agent: Agent) {
    const next = agent.status === "Idle" ? "Working" : "Idle";
    setAgents(prev => prev.map(a => (a.id === agent.id ? { ...a, status: next } : a)));
    setWorkflows(w => ({
      ...w,
      active: Math.max(0, w.active + (next === "Working" ? 1 : -1)),
      completed: w.completed + (next === "Idle" ? 1 : 0),
    }));
    log(`${agent.name}: ${next}`);
  }

  function removeAgent(id: number) {
    setAgents(prev => prev.filter(a => a.id !== id));
    log(`Agent ${id} removed`);
  }

  function addAgent() {
    const id = (agents.at(-1)?.id ?? 0) + 1;
    setAgents(prev => [...prev, { id, name: `Agent ${id}`, role: "Generic worker", tag: "AGENT", status: "Idle" }]);
    log(`Added Agent ${id}`);
  }

  function sendChat() {
    const txt = chat.text.trim();
    if (!txt) return;
    const a = agents.find(x => x.id === chat.agentId);
    log(`→ ${a?.name}: ${txt}`);
    setChat({ ...chat, text: "" });
    // TODO: wire to backend LLM/autogen
  }

  return (
    <div className="bg-slate-50 text-slate-900 dark:bg-slate-900 dark:text-slate-100 min-h-screen">
      <div className="mx-auto max-w-7xl px-4 py-6">
        {/* Top bar */}
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-2xl bg-indigo-600/10 text-indigo-600">
              <Bot className="h-5 w-5" />
            </span>
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Virtual Startup Dashboard</h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">Multi-agent AI system powered by AutoGen</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 rounded-full border border-slate-200 dark:border-slate-800 px-3 py-1.5 text-sm">
              <span className="relative inline-flex h-2.5 w-2.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400/60" />
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
              </span>
              <span>Live updates</span>
              <Wifi className="h-4 w-4" />
            </div>
            <GhostButton onClick={() => setDark(v => !v)}>
              {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              Theme: {dark ? "Light" : "Dark"}
            </GhostButton>
          </div>
        </div>

        {/* Overview */}
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>System Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mt-1 flex items-center gap-2">
                <span className={cn("h-2.5 w-2.5 rounded-full", system === "Operational" ? "bg-emerald-500" : "bg-amber-500")} />
                <p className="text-lg font-semibold">{system}</p>
              </div>
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Uptime: {uptime}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Agent Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 divide-x divide-slate-200 dark:divide-slate-800">
                <div className="px-2 text-center">
                  <p className="text-2xl font-bold">{agents.length}</p>
                  <p className="text-xs text-slate-500">Total</p>
                </div>
                <div className="px-2 text-center">
                  <p className="text-2xl font-bold">{activeCount}</p>
                  <p className="text-xs text-slate-500">Active</p>
                </div>
                <div className="px-2 text-center">
                  <p className="text-2xl font-bold">{idleCount}</p>
                  <p className="text-xs text-slate-500">Idle</p>
                </div>
              </div>
              <div className="mt-4">
                <div className="mb-1 flex items-center justify-between text-xs">
                  <span>Idle percentage</span>
                  <span className="tabular-nums">{idlePercent}%</span>
                </div>
                <Progress value={idlePercent} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Workflows</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mt-1 grid grid-cols-3 text-center">
                <div>
                  <p className="text-2xl font-bold">{workflows.active}</p>
                  <p className="text-xs text-slate-500">Active</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">{workflows.completed}</p>
                  <p className="text-xs text-slate-500">Completed</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">{workflows.failed}</p>
                  <p className="text-xs text-slate-500">Failed</p>
                </div>
              </div>
              {workflows.active === 0 && (
                <p className="mt-3 text-xs text-slate-500">No active tasks</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Agents */}
        <div className="mt-8">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold flex items-center gap-2"><Activity className="h-5 w-5"/>Agents</h2>
            <div className="flex items-center gap-2">
              <input
                placeholder="Search..."
                value={query}
                onChange={e => setQuery(e.target.value)}
                className="w-48 rounded-xl border border-slate-200 dark:border-slate-800 bg-transparent px-3 py-1.5 text-sm focus:outline-none"
              />
              <Button onClick={addAgent}><Plus className="h-4 w-4"/>Add</Button>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filtered.map(agent => (
              <motion.div key={agent.id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardContent className="pt-5">
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className={cn("inline-flex h-2.5 w-2.5 rounded-full", agent.status === "Idle" ? "bg-slate-400" : "bg-emerald-500")} />
                          <h3 className="text-base font-semibold">{agent.name}</h3>
                        </div>
                        <p className="mt-1 text-sm text-slate-500">{agent.role}</p>
                      </div>
                      <Badge>{agent.tag}</Badge>
                    </div>
                    <div className="mt-4 flex items-center gap-2">
                      <GhostButton onClick={() => toggle(agent)}>
                        {agent.status === "Idle" ? <Play className="h-4 w-4"/> : <Pause className="h-4 w-4"/>}
                        {agent.status === "Idle" ? "Start" : "Pause"}
                      </GhostButton>
                      <GhostButton className="text-rose-600 border-rose-200 dark:border-rose-800 hover:bg-rose-50 dark:hover:bg-rose-900/30" onClick={() => removeAgent(agent.id)}>
                        <Trash2 className="h-4 w-4"/>Remove
                      </GhostButton>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Activity + Quick chat */}
        <div className="mt-8 grid grid-cols-1 gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Activity</CardTitle>
                <button className="text-sm underline decoration-dotted" onClick={() => setLogs([])}>Clear</button>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 max-h-64 overflow-y-auto pr-1">
                {logs.length === 0 && (
                  <li className="text-sm text-slate-500">No events</li>
                )}
                {logs.map((line, i) => (
                  <li key={i} className="text-sm text-slate-700 dark:text-slate-300">{line}</li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4"/>
                <CardTitle>Quick ask to agent</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <select
                  value={chat.agentId}
                  onChange={e => setChat({ ...chat, agentId: Number(e.target.value) })}
                  className="w-48 rounded-xl border border-slate-200 dark:border-slate-800 bg-transparent px-3 py-2 text-sm"
                >
                  {agents.map(a => (
                    <option key={a.id} value={a.id}>{a.name}</option>
                  ))}
                </select>
                <input
                  value={chat.text}
                  onChange={e => setChat({ ...chat, text: e.target.value })}
                  onKeyDown={e => { if (e.key === "Enter") sendChat(); }}
                  placeholder="Message..."
                  className="flex-1 rounded-xl border border-slate-200 dark:border-slate-800 bg-transparent px-3 py-2 text-sm"
                />
                <Button onClick={sendChat}><Send className="h-4 w-4"/>Send</Button>
              </div>
              <p className="mt-3 text-xs text-slate-500">Wire this to your backend (AutoGen/LLM) inside <code>sendChat()</code> and <code>toggle()</code>.</p>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="mt-10 text-center text-xs text-slate-500">
          <p>React + Tailwind with shadcn-like primitives. Replace with shadcn/ui components in your app.</p>
          <p className="mt-1 inline-flex items-center gap-1"><Rocket className="h-3 w-3"/> Ready for integration.</p>
        </div>
      </div>
    </div>
  );
}
