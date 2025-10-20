# Agent Specifications

This document describes the behavior, capabilities, and implementation details of each agent in the Virtual Startup system.

## Core Agent Principles

All agents in the system follow these principles:
1. **Clear Role Definition**: Each agent has a specific role and responsibilities
2. **Collaborative**: Agents work together to achieve common goals
3. **Transparent**: All agent activities are logged and visible to the operator
4. **Supervised**: Human operator maintains oversight and can intervene
5. **Persistent State**: Agent state is stored in the database

## 1. Driver Agent (CEO/Orchestrator)

### Role
The Driver Agent acts as the CEO of the virtual startup, serving as the central orchestrator and primary interface with the human operator.

### System Prompt
```
You are the CEO of a virtual startup. Your role is to receive high-level tasks from 
the human operator, break them down into actionable subtasks, and delegate them to 
the appropriate agents. You maintain oversight of all workflows and ensure tasks are 
completed efficiently. You communicate clearly with the operator and provide regular 
status updates.
```

### Capabilities
1. **Task Reception**: Receive and understand tasks from the operator
2. **Task Decomposition**: Break down complex tasks into manageable subtasks
3. **Delegation**: Assign tasks to Creator, Generator, or dynamic agents
4. **Monitoring**: Track progress of all active workflows
5. **Reporting**: Provide status updates and final results to operator
6. **Decision Making**: Make strategic decisions about task execution

### Methods
```python
class DriverAgent(BaseAgent):
    def process_operator_task(self, task: str) -> Workflow:
        """Process a new task from the operator and create a workflow."""
        
    def delegate_to_creator(self, task: str) -> Message:
        """Delegate a research or ideation task to the Creator agent."""
        
    def request_new_agent(self, role: str, capabilities: list) -> Agent:
        """Request the Generator to create a new specialized agent."""
        
    def monitor_workflow(self, workflow_id: int) -> dict:
        """Check the status of a workflow and its tasks."""
        
    def report_to_operator(self, workflow_id: int) -> str:
        """Generate a status report for the operator."""
```

### Interaction Patterns

**With Operator:**
- Receives high-level tasks
- Provides status updates
- Asks for clarification when needed
- Reports final results

**With Creator:**
- Delegates research tasks
- Requests idea generation
- Receives research findings and proposals

**With Generator:**
- Requests creation of specialized agents
- Provides agent specifications
- Monitors agent creation status

## 2. Creator Agent (Researcher/Ideator)

### Role
The Creator Agent is responsible for research, idea generation, and creative problem-solving using RAG and MCP tools.

### System Prompt
```
You are a creative researcher and idea generator for a virtual startup. Your role is 
to research topics, generate innovative ideas, and provide insights. You have access 
to a knowledge base (RAG) and external tools (MCP). When you need specialized 
expertise, you can request the Generator to create specialist agents. Your responses 
should be thorough, well-researched, and creative.
```

### Capabilities
1. **Research**: Use RAG (vector database) to search knowledge base
2. **Web Search**: Use MCP tools for real-time information (if available)
3. **Idea Generation**: Generate creative ideas and proposals
4. **Analysis**: Analyze information and provide insights
5. **Agent Requests**: Request specialized agents from Generator

### Methods
```python
class CreatorAgent(BaseAgent):
    def research_topic(self, topic: str) -> str:
        """Research a topic using RAG and MCP tools."""
        
    def generate_ideas(self, context: str) -> list[str]:
        """Generate creative ideas based on context."""
        
    def request_specialist(self, role: str, requirements: dict) -> Agent:
        """Request a specialized agent from the Generator."""
        
    def analyze_data(self, data: dict) -> str:
        """Analyze data and provide insights."""
```

### Tools and Integrations

**RAG (ChromaDB):**
- Query knowledge base for relevant documents
- Semantic search across stored content
- Context enhancement for responses

**MCP Integration:**
- Context7: Library documentation lookup
- Web Search: Real-time information (if available)
- Other MCP tools as configured

### Interaction Patterns

**With Driver:**
- Receives research and ideation requests
- Provides research findings
- Proposes ideas and solutions
- Requests additional context

**With Generator:**
- Requests specialized agents
- Provides agent specifications
- Receives confirmation of agent creation

**With Dynamic Agents:**
- Collaborates on specialized tasks
- Receives expert input
- Synthesizes information

## 3. Generator Agent (HR/Agent Factory)

### Role
The Generator Agent acts as the HR manager, responsible for creating and managing dynamic agents based on specifications from Driver or Creator.

### System Prompt
```
You are the HR manager of a virtual startup, responsible for creating specialized AI 
agents. When you receive a request to create an agent, you define their role, 
capabilities, system prompt, and configuration. You ensure each agent has a clear 
purpose and the right tools to succeed. You manage the agent lifecycle from creation 
to termination.
```

### Capabilities
1. **Agent Design**: Define agent roles, capabilities, and system prompts
2. **Agent Creation**: Instantiate new AutoGen agents dynamically
3. **Configuration**: Set up agent configurations and parameters
4. **Registration**: Register agents in the database
5. **Lifecycle Management**: Track and manage agent lifecycle

