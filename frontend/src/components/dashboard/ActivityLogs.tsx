import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Activity, Info, CheckCircle2, AlertTriangle, XCircle, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useLive } from "@/hooks";
import type { ActivityLog } from "../../types/activity";

interface ActivityLogsProps {
  maxLogs?: number;
}

/**
 * Get relative time string (e.g., "2s ago", "5m ago")
 */
const getRelativeTime = (timestamp: string): string => {
  const now = new Date();
  const past = new Date(timestamp);
  const diffMs = now.getTime() - past.getTime();
  const diffSeconds = Math.floor(diffMs / 1000);
  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);

  if (diffSeconds < 10) return "just now";
  if (diffSeconds < 60) return `${diffSeconds}s ago`;
  if (diffMinutes < 60) return `${diffMinutes}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  return past.toLocaleTimeString();
};

/**
 * Get icon for log type
 */
const getLogIcon = (type: ActivityLog["type"]) => {
  const iconClass = "h-4 w-4";
  switch (type) {
    case "success":
      return <CheckCircle2 className={iconClass} />;
    case "warning":
      return <AlertTriangle className={iconClass} />;
    case "error":
      return <XCircle className={iconClass} />;
    default:
      return <Info className={iconClass} />;
  }
};

/**
 * Get badge variant for log type
 */
const getLogVariant = (type: ActivityLog["type"]): "default" | "secondary" | "destructive" | "outline" => {
  switch (type) {
    case "success":
      return "default";
    case "warning":
      return "secondary";
    case "error":
      return "destructive";
    default:
      return "outline";
  }
};

/**
 * Get color classes for log type
 */
const getLogColors = (type: ActivityLog["type"]) => {
  switch (type) {
    case "success":
      return {
        bg: "bg-green-100 dark:bg-green-900/20",
        text: "text-green-800 dark:text-green-200",
        border: "border-green-200 dark:border-green-800",
      };
    case "warning":
      return {
        bg: "bg-yellow-100 dark:bg-yellow-900/20",
        text: "text-yellow-800 dark:text-yellow-200",
        border: "border-yellow-200 dark:border-yellow-800",
      };
    case "error":
      return {
        bg: "bg-red-100 dark:bg-red-900/20",
        text: "text-red-800 dark:text-red-200",
        border: "border-red-200 dark:border-red-800",
      };
    default:
      return {
        bg: "bg-blue-100 dark:bg-blue-900/20",
        text: "text-blue-800 dark:text-blue-200",
        border: "border-blue-200 dark:border-blue-800",
      };
  }
};

/**
 * ActivityLogs component displays real-time activity feed
 */
export const ActivityLogs: React.FC<ActivityLogsProps> = ({ maxLogs = 50 }) => {
  // Listen to activity_log events via Socket.IO
  const { data: logs, isConnected } = useLive<ActivityLog[]>({
    event: "activity_log",
    initialData: [],
    onData: (newLog: ActivityLog, currentLogs) => {
      // Prepend new log and limit to maxLogs
      return [newLog, ...currentLogs].slice(0, maxLogs);
    },
  });

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Activity className="h-4 w-4" />
            Activity Feed
          </div>
          <div className="flex items-center gap-2 text-xs font-normal text-muted-foreground">
            {isConnected ? (
              <>
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400/60"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span>Live</span>
              </>
            ) : (
              <>
                <Clock className="h-3 w-3" />
                <span>Connecting...</span>
              </>
            )}
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden">
        {logs.length === 0 ? (
          <div className="h-full flex items-center justify-center text-sm text-muted-foreground">
            No activity logs yet
          </div>
        ) : (
          <div className="h-full overflow-y-auto pr-2 space-y-2">
            <AnimatePresence initial={false}>
              {logs.map((log) => {
                const colors = getLogColors(log.type);
                return (
                  <motion.div
                    key={log.id}
                    initial={{ opacity: 0, x: -20, height: 0 }}
                    animate={{ opacity: 1, x: 0, height: "auto" }}
                    exit={{ opacity: 0, x: 20, height: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <div
                      className={`rounded-lg border p-3 ${colors.bg} ${colors.border}`}
                    >
                      <div className="flex items-start gap-2">
                        <div className={`mt-0.5 ${colors.text}`}>
                          {getLogIcon(log.type)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2 mb-1">
                            <p className={`text-sm font-medium ${colors.text}`}>
                              {log.message}
                            </p>
                            <Badge variant={getLogVariant(log.type)} className="shrink-0 uppercase text-xs">
                              {log.type}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground">
                            <span>{getRelativeTime(log.timestamp)}</span>
                            {log.agent && (
                              <>
                                <span>•</span>
                                <span className="truncate">{log.agent.name}</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ActivityLogs;
