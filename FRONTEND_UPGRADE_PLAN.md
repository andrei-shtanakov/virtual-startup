# Frontend Upgrade Plan — React + shadcn/ui + Live Updates

Purpose: align the redesigned dashboard with your stack (React + TS + Vite + Tailwind + shadcn/ui) and wire live updates via Socket.IO.

---

## 1) Project structure

Place files as follows:

```
frontend/
  src/
    pages/
      Dashboard.tsx
    components/
      AgentCard.tsx
    hooks/
      useLive.ts
    services/
      api.ts
    types/
      agents.ts
    App.tsx
  .env
  index.html
  vite.config.ts
```

---

## 2) Install packages

```bash
# UI + icons + motion
npm i lucide-react framer-motion

# Networking
npm i axios socket.io-client

# shadcn/ui dependencies (if not already added)
npm i class-variance-authority clsx tailwind-merge @radix-ui/react-slot
npx shadcn@latest init
# then generate components you need:
npx shadcn@latest add card button badge progress input label select
```

---

## 3) Environment

`.env`:

```dotenv
VITE_API_URL=http://localhost:5000/api
```

`VITE_API_URL` should point to your Flask API base; Socket.IO will use the same origin without `/api` suffix.

---

## 4) Types

`src/types/agents.ts`

```ts
export type AgentStatus = "Idle" | "Working" | "Waiting";

export interface Agent {
  id: number;
  name: string;
  role: string;
  tag: string;
  status: AgentStatus;
}
```

---

## 5) API service

`src/services/api.ts`

```ts
import axios from "axios";

export const API_URL = import.meta.env.VITE_API_URL as string;

export const api = axios.create({
  baseURL: API_URL,
  timeout: 15000,
});

// Example endpoints
export const agentsApi = {
  list: () => api.get("/agents"),
  start: (id: number) => api.post(`/agents/${id}/start`),
  pause: (id: number) => api.post(`/agents/${id}/pause`),
  remove: (id: number) => api.delete(`/agents/${id}`),
  create: (payload: Partial<{ name: string; role: string }>) =>
    api.post("/agents", payload),
};
```

---

## 6) Live updates hook (Socket.IO)

`src/hooks/useLive.ts`

```ts
import { useEffect, useMemo, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";
import type { Agent } from "@/types/agents";
import { API_URL } from "@/services/api";

type Events = {
  log: (msg: string) => void;
  agent_status: (data: { id: number; status: Agent["status"] }) => void;
  workflow: (data: { active: number; completed: number; failed: number }) => void;
};

function baseSocketUrl() {
  // Strip trailing /api if present
  try {
    const url = new URL(API_URL);
    url.pathname = url.pathname.replace(/\\/?api\\/?$/, "/");
    return url.origin;
  } catch {
    return "http://localhost:5000";
  }
}

export function useLive() {
  const [logs, setLogs] = useState<string[]>([]);
  const [workflows, setWorkflows] = useState({ active: 0, completed: 0, failed: 0 });
  const socketRef = useRef<Socket<Events> | null>(null);

  const url = useMemo(() => baseSocketUrl(), []);

  useEffect(() => {
    const s = io(url, { transports: ["websocket"] });
    socketRef.current = s;

    s.on("log", (msg) => setLogs((p) => [msg, ...p]));
    s.on("workflow", (w) => setWorkflows(w));

    return () => {
      s.close();
      socketRef.current = null;
    };
  }, [url]);

  return { logs, workflows, socket: socketRef };
}
```

Back end should emit events: `log`, `agent_status`, `workflow`.

---

## 7) Replace inline primitives with shadcn/ui

**Before** (inline):

```tsx
function Card({ children }) {
  return <div className="rounded-2xl border ...">{children}</div>;
}
```

**After** (shadcn/ui):

```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
```

Update JSX accordingly and remove the inline primitive definitions.

---

## 8) Dashboard page (TSX)

`src/pages/Dashboard.tsx`

