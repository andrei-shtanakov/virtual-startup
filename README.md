# Virtual Startup - AI Agent Management System

A CLI-based AI agent management system built with Python, Flask, and Textual TUI.

## Features

- 🤖 **Multi-Agent System**: Coordinate multiple AI agents (Driver, Creator, Generator, Manager)
- 💬 **Interactive Chat**: Chat with agents through an intuitive terminal UI
- 🔍 **Research Capabilities**: RAG integration with ChromaDB
- 📊 **Real-time Monitoring**: Track agent status and activities
- 🎨 **Three-Pane TUI**: Clean terminal interface with agent list, chat, and CLI panels
- 🔌 **REST API**: Backend API for agent management and communication
- 💾 **Persistent Storage**: SQLite database with ChromaDB for vector embeddings

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd virtual-startup

# Navigate to backend
cd backend

# Install dependencies (uv will auto-sync from pyproject.toml)
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Application

You need two terminal windows:

**Terminal 1 - API Server:**
```bash
cd backend
uv run python run.py
```

**Terminal 2 - TUI Application:**
```bash
cd backend
uv run python tui_app.py
```

## Architecture

```
User Input (TUI)
    ↓
HTTP Request
    ↓
Flask API
    ↓
Agent Service
    ↓
AI Agents (Driver, Creator, Generator)
    ↓
Database (SQLite + ChromaDB)
    ↓
Response → TUI Display
```

### Core Agents

1. **Driver Agent (CEO)** - Orchestrates tasks and coordinates between agents
2. **Creator Agent (Researcher)** - Researches topics and generates ideas using RAG
3. **Generator Agent (HR)** - Creates specialized agents on-demand based on task requirements

## Project Structure

```
virtual-startup/
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agent implementations
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   └── services/        # Business logic
│   ├── tui_app.py           # Terminal UI application
│   ├── run.py               # API server entry point
│   └── pyproject.toml       # Dependencies
├── CLAUDE.md                # Development guide
└── README.md                # This file
```

## TUI Usage

### Key Bindings

- `q` - Quit application
- `r` - Refresh agent list
- `c` - Clear chat window
- `Ctrl+L` - Clear CLI output
- `Tab` - Switch between input fields
- `Enter` - Send message/command

### CLI Commands

- `/help` - Show available commands
- `/status` - Show system status
- `/agents` - List all agents
- `/clear` - Clear CLI output

### Chat with Agents

1. Select an agent from the left panel (click or use arrow keys + Enter)
2. Type your message in the chat input at the bottom of the center panel
3. Press Enter to send
4. Agent responses appear in the center panel with automatic text wrapping

## API Endpoints

The Flask API runs on `http://localhost:5000`:

- `GET /api/status` - System status
- `POST /api/init` - Initialize agents
- `GET /api/agents` - List all agents
- `GET /api/agents/:id` - Get agent details
- `POST /api/agents/:id/message` - Send message to agent
- `GET /api/stats` - System statistics

## Development

### Install Dev Dependencies

```bash
cd backend
uv add --dev pytest pytest-cov ruff pyright
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint
uv run ruff check . --fix

# Type checking
pyrefly check

# Run tests
uv run pytest
```

### Database Migrations

```bash
# Initialize migrations (first time)
uv run flask db init

# Create migration
uv run flask db migrate -m "description"

# Apply migrations
uv run flask db upgrade
```

## Technology Stack

- **Python 3.12** - Programming language
- **Flask** - Web framework for REST API
- **Textual** - Terminal UI framework
- **Rich** - Terminal formatting
- **SQLAlchemy** - Database ORM
- **AutoGen** - AI agent framework
- **ChromaDB** - Vector database
- **OpenAI** - LLM provider

## Configuration

Edit `backend/.env`:

```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
kill $(lsof -ti:5000)
```

### Agent Initialization Fails

- Check your OpenAI API key in `.env`
- Ensure you have sufficient API credits
- Check network connectivity

### TUI Connection Error

- Ensure the API server is running on port 5000
- Check that there are no firewall issues
- Verify the API_URL in `tui_app.py` is set to `http://localhost:5000/api`

### Text Not Wrapping in TUI

The TUI uses manual text wrapping with Python's `textwrap.fill()`. If text doesn't wrap properly:
- Check that `write_wrapped()` method is being used for long messages
- Verify panel width calculation in `on_mount()` method
- Test with different terminal sizes

## Development Status

### ✅ Completed

- **Backend Infrastructure**
  - Flask REST API
  - Database models (SQLAlchemy)
  - Agent system (AutoGen)
  - RAG integration (ChromaDB)
  - API endpoints

- **TUI Application**
  - Three-pane layout
  - Agent status table
  - Chat window with text wrapping
  - CLI commands
  - Real-time updates

- **Core Features**
  - Multi-agent orchestration
  - Agent communication
  - Workflow tracking
  - Persistent storage

### 🚧 Future Enhancements

- Enhanced agent capabilities
- Additional CLI commands
- Improved error handling
- Performance optimizations
- Additional documentation

## Contributing

This is a development project. Contributions and suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

[Add your license here]

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Status:** CLI-Only Version | Active Development 🚧
