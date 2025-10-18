# API Documentation

This document describes the REST API and WebSocket endpoints for the Virtual Startup system.

## Base URL

```
Development: http://localhost:5000
Production:  https://api.virtual-startup.example.com
```

## REST API Endpoints

### Health Check

#### GET /
Check if the API is running.

**Response**
```json
{
  "status": "ok",
  "message": "Virtual Startup API"
}
```

---

## Agent Endpoints

### GET /api/agents
Get all agents in the system.

**Response**
```json
[
  {
    "id": 1,
    "name": "Driver",
    "type": "driver",
    "role": "CEO and Task Orchestrator",
    "status": "idle",
    "config": {},
    "created_at": "2025-10-16T12:00:00Z"
  },
  {
    "id": 2,
    "name": "Creator",
    "type": "creator",
    "role": "Researcher and Idea Generator",
    "status": "working",
    "config": {},
    "created_at": "2025-10-16T12:00:00Z"
  }
]
```

### GET /api/agents/{id}
Get a specific agent by ID.

**Parameters**
- `id` (path, required): Agent ID

**Response**
```json
{
  "id": 1,
  "name": "Driver",
  "type": "driver",
  "role": "CEO and Task Orchestrator",
  "status": "idle",
  "config": {},
  "created_at": "2025-10-16T12:00:00Z"
}
```

**Error Response**
- `404 Not Found`: Agent not found

### GET /api/agents/{id}/messages
Get all messages for a specific agent.

**Parameters**
- `id` (path, required): Agent ID

**Response**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "sender": "operator",
    "content": "Create a marketing strategy",
    "timestamp": "2025-10-16T12:00:00Z",
    "metadata": {}
  },
  {
    "id": 2,
    "agent_id": 1,
    "sender": "agent",
    "content": "I'll break this down into subtasks...",
    "timestamp": "2025-10-16T12:00:05Z",
    "metadata": {}
  }
]
```

### POST /api/agents/{id}/message
Send a message to an agent.

**Parameters**
- `id` (path, required): Agent ID

**Request Body**
```json
{
  "message": "Create a marketing strategy for our startup"
}
```

**Response**
```json
{
  "id": 3,
  "agent_id": 1,
  "sender": "operator",
  "content": "Create a marketing strategy for our startup",
  "timestamp": "2025-10-16T12:05:00Z",
  "metadata": {}
}
```

**Error Responses**
- `400 Bad Request`: Missing message content
- `404 Not Found`: Agent not found

---

## Workflow Endpoints

### GET /api/workflows
Get all workflows.

**Response**
```json
[
  {
    "id": 1,
    "name": "Marketing Strategy Development",
    "description": "Create comprehensive marketing strategy",
    "status": "active",
    "started_at": "2025-10-16T12:00:00Z",
    "completed_at": null,
    "metadata": {}
  }
]
```

### POST /api/workflows
Create a new workflow.

**Request Body**
```json
{
  "name": "Product Launch Plan",
  "description": "Plan for launching new product",
  "metadata": {
    "priority": "high"
  }
}
```

**Response**
```json
{
  "id": 2,
  "name": "Product Launch Plan",
  "description": "Plan for launching new product",
  "status": "active",
  "started_at": "2025-10-16T12:10:00Z",
  "completed_at": null,
  "metadata": {
    "priority": "high"
  }
}
```

**Error Response**
- `400 Bad Request`: Missing workflow name

### GET /api/workflows/{id}
Get a specific workflow by ID.

**Parameters**
- `id` (path, required): Workflow ID

**Response**
```json
{
  "id": 1,
  "name": "Marketing Strategy Development",
  "description": "Create comprehensive marketing strategy",
  "status": "active",
  "started_at": "2025-10-16T12:00:00Z",
  "completed_at": null,
  "metadata": {}
}
```

### GET /api/workflows/{id}/status
Get workflow status with associated tasks.

**Parameters**
- `id` (path, required): Workflow ID

**Response**
```json
{
  "workflow": {
    "id": 1,
    "name": "Marketing Strategy Development",
    "status": "active",
    "started_at": "2025-10-16T12:00:00Z"
  },
  "tasks": [
    {
      "id": 1,
      "workflow_id": 1,
      "assigned_to": 2,
      "status": "in_progress",
      "description": "Research market trends",
      "result": null,
      "created_at": "2025-10-16T12:01:00Z",
      "completed_at": null
    }
  ]
}
```

---

## Statistics Endpoints

### GET /api/stats/agents
Get agent statistics.

**Response**
```json
{
  "total": 5,
  "active": 2,
  "idle": 3
}
```

### GET /api/stats/workflows
Get workflow statistics.

**Response**
```json
{
  "total": 10,
  "active": 3,
  "completed": 6,
  "failed": 1
}
```

### GET /api/stats/overview
Get system overview.

**Response**
```json
{
  "agents": {
    "total": 5,
    "active": 2,
    "idle": 3
  },
  "workflows": {
    "total": 10,
    "active": 3,
    "completed": 6
  },
  "status": "online"
}
```

---

## WebSocket Events

### Connection

**URL**
```
ws://localhost:5000/socket.io/
```

**Client Connection**
```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});
```

### Events

#### Client → Server

##### send_message
Send a message to an agent.

**Payload**
```json
{
  "agent_id": 1,
  "message": "Create a marketing strategy"
}
```

##### agent_status
Request agent status.

**Payload**
```json
{
  "agent_id": 1
}
```

#### Server → Client

##### connection_response
Confirmation of connection.

**Payload**
```json
{
  "status": "connected"
}
```

##### agent_response
Response from an agent.

**Payload**
```json
{
  "agent_id": 1,
  "message": "I've analyzed your request...",
  "sender": "agent"
}
```

##### agent_status_response
Agent status information.

**Payload**
```json
{
  "agent_id": 1,
  "status": "working"
}
```

##### error
Error notification.

**Payload**
```json
{
  "error": "agent_id and message required"
}
```

### Example WebSocket Usage

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

// Connect
socket.on('connect', () => {
  console.log('Connected');
  
  // Send message to agent
  socket.emit('send_message', {
    agent_id: 1,
    message: 'Create a marketing strategy'
  });
});

// Receive agent response
socket.on('agent_response', (data) => {
  console.log('Agent response:', data);
  // data = {
  //   agent_id: 1,
  //   message: "I'll create a marketing strategy...",
  //   sender: "agent"
  // }
});

// Handle errors
socket.on('error', (error) => {
  console.error('Socket error:', error);
});

// Disconnect
socket.on('disconnect', () => {
  console.log('Disconnected');
});
```

