#!/bin/bash

# Virtual Startup - Easy launcher script
# This script starts both backend and frontend servers

set -e  # Exit on error

echo "🚀 Virtual Startup Launcher"
echo "=============================="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill 0  # Kill all processes in the process group
    exit 0
}

# Register cleanup on script exit
trap cleanup SIGINT SIGTERM

# Check if we're in the project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Start backend server
echo "📦 Starting backend server..."
cd backend
uv run python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start frontend server
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servers started successfully!"
echo ""
echo "📍 Backend:  http://localhost:5000"
echo "📍 Frontend: http://localhost:5173"
echo ""
echo "💡 Press Ctrl+C to stop all servers"
echo ""

# Wait for all background jobs
wait
