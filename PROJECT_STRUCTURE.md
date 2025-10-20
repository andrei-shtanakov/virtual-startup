# Virtual Startup - Project Structure

## Overview
CLI-based AI agent management system using Python, Flask, and Textual TUI.

## Directory Structure

```
virtual-startup/
├── .git/                    # Git repository
├── .venv/                   # Python virtual environment (managed by uv)
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── uv.lock                 # UV dependency lock file
│
├── backend/                # All application code
│   ├── app/
│   │   ├── __init__.py    # Flask app factory
│   │   ├── agents/        # AI agent implementations
│   │   │   ├── base_agent.py
│   │   │   ├── driver.py      # CEO agent
│   │   │   ├── creator.py     # Research agent
│   │   │   ├── generator.py   # Agent creator
│   │   │   └── manager.py
│   │   ├── models/        # Database models
│   │   │   ├── agent.py
│   │   │   ├── message.py
│   │   │   ├── task.py
│   │   │   └── workflow.py
│   │   ├── routes/        # API endpoints
│   │   │   ├── agent_routes.py
│   │   │   ├── workflow_routes.py
│   │   │   └── stats_routes.py
│   │   ├── services/      # Business logic
│   │   │   ├── agent_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── task_processor.py
│   │   │   └── workflow_orchestrator.py
│   │   └── utils/         # Utility functions
│   │
│   ├── data/              # Application data
│   │   └── chromadb/      # Vector database storage
│   │
│   ├── migrations/        # Database migrations
│   ├── tests/             # Test suite
│   │
│   ├── config.py          # Configuration
│   ├── .env               # Environment variables (not in git)
│   ├── run.py             # API server entry point
│   ├── tui_app.py         # TUI application
│   └── pyproject.toml     # Python dependencies
│
├── CLAUDE.md              # Development guide for Claude Code
├── README.md              # Project overview and setup
├── CHANGES.md             # Simplification changelog
└── PROJECT_STRUCTURE.md   # This file
```

## Key Components

### 1. Backend API Server (`run.py`)
- Flask REST API
- Manages agent lifecycle
- Handles database operations
- Runs on http://localhost:5000

### 2. TUI Application (`tui_app.py`)
- Terminal user interface
- Three-pane layout:
  - Left: Agent status table
  - Center: Chat window
  - Right: CLI commands
- Communicates with API via HTTP

### 3. AI Agents (`app/agents/`)
- **Driver**: CEO/orchestrator
- **Creator**: Researcher with RAG
- **Generator**: Dynamic agent creator
- **Manager**: Resource management

### 4. Database
- **SQLite**: Agent state, messages, workflows, tasks
- **ChromaDB**: Vector embeddings for RAG

## Technology Stack

- **Python 3.12**
- **Flask** - REST API framework
- **Textual** - Terminal UI framework
- **Rich** - Terminal formatting
- **SQLAlchemy** - Database ORM
- **AutoGen** - AI agent framework
- **ChromaDB** - Vector database
- **OpenAI** - LLM provider

## Development Files

- `.gitignore` - Git ignore patterns
- `.python-version` - Python version (3.12)
- `uv.lock` - Locked dependencies
- `backend/.env` - Environment configuration (API keys, etc.)

## Documentation Files

- `README.md` - Main project documentation
- `CLAUDE.md` - Development guide (for Claude Code)
- `CHANGES.md` - Changelog of simplification
- `PROJECT_STRUCTURE.md` - This file

## Running the Application

### Terminal 1 - API Server
```bash
cd backend
uv run python run.py
```

### Terminal 2 - TUI
```bash
cd backend
uv run python tui_app.py
```

## Data Flow

```
User Input (TUI)
    ↓
HTTP Request
    ↓
Flask API
    ↓
Agent Service
    ↓
AI Agents
    ↓
Database
    ↓
Response → TUI Display
```

## Environment Variables

Required in `backend/.env`:
```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
```

## Package Management

All dependencies managed by **uv**:
- Installation: `uv add package`
- Dev deps: `uv add --dev package`
- Sync: `uv sync`
- Run: `uv run command`

## Testing

```bash
cd backend
uv run pytest              # Run all tests
uv run pytest -v           # Verbose
uv run pytest --cov        # With coverage
```

## Code Quality

```bash
cd backend
uv run ruff format .       # Format code
uv run ruff check .        # Lint
uv run ruff check . --fix  # Auto-fix
pyrefly check              # Type checking
```
