# Virtual Startup - Development Roadmap

**Last Updated:** October 18, 2025
**Current Status:** WebSocket communication working, agent system operational

---

## ✅ Recently Completed

### WebSocket Fix (October 18, 2025)
- **Issue**: Backend WebSocket handlers weren't receiving messages from frontend
- **Root Cause**: Flask's auto-reloader was creating child processes that didn't re-register Socket.IO handlers
- **Solution**: Disabled auto-reloader by default, ensured proper initialization order
- **Status**: ✅ **FIXED** - See `WEBSOCKET_FIX.md` for details
- **Verification**: Frontend and backend socket IDs now match, messages received successfully

### Agent System Initialization
- **Improvement**: Agents now auto-initialize on server startup
- **Status**: ✅ **COMPLETE** - No manual `/api/init` call required

---

## 🎯 Next Development Options

Choose one of the following development paths based on your priorities:

### Option 1: Frontend Enhancement (React Router + Navigation)

**Priority:** Medium
**Effort:** 4-8 hours
**Status:** Partially deferred (see `DEFERRED_FEATURES.md`)

#### Objective
Transform the single-page application into a multi-page app with proper navigation, improving UX and scalability.

#### What to Build

1. **Install React Router**
   ```bash
   cd frontend
   npm install react-router-dom
   ```

2. **Create Route Structure**
   ```
   frontend/src/
   ├── pages/
   │   ├── Dashboard.tsx       (existing)
   │   ├── ChatDemo.tsx        (existing)
   │   ├── CLI.tsx             (existing)
   │   ├── AgentDetail.tsx     (NEW - individual agent view)
   │   ├── Settings.tsx        (NEW - configuration)
   │   └── NotFound.tsx        (NEW - 404 page)
   ├── components/
   │   ├── layout/
   │   │   ├── Header.tsx      (NEW - navigation bar)
   │   │   ├── Sidebar.tsx     (NEW - agent list sidebar)
   │   │   └── Layout.tsx      (NEW - wrapper)
   ```

3. **Key Tasks**
   - [ ] Set up React Router in `App.tsx`
   - [ ] Create Header component with navigation links
   - [ ] Create Sidebar component with agent list
   - [ ] Create Layout wrapper component
   - [ ] Add route protection (if needed)
   - [ ] Create AgentDetail page for focused chat
   - [ ] Create Settings page for configuration
   - [ ] Add 404 Not Found page
   - [ ] Update navigation to use router links
   - [ ] Add breadcrumbs for navigation context

4. **Routes to Implement**
   ```typescript
   /                      → Dashboard (default)
   /agents/:id            → AgentDetail (focused chat)
   /chat                  → ChatDemo (multi-agent chat)
   /cli                   → CLI (terminal interface)
   /settings              → Settings (configuration)
   ```

5. **Success Criteria**
   - ✅ Can navigate between pages without page reload
   - ✅ Browser back/forward buttons work correctly
   - ✅ Each page has a unique URL
   - ✅ Header shows current location
   - ✅ Sidebar persists across navigation
   - ✅ 404 page shows for invalid routes

---

### Option 2: Testing Infrastructure

**Priority:** High (before production)
**Effort:** 16-24 hours
**Status:** Deferred (see `DEFERRED_FEATURES.md`)

#### Objective
Add comprehensive automated testing for both frontend and backend to ensure reliability and prevent regressions.

#### Frontend Testing (Playwright)

1. **Setup**
   ```bash
   cd frontend
   npm install --save-dev @playwright/test
   npx playwright install
   ```

2. **Test Structure**
   ```
   frontend/
   ├── tests/
   │   ├── e2e/
   │   │   ├── dashboard.spec.ts
   │   │   ├── chat.spec.ts
   │   │   ├── agent-interaction.spec.ts
   │   │   └── websocket.spec.ts
   │   └── fixtures/
   │       └── test-data.ts
   └── playwright.config.ts
   ```

