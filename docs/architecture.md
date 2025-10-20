# Virtual Startup - System Architecture

## Overview

Virtual Startup is a multi-agent system for virtual startup management using AutoGen. The system consists of three core permanent agents (Driver, Creator, Generator) that collaborate under human operator supervision through both CLI and web UI interfaces.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Human Operator                          │
│                   (CLI / Web Interface)                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Commands/Tasks
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    Driver Agent (CEO)                        │
│              Orchestrator & Task Manager                     │
└──────┬──────────────────────────────────────────────────────┘
       │
       ├──────────────► Creator Agent (Researcher)
       │                 - Research & Ideas
       │                 - RAG (Vector DB)
       │                 - MCP Tools
       │                 - Idea Generation
       │
       └──────────────► Generator Agent (HR)
                        - Dynamic Agent Creation
                        - Agent Specification
                        - Lifecycle Management
                             │
                             ▼
                        Dynamic Agents
                        (Task-specific)
```

## Technology Stack

### Backend
- **Language**: Python 3.12
- **Framework**: Flask
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **Migrations**: Flask-Migrate
- **Agent Framework**: AutoGen (pyautogen)
- **Real-time**: Flask-SocketIO, Python-SocketIO
- **Vector DB**: ChromaDB (for RAG)
- **Testing**: pytest, pytest-cov
- **Code Quality**: Ruff, Pyright

### Frontend
- **Language**: TypeScript
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **HTTP Client**: Axios
- **Real-time**: Socket.IO Client
- **Routing**: React Router Dom

## System Components

### 1. Core Agents (Permanent)

#### Driver Agent (CEO/Orchestrator)
- **Role**: Central coordinator and task manager
- **Responsibilities**:
  - Receive tasks from human operator
  - Break down complex tasks into subtasks
  - Delegate tasks to appropriate agents
  - Monitor workflow progress
  - Report back to operator
  - Manage inter-agent communication

#### Creator Agent (Researcher/Ideator)
- **Role**: Research and idea generation
- **Responsibilities**:
  - Research topics using RAG (Retrieval-Augmented Generation)
  - Use MCP tools for enhanced capabilities
  - Generate creative ideas and proposals
  - Request specialized agents when needed
  - Provide context and insights

#### Generator Agent (HR/Agent Factory)
- **Role**: Dynamic agent creation and management
- **Responsibilities**:
  - Receive agent specifications from Driver/Creator
  - Generate agent configurations
  - Instantiate new AutoGen agents dynamically
  - Define agent roles and capabilities
  - Manage agent lifecycle

### 2. Dynamic Agents (Task-Specific)

Dynamic agents are created on-demand by the Generator agent for specific tasks:
- Specialized roles (e.g., "Marketing Strategist", "Technical Architect")
- Task-specific capabilities
- Temporary lifecycle (created and terminated as needed)
- Custom system prompts and configurations

### 3. Database Schema

```sql
-- Agents Table
agents:
  - id (PK)
  - name
  - type (driver/creator/generator/dynamic)
  - role
  - status (idle/working/waiting)
  - config (JSON)
  - created_at

-- Messages Table
messages:
  - id (PK)
  - agent_id (FK -> agents.id)
  - sender (agent/operator/system)
  - content
  - timestamp
  - metadata (JSON)

-- Workflows Table
workflows:
  - id (PK)
  - name
  - description
  - status (active/completed/failed)
  - started_at
  - completed_at
  - metadata (JSON)

-- Tasks Table
tasks:
  - id (PK)
  - workflow_id (FK -> workflows.id)
  - assigned_to (FK -> agents.id)
  - status (pending/in_progress/completed/failed)
  - description
  - result
  - created_at
  - completed_at
```

### 4. Communication Layer

#### REST API
- Standard HTTP endpoints for CRUD operations
- Agent management
- Workflow management
- Statistics and monitoring

#### WebSocket (Socket.IO)
- Real-time bidirectional communication
- Live chat between operator and agents
- Agent status updates
- Workflow progress notifications
- Inter-agent message broadcasting

### 5. RAG (Retrieval-Augmented Generation)
- **Vector Database**: ChromaDB
- **Purpose**: Knowledge base for Creator agent
- **Features**:
  - Document storage and retrieval
  - Semantic search
  - Context enhancement for agent responses

### 6. MCP (Model Context Protocol) Integration
- Context7 MCP server for library documentation
- Web search capabilities (if available)
- Tool integration for enhanced agent capabilities

## Data Flow

### Task Execution Flow

```
1. Operator → Driver: "Create a marketing strategy"
2. Driver analyzes task
3. Driver → Creator: "Research current marketing trends"
4. Creator uses RAG/MCP to research
5. Creator generates ideas
6. Creator → Driver: Sends research and ideas
7. Driver → Generator: "Create a Marketing Specialist agent"
8. Generator creates dynamic agent
9. Dynamic Agent executes specialized task
10. Results flow back through: Agent → Driver → Operator
```

### Message Flow (WebSocket)

```
Frontend (Browser)
    ↓ WebSocket connection
Backend (Flask-SocketIO)
    ↓ Agent Manager
Core Agents ↔ Dynamic Agents
    ↓ Database
Persist messages and state
```

## Deployment Architecture

### Development
```
Backend:  localhost:5000
Frontend: localhost:5173
Database: SQLite (local file)
```

### Production (Future)
```
Backend:  Cloud service (AWS/GCP/Azure)
Frontend: CDN (Vercel/Netlify)
Database: PostgreSQL (managed service)
Redis:    For Celery task queue
```

## Security Considerations

1. **API Keys**: Stored in environment variables (.env)
2. **CORS**: Configured to allow specific origins
3. **Input Validation**: All user inputs validated
4. **Rate Limiting**: To prevent abuse (future)
5. **Authentication**: JWT tokens (future, for multi-user)

## Scalability Considerations

1. **Agent Pool**: Limit number of concurrent dynamic agents
2. **Message Queue**: Celery + Redis for async processing (future)
3. **Database**: PostgreSQL for production with connection pooling
4. **Caching**: Redis for session and agent state caching (future)
5. **Load Balancing**: Multiple backend instances (future)

## Monitoring and Observability

1. **Logging**: Structured logging for all agent activities
2. **Metrics**: Agent performance, task completion rates
3. **Error Tracking**: Sentry or similar (future)
4. **Health Checks**: API endpoints for system health

## Development Workflow

1. **Backend Development**: `cd backend && uv run flask run --debug`
2. **Frontend Development**: `cd frontend && npm run dev`
3. **Database Migrations**: `uv run flask db migrate && uv run flask db upgrade`
4. **Testing**: `uv run pytest` (backend), `npm test` (frontend)
5. **Code Quality**: `uv run ruff format . && uv run ruff check .`

## Future Enhancements

1. Multi-user support with authentication
2. Agent memory persistence (long-term memory)
3. Workflow templates
4. Agent marketplace (pre-defined agent types)
5. Voice interface
6. Integration with external tools (GitHub, Slack, etc.)
7. Cost tracking for LLM API calls
8. Performance metrics and analytics



