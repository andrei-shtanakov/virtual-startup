import { useState, useEffect, useCallback } from "react";
import { socket, socketService } from "../services/socket";

export interface UseLiveOptions<T> {
  /** Event name(s) to listen to */
  event: string | string[];
  /** Initial data value */
  initialData: T;
  /** Optional handler to transform incoming data */
  onData?: (data: any, current: T) => T;
  /** Whether to automatically connect socket on mount */
  autoConnect?: boolean;
}

export interface UseLiveReturn<T> {
  /** Current data state */
  data: T;
  /** Whether socket is connected */
  isConnected: boolean;
  /** Manually set data */
  setData: React.Dispatch<React.SetStateAction<T>>;
  /** Emit an event to the server */
  emit: (event: string, data?: any) => void;
  /** Force reconnect */
  reconnect: () => void;
}

/**
 * Generic hook for real-time Socket.IO updates
 *
 * @example
 * // Listen to a single event
 * const { data, isConnected } = useLive({
 *   event: "activity_log",
 *   initialData: [],
 *   onData: (log, logs) => [log, ...logs].slice(0, 100)
 * });
 *
 * @example
 * // Listen to multiple events
 * const { data, emit } = useLive({
 *   event: ["message", "typing"],
 *   initialData: { messages: [], typing: false },
 *   onData: (payload, state) => {
 *     if (payload.type === "message") return { ...state, messages: [...state.messages, payload] };
 *     if (payload.type === "typing") return { ...state, typing: payload.isTyping };
 *     return state;
 *   }
 * });
 */
export const useLive = <T>({
  event,
  initialData,
  onData,
  autoConnect = true,
}: UseLiveOptions<T>): UseLiveReturn<T> => {
  const [data, setData] = useState<T>(initialData);
  const [isConnected, setIsConnected] = useState(false);

  // Emit event to server
  const emit = useCallback((eventName: string, eventData?: any) => {
    if (socket.connected) {
      console.log(`✅ Emitting ${eventName} to server`, eventData);
      socket.emit(eventName, eventData);
    } else {
      console.warn(`Cannot emit ${eventName}: socket not connected`);
    }
  }, []);

  // Force reconnect
  const reconnect = useCallback(() => {
    socketService.reconnect();
  }, []);

  useEffect(() => {
    // Auto-connect if requested
    if (autoConnect) {
      socketService.connect();
    }

    // Subscribe to connection state
    const unsubscribe = socketService.onConnectionChange((connected) => {
      setIsConnected(connected);
    });

    // Handle incoming events
    const handleEvent = (eventData: any) => {
      if (onData) {
        setData((current) => onData(eventData, current));
      } else {
        setData(eventData);
      }
    };

    // Register event listeners
    const events = Array.isArray(event) ? event : [event];
    events.forEach((evt) => {
      socket.on(evt, handleEvent);
    });

    // Cleanup
    return () => {
      unsubscribe();
      events.forEach((evt) => {
        socket.off(evt, handleEvent);
      });
    };
  }, [event, onData, autoConnect]);

  return {
    data,
    isConnected,
    setData,
    emit,
    reconnect,
  };
};

export default useLive;
