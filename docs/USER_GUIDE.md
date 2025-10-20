# Virtual Startup - User Guide

**Version**: 1.0.0
**Last Updated**: October 18, 2025

Welcome to Virtual Startup! This guide will help you get started with the multi-agent AI system for startup management.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard](#dashboard)
3. [Chat Interface](#chat-interface)
4. [CLI Interface](#cli-interface)
5. [Working with Agents](#working-with-agents)
6. [Workflows](#workflows)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Quick Start

1. **Start the Backend**:
   ```bash
   cd backend
   uv run python run.py
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open the Application**:
   Navigate to [http://localhost:5173](http://localhost:5173) in your browser.

### First Steps

When you first open Virtual Startup, you'll see the **Dashboard** with three main navigation options:

- **Dashboard**: Overview of agents and system stats
- **Chat Demo**: Interactive chat with individual agents
- **CLI**: Command-line interface for advanced users

---

## Dashboard

The Dashboard is your central hub for monitoring the Virtual Startup system.

### Features

#### 1. **Agent Cards**
View all active agents in the system:
- **Driver (CEO)**: Orchestrates tasks and coordinates agents
- **Creator (Researcher)**: Researches topics and generates ideas
- **Generator (HR)**: Creates new specialized agents on demand

#### 2. **Stats Panel**
Monitor system health and activity:
- Total agents
- Active workflows
- System status

#### 3. **Quick Navigation**
Use the top-right buttons to switch between pages.

### Example: Viewing Agent Status

1. Open the Dashboard
2. Scroll to see agent cards
3. Each card shows:
   - Agent name and role
   - Current status (idle/busy/error)
   - Quick action buttons

---

## Chat Interface

The Chat Interface allows you to communicate directly with individual agents.

### How to Use

#### Step 1: Select an Agent

Click the **Chat Demo** button in the top navigation to open the chat interface.

You'll see options to select an agent:
- **Driver**: For task orchestration and project management
- **Creator**: For research and idea generation
- **Generator**: For creating new agents

#### Step 2: Start a Conversation

1. **Select your agent** (e.g., "Driver")
2. **Type your message** in the input field at the bottom
3. **Press Enter** or click **Send** to send the message
4. **Wait for the response** (you'll see a "typing" indicator)

### Examples

#### Example 1: Ask Driver for Project Status

**You**:
```
What is the current status of our project?
```

**Driver Agent**:
```
I'm currently coordinating three active workflows:
1. Market Research (70% complete)
2. Product Development (in progress)
3. Marketing Strategy (pending)

Would you like details on any specific workflow?
```

#### Example 2: Ask Creator to Research a Topic

**You**:
```
Can you research the latest trends in AI startups?
```

**Creator Agent**:
```
I'll research AI startup trends for you. Let me search through my knowledge base and provide insights...

Based on my research, here are the top 3 trends:
1. Multi-agent AI systems
2. AI-powered automation
3. Vertical AI solutions

Would you like me to dive deeper into any of these?
```

#### Example 3: Ask Generator to Create a New Agent

**You**:
```
We need a marketing specialist agent to help with our campaign
```

**Generator Agent**:
```
I can create a Marketing Specialist agent for you with the following capabilities:
- Market research
- Content creation
- Campaign planning
- Analytics

Should I proceed with creating this agent?
```

### Chat Features

- **Multi-word Messages**: Type natural sentences and questions
- **Character Limit**: Up to 2000 characters per message
- **Message History**: Scroll up to see previous conversations
- **Real-time Updates**: Responses appear instantly via WebSocket

---

## CLI Interface

The CLI (Command-Line Interface) provides powerful text-based interaction with the system.

### Available Commands

#### `/help`
Display all available commands

**Example**:
```
> /help

Available Commands:
/help              - Show this help message
/status            - Show system status
/agents            - List all agents
/driver <message>  - Send message to Driver agent
/creator <message> - Send message to Creator agent
/generator <message> - Send message to Generator agent
/clear             - Clear terminal output
```

#### `/status`
Show current system status

**Example**:
```
> /status

System Status: Online
Agents Initialized: Yes
Active Workflows: 3
Database: Connected
```

#### `/agents`
List all agents in the system

**Example**:
```
> /agents

Available Agents:
1. Driver (CEO) - Status: idle
2. Creator (Researcher) - Status: busy
3. Generator (HR) - Status: idle

Total: 3 agents
```

#### `/driver <message>`
Send a message to the Driver agent

**Example**:
```
> /driver Create a new project plan for AI product launch

[Driver]: I'll create a comprehensive project plan for the AI product launch.
I'll coordinate with Creator for market research and Generator for team building...
```

#### `/creator <message>`
Send a message to the Creator agent

**Example**:
```
> /creator What are the top AI frameworks for 2025?

[Creator]: Based on my research, the top AI frameworks for 2025 are:
1. AutoGen - Multi-agent systems
2. LangChain - LLM applications
3. PyTorch 2.0 - Deep learning
...
```

#### `/generator <message>`
Send a message to the Generator agent

**Example**:
```
> /generator Create a data analyst agent

[Generator]: Creating a Data Analyst agent with capabilities:
- Data processing
- Statistical analysis
- Visualization
Agent created successfully!
```

#### `/clear`
Clear the terminal output

**Example**:
```
> /clear

[Terminal cleared]
```

### CLI Features

- **Command History**: Use ↑/↓ arrow keys to navigate previous commands
- **Tab Completion**: (Future feature)
- **Colored Output**: Different colors for commands, output, and errors
- **Timestamps**: Each output shows when it was generated

---

## Working with Agents

### The Three Core Agents

#### 1. Driver Agent (CEO)

**Role**: Task orchestration and project management

**When to Use**:
- Coordinating multiple tasks
- Getting project status updates
- Delegating work to other agents
- Managing workflows

**Example Questions**:
- "What's the status of our current projects?"
- "Create a plan for launching our product"
- "Delegate market research to Creator"
- "What tasks are pending?"

---

#### 2. Creator Agent (Researcher)

**Role**: Research and idea generation using RAG

**When to Use**:
- Researching topics
- Generating ideas
- Finding information
- Creating content

**Example Questions**:
- "Research AI trends in healthcare"
- "Generate 5 ideas for a startup pitch"
- "What are the best practices for React development?"
- "Summarize the latest AI news"

**Special Features**:
- **RAG (Retrieval Augmented Generation)**: Uses ChromaDB vector database
- **Knowledge Base**: 10+ sample documents about tech topics
- **Semantic Search**: Finds relevant information intelligently

---

#### 3. Generator Agent (HR)

**Role**: Dynamic agent creation

**When to Use**:
- Need specialized expertise
- Scaling the team
- Creating task-specific agents
- Building custom workflows

**Example Questions**:
- "Create a marketing specialist agent"
- "We need a data analyst for our project"
- "Build an agent for customer support"
- "What agents can you create?"

**Agent Types You Can Create**:
- Marketing Specialist
- Data Analyst
- Customer Support
- Content Writer
- Sales Representative
- Technical Writer
- And more!

---

### Agent States

Agents can be in different states:

| State | Meaning | What to Do |
|-------|---------|------------|
| **idle** | Agent is available | Send messages freely |
| **busy** | Agent is processing | Wait for response |
| **error** | Agent encountered an issue | Check error message, try again |

---

## Workflows

Workflows are multi-step processes coordinated across agents.

### Creating a Workflow

#### Method 1: Via Chat (Recommended)

1. Go to **Chat Demo**
2. Select **Driver** agent
3. Describe your workflow:
   ```
   I need to launch a new AI product. Can you create a workflow?
   ```

4. Driver will:
   - Break down the task
   - Create a workflow
   - Coordinate with other agents
   - Report progress

#### Method 2: Via API

```bash
curl -X POST http://localhost:5000/api/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Launch new AI product"}'
```

### Workflow Example

**Task**: "Launch a new AI product"

**Workflow Steps**:
1. **Market Research** (Creator)
   - Research AI market trends
   - Identify target audience
   - Analyze competitors

2. **Product Planning** (Driver)
   - Define features
   - Create roadmap
   - Set milestones

3. **Team Building** (Generator)
   - Create Marketing Agent
   - Create Sales Agent
   - Create Support Agent

4. **Execution** (All Agents)
   - Marketing campaign
   - Sales outreach
   - Customer support setup

### Monitoring Workflows

**Via Dashboard**:
- View active workflows
- See completion status
- Track agent assignments

**Via API**:
```bash
curl http://localhost:5000/api/workflows/1/status
```

**Via CLI**:
```
> /status
```

---

## Tips & Best Practices

### 1. Clear Communication

✅ **Good**:
```
Create a marketing plan for an AI chatbot targeting small businesses
```

❌ **Not Recommended**:
```
marketing
```

**Why**: Agents work better with specific, detailed instructions.

---

### 2. Use the Right Agent

| Task | Best Agent |
|------|------------|
| Project coordination | Driver |
| Research & ideas | Creator |
| Team building | Generator |
| General questions | Any agent |

---

### 3. Break Down Complex Tasks

Instead of:
```
Build and launch a complete SaaS product
```

Try:
```
Step 1: Research SaaS market trends (Creator)
Step 2: Create product roadmap (Driver)
Step 3: Build development team (Generator)
```

---

### 4. Leverage Agent Strengths

**Creator's RAG Knowledge**:
- "What does my knowledge base say about Python?"
- "Search for information about Flask"

**Driver's Coordination**:
- "Coordinate research and development tasks"
- "Create a timeline for all agents"

**Generator's Flexibility**:
- "Create a specialized agent for X"
- "Build a team of 3 agents for Y project"

---

### 5. Check Agent Status

Before sending complex tasks, check if agents are available:

**Dashboard**: Look at agent status indicators
**CLI**: Use `/agents` command
**Chat**: Agent status shows in the UI

---

### 6. Use Workflows for Big Projects

For multi-step projects:
1. Describe the entire project to Driver
2. Let Driver create a workflow
3. Monitor progress via Dashboard
4. Intervene only when needed

---

## Troubleshooting

### Issue: "Agent system not initialized"

**Solution**:
```bash
curl -X POST http://localhost:5000/api/init
```

Or restart the backend:
```bash
cd backend
uv run python run.py
```

---

### Issue: "No response from agent"

**Possible Causes**:
1. Agent is still processing (wait longer)
2. WebSocket connection lost (refresh page)
3. Backend crashed (check backend terminal)

**Solution**:
1. Wait 30 seconds
2. Refresh the browser
3. Restart backend if needed

---

### Issue: "WebSocket connection failed"

**Solution**:
1. Check backend is running: `http://localhost:5000`
2. Check CORS settings in `.env`
3. Use `run.py` (NOT `flask run`)

---

### Issue: "Message not sending"

**Checklist**:
- [ ] Message is not empty
- [ ] Under 2000 characters
- [ ] Agent is selected (Chat Demo)
- [ ] Backend is running
- [ ] WebSocket connected (check browser console)

---

## Keyboard Shortcuts

| Shortcut | Action | Where |
|----------|--------|-------|
| Enter | Send message | Chat, CLI |
| ↑ | Previous command | CLI |
| ↓ | Next command | CLI |
| Ctrl+L | Clear CLI | CLI |

---

## Getting Help

### In-App Help

- **CLI**: Type `/help`
- **Chat**: Ask any agent "How do I...?"

### Documentation

- **API Docs**: `docs/api.md`
- **Agent Docs**: `docs/agents.md`
- **Architecture**: `docs/architecture.md`

### Support

- **GitHub Issues**: [Report bugs](https://github.com/your-repo/issues)
- **Email**: support@virtual-startup.com

---

## Next Steps

Now that you know the basics:

1. **Explore the Dashboard** - Get familiar with the interface
2. **Chat with Agents** - Try all three core agents
3. **Use the CLI** - Practice commands
4. **Create a Workflow** - Try a multi-step project
5. **Build Custom Agents** - Use Generator to expand your team

**Happy building! 🚀**

---

**Version**: 1.0.0
**Last Updated**: October 18, 2025
**Questions?** Check `docs/` folder for more documentation
