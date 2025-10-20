# Deferred Features

This document tracks features that were intentionally deferred during development.

---

## Phase 3: Agent System

### 3.5 MCP Integration (for Creator) ⏭️ DEFERRED

**Status:** Intentionally Deferred  
**Decision Date:** Phase 3 (October 2025)  
**Priority:** Low (Enhancement)

#### What It Is
Model Context Protocol (MCP) integration would allow the Creator agent to:
- Connect to Context7 MCP server for documentation lookup
- Access web search through MCP tools
- Query other MCP-compatible services

#### Why It Was Deferred

1. **Not Critical for MVP**
   - RAG service (ChromaDB) already provides research capabilities
   - Creator agent can effectively research using vector search
   - Core functionality doesn't depend on MCP

2. **Technical Complexity**
   - Requires additional MCP server setup and configuration
   - Complex integration with AutoGen's tool system
   - Additional dependencies and potential instability

3. **Time/Priority Trade-off**
   - Other features (API, Frontend, Testing) had higher priority
   - RAG provides 80% of the value with 20% of the complexity
   - Can be added incrementally later without breaking changes

#### Current Alternative

**RAG Service (ChromaDB)** provides:
- ✅ Semantic search over knowledge base
- ✅ Context retrieval for research
- ✅ Document storage and indexing
- ✅ Fast, local, reliable

This is sufficient for current needs.

#### Future Implementation Plan

When MCP integration becomes necessary:

1. **Research Phase**
   - Study AutoGen + MCP integration patterns
   - Evaluate Context7 MCP server setup
   - Assess other useful MCP tools

2. **Implementation**
   ```python
   # backend/app/services/mcp_service.py
   class MCPService:
       def __init__(self):
           self.context7_client = None
           self.web_search_client = None
       
       def query_context7(self, query: str) -> str:
           """Query Context7 for documentation"""
           pass
       
       def search_web(self, query: str) -> list:
           """Search web through MCP"""
           pass
   ```

3. **Integration with Creator**
   ```python
   # Update Creator agent to use MCP
   def research_topic(self, topic: str) -> str:
       # Try MCP first
       mcp_results = self.mcp_service.query_context7(topic)
       # Fallback to RAG
       rag_results = self.rag_service.search(topic)
       # Combine results
       return self._synthesize_research(mcp_results, rag_results)
   ```

4. **Testing**
   - Unit tests for MCP service
   - Integration tests with Creator
   - Fallback tests (MCP unavailable)

#### Estimated Effort
- **Research**: 2-4 hours
- **Implementation**: 4-8 hours
- **Testing**: 2-4 hours
- **Total**: 8-16 hours

#### Dependencies
- MCP server running (Context7 or other)
- MCP client library for Python
- AutoGen tool integration updates

#### Notes
- This is an **enhancement**, not a bug fix
- Current system is fully functional without it
- Can be implemented anytime without breaking changes
- Low risk, optional feature

---

## Other Deferred Features

### Phase 5: Frontend UI Layout (Partial)

**Status:** Partially Complete  
**Deferred Items:**
- React Router integration (using simple state-based routing instead)
- Header component
- Sidebar component
- Full layout wrapper

**Reason:** Simple navigation sufficient for demo/MVP

**Priority:** Medium - Should be completed before production

---

### Phase 10: Frontend Testing

**Status:** Deferred  
**Items:**
- Frontend component tests
- E2E tests with Playwright/Cypress
- WebSocket testing

**Reason:** Backend testing prioritized first

**Priority:** High - Should be completed before production

---

## Summary

| Feature | Phase | Status | Priority | Effort |
|---------|-------|--------|----------|--------|
| MCP Integration | 3 | Deferred | Low | 8-16h |
| React Router | 5 | Partial | Medium | 4-8h |
| Frontend Tests | 10 | Deferred | High | 16-24h |

**Total Deferred Work:** ~28-48 hours

---

## Decision Log

### Why Defer Instead of Delete?

These features were **deferred**, not deleted because:
1. They add value but aren't critical for MVP
2. They can be added incrementally without refactoring
3. The architecture supports them (no blocking dependencies)
4. They may become important for production/scale

### When to Implement?

**Before Production:**
- Frontend tests (High priority)
- React Router (Medium priority)

**Post-Production (Enhancement):**
- MCP Integration (Low priority)

---

*Last Updated: October 16, 2025*



