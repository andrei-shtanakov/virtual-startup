@echo off
REM Virtual Startup - Easy launcher script for Windows
REM This script starts both backend and frontend servers

echo.
echo 🚀 Virtual Startup Launcher
echo ==============================
echo.

REM Check if we're in the project root
if not exist "backend" (
    echo ❌ Error: Please run this script from the project root directory
    exit /b 1
)
if not exist "frontend" (
    echo ❌ Error: Please run this script from the project root directory
    exit /b 1
)

REM Start backend server in new window
echo 📦 Starting backend server...
start "Backend Server" cmd /k "cd backend && uv run python run.py"

REM Wait for backend to initialize
echo ⏳ Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

REM Start frontend server in new window
echo 🎨 Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Servers started successfully!
echo.
echo 📍 Backend:  http://localhost:5000
echo 📍 Frontend: http://localhost:5173
echo.
echo 💡 Close the terminal windows to stop the servers
echo.
pause
