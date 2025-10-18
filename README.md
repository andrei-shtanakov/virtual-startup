# Virtual Startup

A multi-agent system for virtual startup management using AutoGen agents. The system features three core AI agents (Driver, Creator, Generator) that collaborate to manage tasks, research ideas, and dynamically create specialized agents as needed.

## Overview

Virtual Startup is an AI-powered platform where autonomous agents work together to help you manage and execute startup tasks. The system provides both a web interface and CLI for interacting with the agents.

### Core Agents

1. **Driver Agent (CEO)** - Orchestrates tasks and coordinates between agents
2. **Creator Agent (Researcher)** - Researches topics and generates ideas using RAG and MCP tools
3. **Generator Agent (HR)** - Creates specialized agents on-demand based on task requirements

### Features

- 🤖 Multi-agent orchestration with AutoGen
- 💬 Real-time chat interface with agents
- 🔍 Research capabilities with RAG (ChromaDB)
- 🛠️ MCP integration for enhanced agent capabilities
- 🌐 Web UI and CLI interfaces
- 📊 Workflow tracking and monitoring
- 🔄 Dynamic agent creation

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed system architecture.

```
Human Operator (Web/CLI)
    ↓
Driver Agent (CEO)
    ├─→ Creator Agent (Research & Ideas)
    └─→ Generator Agent (Dynamic Agent Creation)
            └─→ Dynamic Agents (Task-specific)
```

## Technology Stack

**Backend:**
- Python 3.12
- Flask
- AutoGen (pyautogen)
- SQLAlchemy
- Flask-SocketIO
- ChromaDB

**Frontend:**
- React 18
- TypeScript
- Vite
- TailwindCSS
- Socket.IO Client

## 🚀 Quick Start

**Get running in under 2 minutes!**

### Easy Way (Recommended)

```bash
# Install dependencies (first time only)
cd backend && uv sync && cd ..
cd frontend && npm install && cd ..

# Start everything with one command!
./start.sh        # macOS/Linux
start.bat         # Windows
```