```tsx
import React from "react";
import { motion } from "framer-motion";
import { Bot, Wifi, Sun, Moon, Play, Pause, Trash2, Plus, Send } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";
import type { Agent } from "@/types/agents";
import { agentsApi } from "@/services/api";
import { useLive } from "@/hooks/useLive";

const initialAgents: Agent[] = [
  { id: 1, name: "Driver", role: "CEO & Orchestrator", tag: "DRIVER", status: "Idle" },
  { id: 2, name: "Creator", role: "Research & Ideas", tag: "CREATOR", status: "Idle" },
  { id: 3, name: "Generator", role: "HR & Agent Builder", tag: "GENERATOR", status: "Idle" },
];

export default function Dashboard() {
  const [dark, setDark] = React.useState(true);
  const [system] = React.useState("Operational");
  const [uptime] = React.useState("99.98%");
  const [agents, setAgents] = React.useState<Agent[]>(initialAgents);
  const [query, setQuery] = React.useState("");
  const [chat, setChat] = React.useState({ agentId: 1, text: "" });

  const { logs, workflows } = useLive();

  React.useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const activeCount = agents.filter((a) => a.status !== "Idle").length;
  const idleCount = agents.length - activeCount;
  const idlePercent = Math.round((idleCount / Math.max(1, agents.length)) * 100);

  const filtered = agents.filter((a) => {
    const q = query.toLowerCase();
    return !q || a.name.toLowerCase().includes(q) || a.role.toLowerCase().includes(q);
  });

  async function toggle(agent: Agent) {
    const next = agent.status === "Idle" ? "Working" : "Idle";
    setAgents((prev) => prev.map((a) => (a.id === agent.id ? { ...a, status: next } : a)));
    try {
      if (next === "Working") await agentsApi.start(agent.id);
      else await agentsApi.pause(agent.id);
    } catch {}
  }

  async function removeAgent(id: number) {
    setAgents((prev) => prev.filter((a) => a.id !== id));
    try { await agentsApi.remove(id); } catch {}
  }

  async function addAgent() {
    const id = (agents.at(-1)?.id ?? 0) + 1;
    const created = { id, name: `Agent ${id}`, role: "Generic worker", tag: "AGENT", status: "Idle" as const };
    setAgents((p) => [...p, created]);
    try { await agentsApi.create({ name: created.name, role: created.role }); } catch {}
  }

  function sendChat() {
    if (!chat.text.trim()) return;
    // TODO: call your backend endpoint to dispatch a message to the selected agent
    setChat((c) => ({ ...c, text: "" }));
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
            <Button variant="ghost" onClick={() => setDark((v) => !v)}>
              {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              Theme: {dark ? "Light" : "Dark"}
            </Button>
          </div>
        </div>

        {/* Overview */}
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Card>
            <CardHeader><CardTitle>System Status</CardTitle></CardHeader>
            <CardContent>
              <div className="mt-1 flex items-center gap-2">
                <span className={\"h-2.5 w-2.5 rounded-full \" + (system === \"Operational\" ? \"bg-emerald-500\" : \"bg-amber-500\")} />
                <p className="text-lg font-semibold">{system}</p>
              </div>
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Uptime: {uptime}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle>Agent Statistics</CardTitle></CardHeader>
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
            <CardHeader><CardTitle>Workflows</CardTitle></CardHeader>
            <CardContent>
              <div className="mt-1 grid grid-cols-3 text-center">
                <div><p className="text-2xl font-bold">{workflows.active}</p><p className="text-xs text-slate-500">Active</p></div>\n                <div><p className="text-2xl font-bold">{workflows.completed}</p><p className="text-xs text-slate-500">Completed</p></div>\n                <div><p className="text-2xl font-bold">{workflows.failed}</p><p className="text-xs text-slate-500">Failed</p></div>\n              </div>\n              {workflows.active === 0 && (<p className=\"mt-3 text-xs text-slate-500\">No active tasks</p>)}\n            </CardContent>\n          </Card>\n        </div>\n\n        {/* Agents */}\n        <div className=\"mt-8\">\n          <div className=\"mb-3 flex items-center justify-between\">\n            <h2 className=\"text-lg font-semibold\">Agents</h2>\n            <div className=\"flex items-center gap-2\">\n              <Input placeholder=\"Search...\" value={query} onChange={(e) => setQuery(e.target.value)} className=\"w-48\" />\n              <Button onClick={addAgent}><Plus className=\"h-4 w-4\"/>Add</Button>\n            </div>\n          </div>\n          <div className=\"grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3\">\n            {filtered.map((agent) => (\n              <motion.div key={agent.id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>\n                <Card>\n                  <CardContent className=\"pt-5\">\n                    <div className=\"flex items-start justify-between gap-2\">\n                      <div>\n                        <div className=\"flex items-center gap-2\">\n                          <span className={\"inline-flex h-2.5 w-2.5 rounded-full \" + (agent.status === \"Idle\" ? \"bg-slate-400\" : \"bg-emerald-500\")} />\n                          <h3 className=\"text-base font-semibold\">{agent.name}</h3>\n                        </div>\n                        <p className=\"mt-1 text-sm text-slate-500\">{agent.role}</p>\n                      </div>\n                      <Badge>{agent.tag}</Badge>\n                    </div>\n                    <div className=\"mt-4 flex items-center gap-2\">\n                      <Button variant=\"ghost\" onClick={() => toggle(agent)}>\n                        {agent.status === \"Idle\" ? <Play className=\"h-4 w-4\"/> : <Pause className=\"h-4 w-4\"/>}\n                        {agent.status === \"Idle\" ? \"Start\" : \"Pause\"}\n                      </Button>\n                      <Button variant=\"ghost\" className=\"text-rose-600\" onClick={() => removeAgent(agent.id)}>\n                        <Trash2 className=\"h-4 w-4\"/>Remove\n                      </Button>\n                    </div>\n                  </CardContent>\n                </Card>\n              </motion.div>\n            ))}\n          </div>\n        </div>\n\n        {/* Activity + Quick chat */}\n        <div className=\"mt-8 grid grid-cols-1 gap-4 lg:grid-cols-2\">\n          <Card>\n            <CardHeader>\n              <div className=\"flex items-center justify-between\">\n                <CardTitle>Activity</CardTitle>\n                <button className=\"text-sm underline decoration-dotted\" onClick={() => window.dispatchEvent(new Event('clear-logs'))}>Clear</button>\n              </div>\n            </CardHeader>\n            <CardContent>\n              {/* You can render logs from useLive here */}\n            </CardContent>\n          </Card>\n\n          <Card>\n            <CardHeader><CardTitle>Quick ask to agent</CardTitle></CardHeader>\n            <CardContent>\n              <div className=\"flex gap-2\">\n                <select\n                  value={chat.agentId}\n                  onChange={(e) => setChat({ ...chat, agentId: Number(e.target.value) })}\n                  className=\"w-48 rounded-xl border border-slate-200 dark:border-slate-800 bg-transparent px-3 py-2 text-sm\"\n                >\n                  {agents.map((a) => (<option key={a.id} value={a.id}>{a.name}</option>))}\n                </select>\n                <Input\n                  value={chat.text}\n                  onChange={(e) => setChat({ ...chat, text: e.target.value })}\n                  onKeyDown={(e) => { if (e.key === 'Enter') sendChat(); }}\n                  placeholder=\"Message...\"\n                  className=\"flex-1\"\n                />\n                <Button onClick={sendChat}><Send className=\"h-4 w-4\"/>Send</Button>\n              </div>\n              <p className=\"mt-3 text-xs text-slate-500\">Wire this to your backend (AutoGen/LLM) inside <code>sendChat()</code> and <code>toggle()</code>.</p>\n            </CardContent>\n          </Card>\n        </div>\n      </div>\n    </div>\n  );\n}\n```

---

## 9) Routing

`src/App.tsx`:

```tsx
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Dashboard from "@/pages/Dashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path=\"/\" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## 10) Linting and formatting

```bash
npm i -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin prettier eslint-config-prettier eslint-plugin-react
```

Enable `\"strict\": true` in `tsconfig.json`.

---

## 11) Acceptance checklist

- [ ] TSX components in `src/pages` and `src/components`.
- [ ] shadcn/ui primitives replace inline primitives.
- [ ] `api.ts` uses `VITE_API_URL`.
- [ ] `useLive.ts` subscribes to `log`, `agent_status`, `workflow`.
- [ ] Dark mode toggle works.
- [ ] Build runs with `npm run dev` and `npm run build`.

---

## 12) Dev commands

```bash
npm run dev     # start Vite dev server
npm run build   # production build
npm run lint    # lint
npm run preview # preview production build
```
