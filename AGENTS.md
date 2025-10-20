# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this CLI-based AI agent management system.

## Project Structure

```
project-root/
├── backend/          # Python Flask API + TUI Application
└── CLAUDE.md         # This file
```

---

## Backend (Python Flask + Textual TUI)

### Technology Stack
- **Python 3.12**
- **Flask** - REST API framework
- **SQLAlchemy + Flask-SQLAlchemy** - ORM
- **Flask-Migrate** - Database migrations
- **SQLite** - Database
- **Textual** - Terminal User Interface framework
- **Rich** - Terminal formatting and styling
- **AutoGen** - AI agent framework
- **ChromaDB** - Vector database for RAG

### Core Development Rules

1. **Package Management**
   - ONLY use `uv`, NEVER pip
   - Installation: `uv add package`
   - Running tools: `uv run tool`
   - Dev dependencies: `uv add --dev package`
   - Upgrading: `uv add --upgrade-package package`
   - FORBIDDEN: `uv pip install`, `@latest` syntax

2. **Code Quality**
   - Type hints required for all code
   - Use pyrefly for type checking:
     - `pyrefly init` - Initialize
     - `pyrefly check` - Check after every change
   - Public APIs must have docstrings
   - Functions must be focused and small
   - Line length: 88 chars maximum

3. **Testing**
   - Framework: `uv run pytest`
   - Async testing: use anyio, not asyncio
   - New features require tests
   - Bug fixes require regression tests

4. **Code Style**
   - PEP 8 naming (snake_case for functions/variables)
   - Class names in PascalCase
   - Constants in UPPER_SNAKE_CASE
   - Use f-strings for formatting
   - Document with docstrings

### Common Commands

```bash
# Navigate to backend
cd backend

# Install dependencies
uv add flask flask-sqlalchemy flask-migrate python-dotenv textual rich

# Development dependencies
uv add --dev pytest pytest-cov ruff pyright

# Run API server (for TUI to connect to)
uv run python run.py          # Runs on http://localhost:5000

# Run TUI application (in another terminal)
uv run python tui_app.py

# Database migrations
uv run flask db init          # Initialize migrations
uv run flask db migrate -m "description"  # Create migration
uv run flask db upgrade       # Apply migrations

# Testing
uv run pytest                 # Run all tests
uv run pytest -v              # Verbose output
uv run pytest --cov           # With coverage

# Code quality
uv run ruff format .          # Format code
uv run ruff check .           # Check linting
uv run ruff check . --fix     # Auto-fix issues
pyrefly check                 # Type checking
```

### Backend Architecture

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   ├── agents/              # AI agent implementations
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── migrations/              # Database migrations
├── tests/                   # Test files
├── config.py                # Configuration
├── .env                     # Environment variables
├── run.py                   # API server entry point
├── tui_app.py               # TUI application
└── pyproject.toml           # Dependencies
```

### MVC Pattern
- **Models** (`app/models/`) - Database schema
- **Routes** (`app/routes/`) - HTTP endpoints (Controllers)
- **Services** (`app/services/`) - Business logic
- **Agents** (`app/agents/`) - AI agent implementations

---

## TUI Application (Terminal User Interface)

### Features
- **Three-pane layout**:
  - Left panel: Agent status table
  - Center panel: Chat window with selected agent
  - Right panel: CLI commands
- **Real-time agent monitoring**
- **Direct chat with AI agents**
- **System status commands**

### TUI Components

**Key Bindings:**
- `q` - Quit application
- `r` - Refresh agent list
- `c` - Clear chat window
- `Ctrl+L` - Clear CLI output

**CLI Commands:**
- `/help` - Show available commands
- `/status` - Show system status
- `/agents` - List all agents
- `/clear` - Clear CLI output

### TUI Development

The TUI is built with **Textual**, a modern Python framework for terminal UIs:

```python
# Basic structure
from textual.app import App
from textual.widgets import DataTable, Log, Input

class VirtualStartupTUI(App):
    # Define layout using CSS
    CSS = """..."""

    # Compose UI elements
    def compose(self) -> ComposeResult:
        yield Header()
        # ... panels and widgets
        yield Footer()
```

**Important TUI considerations:**
- Text wrapping must be handled manually using `textwrap.fill()`
- The `Log` widget doesn't auto-wrap text
- Calculate panel width dynamically: `self.size.width - 4`
- Use `write()` method to add content to Log widgets
- Async operations should use `asyncio.to_thread()` for blocking calls

---

## Development Workflow

### Initial Setup

```bash
# Backend setup
cd backend

# Install dependencies (automatically syncs from pyproject.toml)
uv sync

# Initialize database
uv run flask db init
uv run flask db upgrade

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Environment Variables

**Backend** (`.env` in `backend/` directory):
```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
```

### Running the Application

**Two-terminal setup:**

