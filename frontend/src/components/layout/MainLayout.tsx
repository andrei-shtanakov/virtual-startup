import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Bot,
  MessageSquare,
  Terminal,
  LayoutDashboard,
  Menu,
  X,
  Sun,
  Moon,
  Activity
} from "lucide-react";
import { useTheme } from "@/contexts/ThemeContext";
import { useAgents } from "@/hooks";

interface MainLayoutProps {
  children: React.ReactNode;
}

/**
 * MainLayout - ChatGPT-inspired layout with sidebar navigation
 */
export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const { agents, isConnected } = useAgents();

  // Navigation items
  const navItems = [
    { path: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
    { path: "/chat", icon: MessageSquare, label: "Chat" },
    { path: "/cli", icon: Terminal, label: "CLI" },
  ];

  // Check if route is active
  const isActive = (path: string) => location.pathname === path;

  // Get agent status counts
  const activeAgents = agents.filter(a => a.status === "active").length;
  const totalAgents = agents.length;

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`
          ${sidebarOpen ? "w-64" : "w-0"}
          transition-all duration-300 ease-in-out
          bg-sidebar border-r border-sidebar-border
          flex flex-col
          overflow-hidden
        `}
      >
        {/* Sidebar Header */}
        <div className="p-4 border-b border-sidebar-border">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Bot className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <h1 className="text-sm font-semibold text-sidebar-foreground truncate">
                Virtual Startup
              </h1>
              <p className="text-xs text-muted-foreground">AI Terminal</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  flex items-center gap-3 px-3 py-2 rounded-md
                  transition-colors duration-150
                  ${active
                    ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                    : "text-muted-foreground hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
                  }
                `}
              >
                <Icon className="h-4 w-4 flex-shrink-0" />
                <span className="text-sm truncate">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Agent Status */}
        <div className="p-4 border-t border-sidebar-border space-y-3">
          {/* Connection Status */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? "bg-primary" : "bg-destructive"}`} />
              <span className="text-xs text-muted-foreground">
                {isConnected ? "Connected" : "Disconnected"}
              </span>
            </div>
            <Activity className="h-3 w-3 text-muted-foreground" />
          </div>

          {/* Agents Count */}
          <div className="flex items-center justify-between px-3 py-2 rounded-md bg-sidebar-accent/50">
            <span className="text-xs text-muted-foreground">Active Agents</span>
            <span className="text-xs font-mono font-semibold text-primary">
              {activeAgents}/{totalAgents}
            </span>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-sidebar-accent/50 hover:text-sidebar-foreground transition-colors"
          >
            {theme === "dark" ? (
              <>
                <Moon className="h-4 w-4" />
                <span className="text-sm">Dark Mode</span>
              </>
            ) : (
              <>
                <Sun className="h-4 w-4" />
                <span className="text-sm">Light Mode</span>
              </>
            )}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="h-14 border-b border-border flex items-center px-4 bg-card">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-md hover:bg-accent transition-colors"
          >
            {sidebarOpen ? (
              <X className="h-5 w-5 text-muted-foreground" />
            ) : (
              <Menu className="h-5 w-5 text-muted-foreground" />
            )}
          </button>

          {/* Current Page Title */}
          <div className="ml-4">
            <h2 className="text-sm font-medium text-foreground">
              {navItems.find(item => isActive(item.path))?.label || "Virtual Startup"}
            </h2>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
