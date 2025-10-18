# WebSocket Fix - Backend Handler Registration Issue

## Problem Summary

The WebSocket handlers in the backend were not receiving connections or messages from the frontend, even though:
- Frontend showed "Socket connected"
- Handlers appeared to be registered
- No error messages were displayed

## Root Cause

**Flask's auto-reloader in debug mode** was creating child processes that didn't properly re-register Socket.IO event handlers. When Flask detected file changes and reloaded with `* Restarting with stat`, the WebSocket handlers weren't being re-attached to the new process.

## The Fix

### 1. Disabled Flask Auto-Reloader (`backend/run.py`)

**File**: `backend/run.py:38-42`

```python
# Disable Flask's reloader in debug mode to prevent WebSocket handler issues
# The reloader creates a child process which doesn't properly re-register Socket.IO handlers
use_reloader = os.environ.get('FLASK_USE_RELOADER', 'false').lower() == 'true'

socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True, use_reloader=use_reloader)
```

**Why this works**: By default (`use_reloader=False`), Flask won't create child processes, so Socket.IO handlers remain properly registered throughout the server's lifetime.

**Optional**: Set `FLASK_USE_RELOADER=true` environment variable to enable reloader if needed, but this may cause WebSocket issues.

### 2. Ensured Proper Handler Registration Order (`backend/app/__init__.py`)

**File**: `backend/app/__init__.py:40-47`

```python
# Initialize Socket.IO first
socketio.init_app(app)

# Then register socket handlers AFTER Socket.IO is initialized with the app
# This ensures the decorators have access to the fully configured socketio instance
from app.sockets import register_socketio_handlers

register_socketio_handlers()
```

**Why this matters**: Socket.IO must be initialized with the Flask app **before** importing the handler modules, so the `@socketio.on()` decorators can properly attach to the configured instance.

## Verification

After the fix, you should see these logs when a client connects:

**Frontend Console**:
```
✅ Socket connected: Y1P7JY074ju0HWp0AAAB
WebSocket connected
```

**Backend Logs**:
```
🔌 Client connected: Y1P7JY074ju0HWp0AAAB
💬 Received message for agent 1: Hi
```

Notice the matching Socket IDs between frontend and backend!

## Files Modified

### Backend
1. **`backend/run.py`**
   - Added `use_reloader` parameter (disabled by default)
   - Added environment variable support for optional reloader

2. **`backend/app/__init__.py`**
   - Reordered initialization: `socketio.init_app()` before handler registration
   - Added explanatory comments

3. **`backend/app/sockets/chat_socket.py`**
   - Added emoji indicators for better log visibility:
     - `🔌 Client connected`
     - `💬 Received message`

### No Frontend Changes Required
The frontend code was already correct. The issue was entirely on the backend.

## Testing Checklist

- [x] Backend starts without "Restarting with stat" message
- [x] Frontend shows "✅ Socket connected" with socket ID
- [x] Backend logs "🔌 Client connected" with matching socket ID
- [x] Sending a message shows "💬 Received message" in backend logs
- [x] Agent responds to messages through WebSocket
- [x] No "Agent system not initialized" errors

## Known Issues

### AsyncIO Task Warning
You may see this warning in the logs:
```
Task was destroyed but it is pending!
task: <Task pending name='Task-5' coro=<<async_generator_athrow without __name__>()>>
```

This is a known issue with AutoGen's async generator cleanup and doesn't affect functionality. It will be addressed in a future update.

## Development Workflow

### Starting the Application

**Option 1: Easy Way (Recommended)**
```bash
./start.sh          # macOS/Linux
start.bat           # Windows
```

**Option 2: Manual Way**
```bash
# Terminal 1 - Backend
cd backend
uv run python run.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Important: No Manual Initialization Required
The agents are now **automatically initialized** when the backend starts. You no longer need to run:
```bash
curl -X POST http://localhost:5000/api/init  # ❌ NOT NEEDED ANYMORE
```

## Summary

**Problem**: Flask's reloader broke WebSocket handler registration
**Solution**: Disable auto-reloader by default (`use_reloader=False`)
**Result**: WebSocket connections now work reliably
**Status**: ✅ **FIXED AND TESTED**

---

*Last Updated: October 18, 2025*