3. **Key Test Cases**
   - [ ] Dashboard loads and displays agents
   - [ ] Can select an agent and open chat
   - [ ] Can type and send multi-word messages
   - [ ] Agent responds to messages
   - [ ] WebSocket connection established
   - [ ] Status updates reflect correctly
   - [ ] Error handling works (offline agent)
   - [ ] Message history persists
   - [ ] CLI interface accepts commands
   - [ ] Multi-agent chat synchronizes

4. **Commands**
   ```bash
   npm run test:e2e              # Run all tests
   npm run test:e2e:headed       # Run with browser visible
   npm run test:e2e:debug        # Debug mode
   ```

#### Backend Testing (Pytest)

1. **Expand Test Coverage**
   ```
   backend/tests/
   ├── unit/
   │   ├── test_agents.py        (expand existing)
   │   ├── test_rag_service.py   (NEW)
   │   ├── test_workflow.py      (NEW)
   │   └── test_task_processor.py (NEW)
   ├── integration/
   │   ├── test_api_endpoints.py (expand existing)
   │   ├── test_websocket.py     (NEW)
   │   └── test_agent_workflow.py (NEW)
   └── fixtures/
       └── agent_fixtures.py     (NEW)
   ```

2. **Key Test Cases**
   - [ ] Agent initialization
   - [ ] Message sending and receiving
   - [ ] RAG service queries
   - [ ] Workflow orchestration
   - [ ] Task processing
   - [ ] WebSocket connection handling
   - [ ] WebSocket message flow
   - [ ] Database operations
   - [ ] Error handling and recovery
   - [ ] Concurrent agent operations

3. **Commands**
   ```bash
   cd backend
   uv run pytest                 # Run all tests
   uv run pytest -v              # Verbose
   uv run pytest --cov           # With coverage
   uv run pytest --cov-report=html  # HTML report
   ```

4. **Success Criteria**
   - ✅ Frontend: >80% code coverage
   - ✅ Backend: >90% code coverage
   - ✅ All critical paths tested
   - ✅ WebSocket flow fully tested
   - ✅ Tests run in CI/CD pipeline
   - ✅ No flaky tests

---

### Option 3: Agent Workflow Improvements

**Priority:** Medium
**Effort:** 8-16 hours

#### Objective
Enhance agent collaboration, task delegation, and workflow visualization.

#### What to Build

1. **Task Delegation System**
   ```python
   # backend/app/services/delegation_service.py
   class DelegationService:
       def delegate_task(self, from_agent: Agent, to_agent: Agent, task: Task)
       def monitor_delegation(self, task_id: int) -> DelegationStatus
       def handle_delegation_response(self, task_id: int, response: dict)
   ```

2. **Workflow Visualization**
   ```typescript
   // frontend/src/components/workflow/WorkflowGraph.tsx
   // Visual representation of agent interactions and task flow
   ```

3. **Enhanced Agent Status**
   - Current task being worked on
   - Queue of pending tasks
   - Last activity timestamp
   - Performance metrics (tasks completed, avg response time)

4. **Key Tasks**
   - [ ] Create delegation service in backend
   - [ ] Add task queue for each agent
   - [ ] Implement task routing logic
   - [ ] Add workflow state machine
   - [ ] Create workflow graph component
   - [ ] Add real-time workflow updates via WebSocket
   - [ ] Implement task priority system
   - [ ] Add workflow history tracking
   - [ ] Create workflow analytics dashboard
   - [ ] Add workflow export functionality

5. **Success Criteria**
   - ✅ Agents can delegate tasks to each other
   - ✅ Task flow is visible in UI
   - ✅ Status updates are real-time
   - ✅ Can view workflow history
   - ✅ Analytics show agent performance

---

### Option 4: MCP Integration (External Tools)

**Priority:** Low (enhancement)
**Effort:** 8-16 hours
**Status:** Intentionally deferred (see `DEFERRED_FEATURES.md`)

#### Objective
Integrate Model Context Protocol (MCP) to give agents access to external tools and data sources.

#### What to Build

