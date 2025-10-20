import { io, Socket } from "socket.io-client";

const SOCKET_URL = import.meta.env.VITE_API_URL?.replace("/api", "") || "http://localhost:5000";

// Reconnection configuration
const RECONNECTION_ATTEMPTS = 5;
const RECONNECTION_DELAY = 3000;

// Connection state callbacks
type ConnectionCallback = (connected: boolean) => void;
const connectionCallbacks: Set<ConnectionCallback> = new Set();

// Initialize socket instance with reconnection config
export const socket: Socket = io(SOCKET_URL, {
  autoConnect: false,
  transports: ["websocket", "polling"],
  reconnection: true,
  reconnectionAttempts: RECONNECTION_ATTEMPTS,
  reconnectionDelay: RECONNECTION_DELAY,
  reconnectionDelayMax: 10000,
  timeout: 20000,
});

let reconnectAttempt = 0;
let isConnected = false;

// Notify all listeners of connection state changes
const notifyConnectionChange = (connected: boolean) => {
  isConnected = connected;
  connectionCallbacks.forEach((callback) => callback(connected));
};

// Setup event listeners
socket.on("connect", () => {
  console.log("✅ Socket connected:", socket.id);
  reconnectAttempt = 0;
  notifyConnectionChange(true);
});

socket.on("connection_response", (data) => {
  console.log("📨 Received connection_response:", data);
});

socket.on("disconnect", (reason) => {
  console.log("❌ Socket disconnected:", reason);
  notifyConnectionChange(false);

  // Auto-reconnect on certain disconnect reasons
  if (reason === "io server disconnect") {
    // Server initiated disconnect, reconnect manually
    socket.connect();
  }
});

socket.on("connect_error", (error) => {
  console.error("⚠️ Socket connection error:", error);
  console.error("Error details:", {
    message: error.message,
    type: error.type,
    description: error.description,
    context: error.context,
  });
  reconnectAttempt++;

  if (reconnectAttempt >= RECONNECTION_ATTEMPTS) {
    console.error("❌ Max reconnection attempts reached");
  }
});

socket.on("reconnect", (attemptNumber) => {
  console.log(`🔄 Socket reconnected after ${attemptNumber} attempt(s)`);
  reconnectAttempt = 0;
});

socket.on("reconnect_attempt", (attemptNumber) => {
  console.log(`🔄 Reconnection attempt ${attemptNumber}/${RECONNECTION_ATTEMPTS}`);
});

socket.on("reconnect_error", (error) => {
  console.error("⚠️ Reconnection error:", error.message);
});

socket.on("reconnect_failed", () => {
  console.error("❌ Reconnection failed - all attempts exhausted");
});

socket.on("error", (error) => {
  console.error("Socket error:", error);
});

// Helper functions
export const socketService = {
  /**
   * Connect to the socket server
   */
  connect: () => {
    if (!socket.connected) {
      console.log("Connecting to socket server...");
      socket.connect();
    }
  },

  /**
   * Disconnect from the socket server
   */
  disconnect: () => {
    if (socket.connected) {
      console.log("Disconnecting from socket server...");
      socket.disconnect();
    }
  },

  /**
   * Check if socket is connected
   */
  isConnected: () => isConnected,

  /**
   * Subscribe to connection state changes
   */
  onConnectionChange: (callback: ConnectionCallback) => {
    connectionCallbacks.add(callback);
    // Immediately call with current state
    callback(isConnected);
    
    // Return unsubscribe function
    return () => {
      connectionCallbacks.delete(callback);
    };
  },

  /**
   * Get current connection status with details
   */
  getStatus: () => ({
    connected: socket.connected,
    id: socket.id,
    reconnecting: reconnectAttempt > 0,
    reconnectAttempt,
    maxAttempts: RECONNECTION_ATTEMPTS,
  }),

  /**
   * Force reconnection
   */
  reconnect: () => {
    console.log("Forcing reconnection...");
    reconnectAttempt = 0;
    if (socket.connected) {
      socket.disconnect();
    }
    socket.connect();
  },
};

export default socket;