```bash
# Terminal 1 - API Server
cd backend
uv run python run.py       # Runs on http://localhost:5000

# Terminal 2 - TUI Application
cd backend
uv run python tui_app.py
```

The TUI will automatically connect to the API server at `http://localhost:5000`.

---

## Using Context7 MCP Server

The context7 MCP server should be used to check library documentation and best practices.

### When to Use Context7

- Checking API documentation for libraries
- Verifying correct usage patterns
- Looking up type definitions
- Finding examples for specific features
- Checking compatibility between versions

### Examples

```bash
# Before using a new library method
"Use context7 to check Flask-SQLAlchemy query methods"

# When implementing Textual UI features
"Use context7 to check Textual widget documentation"

# For AutoGen agent patterns
"Use context7 to check AutoGen agent configuration"
```

---

## REST API Communication

### API Structure

```
Backend API Base URL: http://localhost:5000/api

Available endpoints:
GET    /api/status              # System status
POST   /api/init                # Initialize agents
GET    /api/agents              # List all agents
GET    /api/agents/:id          # Get agent details
POST   /api/agents/:id/message  # Send message to agent
GET    /api/stats               # System statistics
```

### TUI-API Communication Pattern

The TUI communicates with the API using synchronous HTTP requests:

```python
import requests

API_URL = "http://localhost:5000/api"

# Fetch data
response = requests.get(f"{API_URL}/agents", timeout=2)
if response.ok:
    agents = response.json()

# Send data (with async support)
response = await asyncio.to_thread(
    requests.post,
    f"{API_URL}/agents/{agent_id}/message",
    json={"message": message},
    timeout=10
)
```

---

## Development Best Practices

### General Principles
- **Simplicity**: Write simple, straightforward code
- **Readability**: Make code easy to understand
- **Build Iteratively**: Start minimal, verify, then expand
- **Test Frequently**: Test with realistic inputs
- **Less Code = Less Debt**: Minimize code footprint

### Backend Best Practices
- Use early returns to avoid nested conditions
- Prefix handlers with "handle_"
- Use constants over functions where possible
- Keep core logic clean, push details to edges
- Type hints for all functions
- Docstrings for public APIs

### TUI Best Practices
- Handle text wrapping manually with `textwrap.fill()`
- Calculate dynamic widths based on panel size
- Use async operations for blocking I/O (HTTP requests)
- Provide clear error messages in the UI
- Add blank lines for visual separation in logs
- Test with various terminal sizes

---

## Adding Dependencies

### When to Add Packages

Add packages ONLY when you need them. Start with the minimal setup, then expand.

### Backend - Additional Packages (Add as needed)

```bash
# Authentication
uv add flask-jwt-extended

# API Documentation
uv add flask-smorest

# Validation
uv add marshmallow

# Testing utilities
uv add --dev pytest-flask faker

# Additional TUI features
uv add textual-dev  # Development tools for Textual
```

---

## Troubleshooting

### Backend Issues

1. **Import errors**: Check pyrefly for type checking
2. **Database errors**: Check migrations with `flask db current`
3. **Port in use**: Change port in `run.py` or kill existing process
4. **Agent initialization fails**: Check OpenAI API key in `.env`

### TUI Issues

1. **Connection errors**: Ensure API server is running on port 5000
2. **Text not wrapping**: Check `write_wrapped()` implementation
3. **Layout issues**: Adjust CSS width values or panel sizes
4. **Async errors**: Use `asyncio.to_thread()` for blocking operations

### Common Commands for Debugging

```bash
# Backend
uv run flask routes          # List all routes
uv run flask shell           # Interactive shell
pyrefly check                # Type checking

# Check if port is in use
lsof -ti:5000                # Find process using port 5000
kill $(lsof -ti:5000)        # Kill process on port 5000

# TUI debugging
uv run textual console       # Open Textual console for debugging
```

---

## Git Workflow

```bash
# Before committing
cd backend && uv run ruff format . && uv run ruff check . --fix

# Check status
git status

# Commit
git add .
git commit -m "feat: descriptive message"
```

---

## Architecture Overview

### System Components

1. **Flask API Server** (`run.py`)
   - Provides REST API endpoints
   - Manages agent lifecycle
   - Handles database operations
   - No web frontend - API only

2. **TUI Application** (`tui_app.py`)
   - Terminal-based user interface
   - Three-pane layout (agents, chat, CLI)
   - Connects to Flask API via HTTP
   - Built with Textual framework

3. **AI Agents** (`app/agents/`)
   - Driver: Project coordination
   - Creator: Content generation
   - Generator: Code generation
   - Manager: Resource management

4. **Database** (SQLite + ChromaDB)
   - SQLite: Agent state, messages, workflows
   - ChromaDB: Vector embeddings for RAG

### Data Flow

```
User Input (TUI)
  → HTTP Request
    → Flask API
      → Agent Service
        → AI Agent
          → Database
            → Response
              → TUI Display
```