1. **MCP Service**
   ```python
   # backend/app/services/mcp_service.py
   class MCPService:
       def __init__(self):
           self.context7_client = None  # Documentation lookup
           self.web_search_client = None  # Web search

       def query_context7(self, query: str) -> str:
           """Query Context7 for library documentation"""
           pass

       def search_web(self, query: str) -> list:
           """Search web through MCP"""
           pass

       def get_available_tools(self) -> list[str]:
           """List all available MCP tools"""
           pass
   ```

2. **Integration with Creator Agent**
   - Enhance research capabilities
   - Combine MCP + RAG results
   - Add fallback logic

3. **Key Tasks**
   - [ ] Research AutoGen + MCP integration patterns
   - [ ] Set up Context7 MCP server
   - [ ] Create MCP service wrapper
   - [ ] Integrate with Creator agent
   - [ ] Add web search capability
   - [ ] Implement tool discovery
   - [ ] Add MCP health checks
   - [ ] Create tests with MCP mocks
   - [ ] Add MCP configuration to settings
   - [ ] Document MCP setup process

4. **Success Criteria**
   - ✅ Creator can query Context7 for docs
   - ✅ Web search results integrated
   - ✅ Fallback to RAG if MCP unavailable
   - ✅ Tool discovery working
   - ✅ No breaking changes to existing system

---

## 📋 Development Guidelines

### Before Starting Any Option

1. **Create a feature branch**
   ```bash
   git checkout -b feature/option-name
   ```

2. **Review existing code**
   - Check current implementation
   - Identify dependencies
   - Review related documentation

3. **Plan incrementally**
   - Start with minimal implementation
   - Test frequently
   - Expand gradually

### During Development

1. **Follow code style**
   - Backend: PEP 8, type hints, docstrings
   - Frontend: TypeScript strict mode, ESLint
   - See `CLAUDE.md` for detailed guidelines

2. **Test as you go**
   - Unit tests for new functions
   - Integration tests for workflows
   - Manual testing in browser/terminal

3. **Document changes**
   - Update `CLAUDE.md` if needed
   - Add inline comments for complex logic
   - Update API documentation

### Before Committing

1. **Code quality checks**
   ```bash
   # Backend
   cd backend
   uv run ruff format .
   uv run ruff check . --fix
   pyrefly check

   # Frontend
   cd frontend
   npm run lint:fix
   npm run typecheck
   ```

2. **Test everything**
   ```bash
   # Backend
   cd backend
   uv run pytest

   # Frontend
   cd frontend
   npm run test:e2e  # If tests exist
   ```

3. **Commit with descriptive message**
   ```bash
   git add .
   git commit -m "feat: add React Router navigation"
   ```

---

## 🔗 Related Documentation

- **`WEBSOCKET_FIX.md`** - Details of the WebSocket handler fix
- **`DEFERRED_FEATURES.md`** - Features intentionally deferred with reasoning
- **`CLAUDE.md`** - Development guidelines and project structure
- **`docs/architecture.md`** - System architecture overview
- **`docs/agents.md`** - Agent system documentation
- **`docs/api.md`** - API endpoint documentation

---

## 🤔 Decision Framework

**Choose Option 1 (React Router) if:**
- You want better user experience
- You need proper URL-based navigation
- You're preparing for production deployment

**Choose Option 2 (Testing) if:**
- You're preparing for production
- You want to prevent regressions
- You need confidence in code changes

**Choose Option 3 (Workflow) if:**
- You want better agent collaboration
- You need task delegation features
- You want workflow analytics

**Choose Option 4 (MCP) if:**
- You need external tool integration
- You want enhanced research capabilities
- You're comfortable with additional complexity

---

## 📊 Priority Summary

| Option | Priority | Effort | Production Ready? |
|--------|----------|--------|-------------------|
| Option 1: React Router | Medium | 4-8h | Recommended |
| Option 2: Testing | **High** | 16-24h | **Required** |
| Option 3: Workflow | Medium | 8-16h | Optional |
| Option 4: MCP | Low | 8-16h | Optional |

**Recommended sequence for production:**
1. Option 2 (Testing) - High priority
2. Option 1 (React Router) - Medium priority
3. Option 3 or 4 - Based on needs

---

*Select one option and start implementation, or ask for clarification on any option.*