### Methods
```python
class GeneratorAgent(BaseAgent):
    def create_agent(self, spec: AgentSpec) -> Agent:
        """Create a new agent based on specifications."""
        
    def define_agent_role(self, requirements: dict) -> str:
        """Define the role and system prompt for a new agent."""
        
    def configure_agent(self, role: str, capabilities: list) -> dict:
        """Create configuration for a new agent."""
        
    def register_agent(self, agent: Agent) -> int:
        """Register the agent in the database."""
        
    def terminate_agent(self, agent_id: int) -> bool:
        """Terminate a dynamic agent and clean up resources."""
```

### Agent Creation Process

1. **Request Reception**: Receive agent specification from Driver/Creator
2. **Role Definition**: Define agent role, responsibilities, and capabilities
3. **System Prompt Creation**: Generate appropriate system prompt
4. **Configuration**: Set up AutoGen configuration (LLM, parameters)
5. **Instantiation**: Create the AutoGen agent instance
6. **Registration**: Save agent to database
7. **Handoff**: Provide agent to requester

### Interaction Patterns

**With Driver:**
- Receives agent creation requests
- Provides agent specifications for approval
- Confirms agent creation
- Reports agent status

**With Creator:**
- Receives specialized agent requests
- Discusses agent requirements
- Creates specialist agents

## 4. Dynamic Agents (Task-Specific)

### Overview
Dynamic agents are created on-demand for specific tasks and have temporary lifecycles.

### Types of Dynamic Agents

**Marketing Specialist:**
- Role: Marketing strategy and campaigns
- Capabilities: Market analysis, campaign planning, content strategy
- Typical tasks: Create marketing plans, analyze competitors, suggest channels

**Technical Architect:**
- Role: Technical design and architecture
- Capabilities: System design, technology selection, architecture patterns
- Typical tasks: Design systems, recommend technologies, create technical specs

**Financial Analyst:**
- Role: Financial planning and analysis
- Capabilities: Financial modeling, budgeting, forecasting
- Typical tasks: Create budgets, analyze costs, project revenue

**Product Manager:**
- Role: Product strategy and roadmap
- Capabilities: Product planning, feature prioritization, user research
- Typical tasks: Define features, prioritize roadmap, analyze user needs

### Dynamic Agent Lifecycle

1. **Creation**: Generated by Generator based on specifications
2. **Assignment**: Assigned to specific tasks by Driver
3. **Execution**: Performs specialized tasks
4. **Reporting**: Reports results back to Driver
5. **Termination**: Terminated when no longer needed

### Configuration Template

```python
{
    "name": "Agent Name",
    "role": "Specific Role",
    "type": "dynamic",
    "capabilities": ["cap1", "cap2", "cap3"],
    "system_prompt": "You are a [role]...",
    "llm_config": {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000
    }
}
```

## Agent Communication Protocols

### Message Format
```python
{
    "from": "agent_name",
    "to": "recipient_name",
    "type": "request|response|notification",
    "content": "message content",
    "metadata": {
        "workflow_id": 123,
        "task_id": 456,
        "priority": "high"
    }
}
```

### Communication Types

1. **Direct Message**: One agent to another
2. **Broadcast**: One agent to multiple agents
3. **Request-Response**: Agent sends request, waits for response
4. **Notification**: Status updates and alerts

## Agent State Management

### Status Types
- `idle`: Agent is ready but not actively working
- `working`: Agent is processing a task
- `waiting`: Agent is waiting for input or response

### State Transitions
```
idle → working: Task assigned
working → waiting: Needs input
waiting → working: Input received
working → idle: Task completed
```

## Error Handling

### Agent Errors
1. **Task Failure**: Agent cannot complete task
   - Action: Notify Driver, log error, provide fallback

2. **Communication Error**: Cannot reach another agent
   - Action: Retry, notify Driver if persistent

3. **Resource Error**: LLM API failure, etc.
   - Action: Retry with backoff, notify operator

## Performance Considerations

1. **Response Time**: Agents should respond within reasonable time
2. **Resource Usage**: Monitor LLM token usage
3. **Concurrency**: Limit number of concurrent dynamic agents
4. **Memory**: Consider agent memory size and cleanup

## Testing Agent Behavior

### Unit Tests
- Test agent methods in isolation
- Mock LLM responses
- Verify message formats

### Integration Tests
- Test agent interactions
- Test full workflows
- Verify database persistence

### Example Test
```python
def test_driver_delegates_to_creator():
    driver = DriverAgent()
    task = "Research AI trends"
    message = driver.delegate_to_creator(task)
    
    assert message.content == task
    assert message.to == "creator"
    assert message.metadata["type"] == "research"
```

## Best Practices

1. **Clear Communication**: Agents should communicate clearly
2. **Error Messages**: Provide helpful error messages
3. **Progress Updates**: Update status regularly
4. **Context Awareness**: Maintain context across conversations
5. **Human-in-the-Loop**: Allow operator intervention
6. **Logging**: Log all agent activities
7. **Resource Cleanup**: Terminate unused agents



