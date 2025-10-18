# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this full-stack application.

## Project Structure

```
project-root/
├── backend/          # Python Flask REST API
├── frontend/         # React TypeScript application
└── CLAUDE.md         # This file
```

---

## Backend (Python Flask)

### Technology Stack
- **Python 3.12**
- **Flask** - Web framework
- **SQLAlchemy + Flask-SQLAlchemy** - ORM
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database

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
uv add flask flask-sqlalchemy flask-migrate flask-cors python-dotenv

# Development dependencies
uv add --dev pytest pytest-cov ruff pyright

# Run development server
uv run flask run --debug

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
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── migrations/              # Database migrations
├── tests/                   # Test files
├── config.py                # Configuration
├── .env                     # Environment variables
└── pyproject.toml           # Dependencies
```

### MVC Pattern
- **Models** (`app/models/`) - Database schema
- **Routes** (`app/routes/`) - HTTP endpoints (Controllers)
- **Services** (`app/services/`) - Business logic

---

## Frontend (React + TypeScript)

### Technology Stack
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client
- **React Router Dom** - Routing

### Common Commands

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time)
npm install

# Development server
npm run dev               # Start dev server (usually http://localhost:5173)

# Build for production
npm run build             # Build optimized bundle
npm run preview           # Preview production build

# Code quality
npm run lint              # ESLint check
npm run lint:fix          # Auto-fix linting issues
npm run typecheck         # TypeScript type checking
```

### Frontend Architecture

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   ├── pages/               # Page components (routes)
│   ├── services/            # API service layer
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Utility functions
│   ├── types/               # TypeScript types/interfaces
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── index.html               # HTML template
├── tailwind.config.js       # TailwindCSS config
├── tsconfig.json            # TypeScript config
├── vite.config.ts           # Vite config
└── package.json             # Dependencies
```

### Code Style
- Functional components with hooks
- TypeScript strict mode enabled
- Prettier with 120 character line width
- Double quotes for strings
- Use arrow functions for components
- Props interfaces defined explicitly

---

## Development Workflow

### Initial Setup

```bash
# 1. Backend setup
cd backend
uv add flask flask-sqlalchemy flask-migrate flask-cors python-dotenv
uv add --dev pytest ruff pyright
uv run flask db init
uv run flask db upgrade

# 2. Frontend setup
cd ../frontend
npm install
```

### Environment Variables

**Backend** (`.env` in `backend/` directory):
```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

**Frontend** (`.env` in `frontend/` directory):
```env
VITE_API_URL=http://localhost:5000/api
```

### Running Both Servers

```bash
# Terminal 1 - Backend (IMPORTANT: Use run.py for WebSocket support)
cd backend
uv run python run.py       # Runs on http://localhost:5000
                          # NOTE: Use run.py, NOT "flask run"!

# Terminal 2 - Initialize agents (one-time after backend starts)
curl -X POST http://localhost:5000/api/init

# Terminal 3 - Frontend
cd frontend
npm run dev                # Runs on http://localhost:5173
```

**CRITICAL**: Always use `uv run python run.py` to start the backend, NOT `flask run`.
The `run.py` file initializes Flask-SocketIO which is required for WebSocket chat functionality.

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

# When implementing a feature
"Use context7 to check React Hook Form validation patterns"

# For type checking
"Use context7 to verify TypeScript type definitions for Axios"
```

## Using Playwright MCP Server

The Playwright MCP server should be used to test and validate web UI behavior across browsers.

### When to Use Playwright

- Running automated end-to-end (E2E) UI tests
- Verifying frontend workflows and user interactions
- Capturing screenshots or tracing steps in web apps
- Checking performance or network requests
- Ensuring cross-browser compatibility

### Examples
```bash
# Before merging frontend changes
"Use Playwright to test login flow in Chromium and Firefox"

# When debugging UI automation
"Use Playwright to trace signup test failures"

# For performance validation
"Use Playwright to measure page load times under throttled network"
```

---

## REST API Communication

### API Structure

```
Backend API Base URL: http://localhost:5000/api

Example endpoints:
GET    /api/items           # List all items
GET    /api/items/:id       # Get single item
POST   /api/items           # Create item
PUT    /api/items/:id       # Update item
DELETE /api/items/:id       # Delete item
```

### Frontend API Service Pattern

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const itemService = {
  getAll: () => api.get('/items'),
  getById: (id: number) => api.get(`/items/${id}`),
  create: (data: ItemData) => api.post('/items', data),
  update: (id: number, data: ItemData) => api.put(`/items/${id}`, data),
  delete: (id: number) => api.delete(`/items/${id}`),
};
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

### Frontend Best Practices
- Component-based architecture
- Custom hooks for reusable logic
- Keep components focused and small
- Use TypeScript interfaces for props
- Handle loading and error states
- Implement proper error boundaries

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
```

### Frontend - Additional Packages (Add as needed)

```bash
# Form handling
npm install react-hook-form

# State management
npm install zustand

# Data fetching
npm install @tanstack/react-query

# UI components
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
```

---

## Troubleshooting

### Backend Issues

1. **Import errors**: Check pyrefly for type checking
2. **Database errors**: Check migrations with `flask db current`
3. **CORS errors**: Verify CORS_ORIGINS in .env
4. **Port in use**: Change port with `flask run --port 5001`

### Frontend Issues

1. **Module not found**: Run `npm install`
2. **Type errors**: Run `npm run typecheck`
3. **API connection**: Check VITE_API_URL in .env
4. **Build errors**: Clear cache with `rm -rf node_modules/.vite`

### Common Commands for Debugging

```bash
# Backend
uv run flask routes          # List all routes
uv run flask shell           # Interactive shell
pyrefly check                # Type checking

# Frontend
npm run build -- --debug     # Verbose build
npm run typecheck            # Check types
```

---

## Git Workflow

```bash
# Before committing
cd backend && uv run ruff format . && uv run ruff check . --fix
cd ../frontend && npm run lint:fix && npm run typecheck

# Check status
git status

# Commit
git add .
git commit -m "feat: descriptive message"
```

---

## TODO

Read TODO.md file ant implement only Phase 1: Project Setup & Foundation
