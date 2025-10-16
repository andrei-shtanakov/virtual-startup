# Quick Start Guide

Get the Virtual Startup AI Agent System running in 5 minutes!

---

## 📋 Prerequisites

- **Python 3.12+** 
- **Node.js 18+** and npm
- **uv** (Python package manager) - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## 🚀 Quick Setup & Run

### 1. Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Install dependencies (uv handles everything)
uv sync

# Set up environment (optional - app works without API keys)
cp .env.example .env
# Edit .env and add your API keys if you want to use real LLMs

# Initialize database
uv run flask db upgrade

# Initialize the 3 core agents (Driver, Creator, Generator)
uv run python init_agents.py

# Start backend server
uv run python run.py
```

Backend will start at **http://localhost:5000**

---

### 2. Frontend Setup (1 minute)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend dev server
npm run dev
```

Frontend will start at **http://localhost:5173**

---

## 🎯 Access the Application

Open your browser and go to:

**http://localhost:5173**

You'll see three navigation options:

1. **Dashboard** - View 3 agent chats simultaneously + stats
2. **CLI** - Terminal-style interface for direct agent commands
3. **Chat Demo** - Single-agent chat interface

---

## 🧪 Running Tests

### Backend Tests (57 tests)

```bash
cd backend

# Run all tests
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_models.py -v
```

**Expected:** 57 passing ✅, 4 skipped ⏭️

### Integration Tests

```bash
cd backend

# Make sure backend is running first!
# Then in another terminal:
python test_workflow_integration.py
```

**Expected:** 6/6 tests passing ✅

---

## 💡 Usage Examples

### Dashboard View
1. Click **Dashboard** button
2. See 3 chat windows (Driver, Creator, Generator)
3. Type messages to any agent
4. View real-time stats panel

### CLI Interface
1. Click **CLI** button
2. Try these commands:
   ```
   /help                     # Show all commands
   /agents                   # List all agents
   /driver "Create a blog"   # Send task to Driver
   /status                   # System status
   /clear                    # Clear terminal
   ```

### Chat Demo
1. Click **Chat Demo** button
2. Select an agent from dropdown
3. Chat with one agent at a time

---

## 🔧 API Endpoints

Backend API is available at **http://localhost:5000/api**

### Key Endpoints

```bash
# Initialize agent system
POST http://localhost:5000/api/init

# Check status
GET http://localhost:5000/api/status

# List agents
GET http://localhost:5000/api/agents

# Send message to agent
POST http://localhost:5000/api/agents/{id}/message
Body: {"message": "Your message here"}

# Execute workflow
POST http://localhost:5000/api/workflows/execute
Body: {"task": "Build a Python REST API"}

# Get statistics
GET http://localhost:5000/api/stats/overview
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
flask run --port 5001
```

**Database errors:**
```bash
# Reset database
rm backend/virtual_startup.db
uv run flask db upgrade
uv run python init_agents.py
```

**Module not found:**
```bash
cd backend
uv sync  # Re-sync dependencies
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Frontend will auto-suggest alternative port
# Or kill process:
lsof -ti:5173 | xargs kill -9
```

**Connection error:**
- Make sure backend is running on port 5000
- Check `.env` file: `VITE_API_URL=http://localhost:5000/api`

**Node modules issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🌟 Features to Try

### 1. Multi-Agent Collaboration
```bash
# In Dashboard, send to Driver:
"Research Python web frameworks and create a specialist agent to compare them"

# Watch as:
# - Driver analyzes the task
# - Creator researches using RAG
# - Generator creates a specialist agent
# - Results flow back
```

### 2. Workflow Execution
```bash
# Via API:
curl -X POST http://localhost:5000/api/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a blog platform with user authentication"}'

# Returns workflow with 3 steps showing agent collaboration
```

### 3. Real-time Updates
```bash
# Open Dashboard in 2 browser windows
# Send message in one window
# See real-time update in both windows via WebSocket
```

### 4. CLI Commands
```bash
/driver "Plan a mobile app project"
/creator "Research React Native vs Flutter"
/generator "Design a mobile developer agent"
/status  # See system health
```

---

## 📊 What You Should See

### Backend Console
```
 * Running on http://127.0.0.1:5000
 * Environment: development
 * Debug mode: on
✅ Socket connected: <socket_id>
```

### Frontend Console
```
✅ Socket connected: <socket_id>
🔄 Reconnection attempt 1/5  (if connection drops)
```

### Test Output
```
===== 57 passed, 4 skipped in 0.36s =====
Coverage: 43%
```

---

## 📚 Next Steps

1. ✅ **Run the app** - Follow steps above
2. 📖 **Read architecture** - See [PHASE3_COMPLETE.md](PHASE3_COMPLETE.md)
3. 🧪 **Run tests** - `uv run pytest tests/ -v`
4. 🔧 **Try API** - Use Postman or curl
5. 🎨 **Explore UI** - Try all 3 interfaces

---

## 🆘 Getting Help

- **Check logs** - Backend prints detailed logs
- **Browser console** - Frontend logs WebSocket events
- **Documentation** - See [README.md](README.md)
- **Phase docs** - See PHASE*_COMPLETE.md files

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Backend
cd backend && uv run python run.py          # Start server
uv run pytest tests/ -v                     # Run tests
uv run flask db upgrade                     # Update database
uv run python init_agents.py                # Reset agents

# Frontend
cd frontend && npm run dev                  # Start dev server
npm run build                               # Build for production
npm run lint                                # Check linting

# Both
# Terminal 1: cd backend && uv run python run.py
# Terminal 2: cd frontend && npm run dev
# Browser: http://localhost:5173
```

---

**Time to first run:** ~5 minutes  
**Time to first test:** ~7 minutes  
**Time to first chat:** ~6 minutes

🎉 **Enjoy exploring the AI Agent System!**

---

*Last Updated: October 16, 2025*