The launcher will:
- ✅ Start the backend server (http://localhost:5000)
- ✅ Auto-initialize the agent system
- ✅ Start the frontend server (http://localhost:5173)

Then open your browser to http://localhost:5173

### Manual Way

```bash
# Backend (Terminal 1)
cd backend
uv sync
uv run python run.py  # Agents auto-initialize on startup!

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# Open http://localhost:5173
```

See [QUICKSTART.md](QUICKSTART.md) for:
- Detailed setup instructions
- Testing guide
- Troubleshooting tips
- Usage examples

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- uv (Python package manager) - [Install](https://github.com/astral-sh/uv)
- npm

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd virtual-startup
```

### 2. Backend Setup

```bash
cd backend

# Dependencies are already managed by uv
# The dependencies are installed in the workspace .venv

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys (OpenAI, Anthropic, etc.)

# Database is already initialized and migrated
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env if needed (default points to http://localhost:5000/api)
```

## Running the Application

### Option 1: Easy Launcher (Recommended)

```bash
./start.sh        # macOS/Linux
start.bat         # Windows
```

This will automatically:
- Start the backend on http://localhost:5000
- Initialize the agent system
- Start the frontend on http://localhost:5173

### Option 2: Manual Start

**Start Backend:**

```bash
cd backend
uv run python run.py
```

The backend will start on `http://localhost:5000` and agents will auto-initialize.

**Start Frontend:**

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### Access the Application

Open your browser and navigate to `http://localhost:5173`

You'll see two main pages:
- **Dashboard** - View agent status and system statistics
- **Chat Demo** - Interact with agents in real-time

## Project Structure

```
virtual-startup/
├── backend/                 # Flask backend
│   ├── app/
│   │   ├── __init__.py     # Flask app factory
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── agents/         # AutoGen agents
│   │   ├── sockets/        # WebSocket handlers
│   │   └── utils/          # Utilities
│   ├── migrations/         # Database migrations
│   ├── tests/              # Tests
│   ├── config.py           # Configuration
│   └── run.py              # Entry point
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom hooks
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utilities
│   └── public/            # Static assets
│
└── docs/                  # Documentation
    ├── architecture.md    # System architecture
    ├── agents.md          # Agent specifications
    └── api.md             # API documentation
```

## Usage

### Web Interface

1. Start the servers using `./start.sh` (macOS/Linux) or `start.bat` (Windows)
2. Open `http://localhost:5173` in your browser
3. **Dashboard** - View agent status, system statistics, and quick navigation
4. **Chat Demo** - Interact with agents in real-time
   - Select an agent (Driver, Creator, or Generator)
   - Type your message and press Enter to send
   - Watch agent responses appear in real-time

### CLI Interface

Navigate to the CLI tab in the web interface for terminal-style interaction:

```
/driver <message>    - Send message to Driver agent
/creator <message>   - Send message to Creator agent
/generator <message> - Send message to Generator agent
/status              - Show system status
/agents              - List all agents
/help                - Show available commands
```

## Development

### Backend Development

```bash
cd backend

# Run development server (IMPORTANT: Use run.py for WebSocket support)
uv run python run.py  # NOT "flask run"

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Type checking
pyrefly check
```

**Note**: Always use `uv run python run.py` instead of `flask run` because the WebSocket functionality requires the SocketIO server initialization in `run.py`.

### Frontend Development

```bash
cd frontend

# Run development server
npm run dev

# Build for production
npm run build

# Type checking
npm run typecheck

# Linting
npm run lint
```

### Database Migrations

```bash
cd backend

# Create migration
FLASK_APP=app uv run flask db migrate -m "Description"

# Apply migration
FLASK_APP=app uv run flask db upgrade

# Downgrade
FLASK_APP=app uv run flask db downgrade
```

## Documentation

- [Architecture](docs/architecture.md) - System architecture overview
- [Agents](docs/agents.md) - Agent specifications and behaviors
- [API](docs/api.md) - REST API and WebSocket documentation

## Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///virtual_startup.db
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173

# LLM API Keys
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

### Frontend Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:5000/api
```

## Development Status

### ✅ Phase 1: Project Setup & Foundation (Complete)

- [x] Project structure created
- [x] Backend initialized with uv
- [x] Frontend initialized with Vite + React + TypeScript
- [x] Database models and migrations
- [x] Basic API endpoints
- [x] WebSocket support
- [x] Documentation

### ✅ Phase 2: Core Infrastructure (Complete)

- [x] Database schema design
- [x] SQLAlchemy models (Agent, Message, Workflow, Task)
- [x] Database migrations
- [x] Configuration setup
- [x] Environment variables

### ✅ Phase 3: Agent System (AutoGen) (Complete)

- [x] Base agent framework
- [x] Agent configuration with system prompts
- [x] **Driver Agent** - CEO/orchestrator
- [x] **Creator Agent** - Researcher with RAG
- [x] **Generator Agent** - Dynamic agent creator
- [x] Agent Manager (singleton)
- [x] RAG integration with ChromaDB
- [x] Test suite (6 tests)

### ✅ Phase 4: Backend - API & Communication (Complete)

- [x] Agent service integration layer
- [x] REST API endpoints (9 endpoints)
  - Send messages to agents
  - Create dynamic agents
  - Get agent status and history
- [x] WebSocket integration (7 events)
  - Real-time agent communication
  - Status broadcasting
- [x] Background task processing
- [x] System initialization endpoints
- [x] Test suite (8 tests)

### ✅ Phase 6: Frontend - Chat Interface (Complete)

- [x] Chat components (Message, ChatInput, ChatWindow)
- [x] Custom React hooks (useChat, useAgentStatus)
- [x] Real-time WebSocket integration
- [x] Agent status indicators
- [x] Message history loading
- [x] Keyboard shortcuts (Enter to send)
- [x] Auto-resizing input
- [x] Character count (2000 limit)
- [x] Dark mode support
- [x] Demo page with agent selector
- [x] Full TypeScript typing
- [x] Responsive design

### ✅ Phase 7: Frontend - Dashboard View (Complete)

- [x] Main dashboard page with 4-column grid
- [x] AgentChats component (3 simultaneous chat windows)
  - Driver (CEO), Creator (Researcher), Generator (HR)
  - Independent WebSocket connections
  - Separate status tracking
- [x] StatsPanel component
  - System status indicator
  - Agent statistics (total, active, idle)
  - Workflow status display
  - Agent list with real-time updates
- [x] Custom hooks (useAgents, useStats)
  - Auto-refresh every 5-10 seconds
  - Error handling
- [x] Navigation between Dashboard and Chat Demo
- [x] Responsive design (mobile, tablet, desktop)
- [x] Beautiful card-based UI
- [x] Dark mode support

### ✅ Phase 8: Frontend - CLI Interface (Complete)

- [x] Terminal component with command system
  - 7 built-in commands (driver, creator, generator, status, agents, help, clear)
  - Command aliases support
  - Async command execution
- [x] TerminalOutput component
  - Color-coded output (command, output, error, success, info, system)
  - Timestamps
  - Auto-scroll
- [x] TerminalInput component
  - Command history navigation (↑/↓ arrows)
  - Keyboard shortcuts
  - Disabled state during processing
- [x] CLI page with terminal interface
  - Info cards (quick start, shortcuts, examples)
  - Dark theme
- [x] Full API integration
- [x] Error handling

### ✅ Phase 9: Integration & Workflow (Complete)

- [x] Workflow Orchestration Service (backend)
  - End-to-end workflow execution
  - Multi-agent collaboration
  - Result aggregation
  - Error handling
- [x] Workflow API endpoints
  - POST `/api/workflows/execute` - Execute complete workflow
  - POST `/api/workflows/{id}/start` - Start workflow
  - GET `/api/workflows/{id}/status` - Get status
- [x] State Management with Zustand
  - Agent store (agentStore.ts)
  - Chat store (chatStore.ts)
  - Workflow store (workflowStore.ts)
- [x] WebSocket Reconnection Logic
  - Auto-reconnect (max 5 attempts)
  - Exponential backoff (3s → 10s)
  - Connection callbacks
  - Status tracking
- [x] Integration Tests
  - 6 comprehensive tests
  - System status, agents, workflows
  - Agent collaboration
  - Error handling
- [x] Database persistence
- [x] Real-time WebSocket updates

### ✅ Phase 10: Testing (Complete)

- [x] **Test Infrastructure**
  - Pytest configuration
  - Fixtures (app, client, db_session, samples)
  - Mock configuration for autogen/chromadb
  - In-memory SQLite database
- [x] **Model Tests** (10 tests)
  - Agent, Message, Workflow, Task models
  - Creation, serialization, relationships
- [x] **API Tests** (23 tests)
  - Agent endpoints (11 tests)
  - Workflow endpoints (12 tests)
  - Error cases, validation
- [x] **Service Tests** (11 tests, 4 skipped)
  - Workflow orchestrator
  - RAG service (singleton)
  - Agent service (singleton)
  - Task processor
- [x] **Edge Case Tests** (23 tests)
  - Null/empty values
  - Invalid inputs
  - Special characters
  - Concurrent operations
  - Error handling
- [x] **Test Suite Stats**
  - 67 total tests
  - 57 passing ✅
  - 4 skipped ⏭️
  - 43% code coverage
  - <1s execution time

### 🚧 Next Phases

- [ ] Phase 5: Frontend UI Layout (full React Router, header, sidebar)
- [ ] Phase 11: Polish & Documentation
- [ ] Phase 12: Deployment

See [TODO.md](TODO.md) for detailed roadmap.

### 📄 Documentation

- [TODO.md](TODO.md) - Single source of truth for roadmap and phase status
- [DEFERRED_FEATURES.md](DEFERRED_FEATURES.md) - Deferred items and rationale
- [QUICKSTART.md](QUICKSTART.md) - Run and test the app locally

## Contributing

This is a development project. Contributions and suggestions are welcome!

## License

[Add your license here]

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Status:** Phase 10 Complete ✅ | Full-Stack AI Agent System with Comprehensive Testing 🧪 | In Active Development 🚧