---

## Error Responses

### Standard Error Format
```json
{
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Authentication (Future)

Future versions will include JWT-based authentication:

```
Authorization: Bearer <token>
```

---

## Rate Limiting (Future)

Future versions will include rate limiting:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634400000
```

---

## CORS Configuration

The API allows requests from:
- Development: `http://localhost:5173`
- Production: Configured via `CORS_ORIGINS` environment variable

---

## Testing the API

### Using cURL

```bash
# Get all agents
curl http://localhost:5000/api/agents

# Get specific agent
curl http://localhost:5000/api/agents/1

# Send message to agent
curl -X POST http://localhost:5000/api/agents/1/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a marketing strategy"}'

# Get agent messages
curl http://localhost:5000/api/agents/1/messages

# Create workflow
curl -X POST http://localhost:5000/api/workflows \
  -H "Content-Type: application/json" \
  -d '{"name": "Product Launch", "description": "Launch new product"}'

# Get statistics
curl http://localhost:5000/api/stats/overview
```

### Using Postman

Import the following collection:
```json
{
  "info": {
    "name": "Virtual Startup API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get All Agents",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/agents"
      }
    },
    {
      "name": "Send Message",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/api/agents/1/message",
        "body": {
          "mode": "raw",
          "raw": "{\"message\": \"Hello Agent\"}"
        }
      }
    }
  ]
}
```

---

## Changelog

### v0.1.0 (Phase 1)
- Initial API design
- Basic CRUD endpoints for agents and workflows
- WebSocket support for real-time communication
- Statistics endpoints


