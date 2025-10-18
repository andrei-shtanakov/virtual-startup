"""Initialize core agents in the database."""

from app import create_app, db
from app.models import Agent


def init_core_agents() -> None:
    """Create the three core agents in the database."""
    app = create_app()

    with app.app_context():
        # Check if agents already exist
        existing_agents = Agent.query.filter(
            Agent.type.in_(["driver", "creator", "generator"])
        ).count()

        if existing_agents > 0:
            print(f"Found {existing_agents} core agents already in database.")
            print("Skipping initialization.")
            return

        # Create Driver Agent
        driver = Agent(
            name="Driver",
            type="driver",
            role="CEO and Task Orchestrator",
            status="idle",
            config={
                "model": "gpt-4",
                "temperature": 0.7,
                "system_prompt": (
                    "You are the CEO of a virtual startup. Your role is to "
                    "receive high-level tasks from the human operator, break "
                    "them down into actionable subtasks, and delegate them to "
                    "the appropriate agents. You maintain oversight of all "
                    "workflows and ensure tasks are completed efficiently."
                ),
            },
        )

        # Create Creator Agent
        creator = Agent(
            name="Creator",
            type="creator",
            role="Researcher and Idea Generator",
            status="idle",
            config={
                "model": "gpt-4",
                "temperature": 0.8,
                "system_prompt": (
                    "You are a creative researcher and idea generator for a "
                    "virtual startup. Your role is to research topics, generate "
                    "innovative ideas, and provide insights. You have access to "
                    "a knowledge base (RAG) and external tools (MCP). When you "
                    "need specialized expertise, you can request the Generator "
                    "to create specialist agents."
                ),
            },
        )

        # Create Generator Agent
        generator = Agent(
            name="Generator",
            type="generator",
            role="HR and Agent Factory",
            status="idle",
            config={
                "model": "gpt-4",
                "temperature": 0.6,
                "system_prompt": (
                    "You are the HR manager of a virtual startup, responsible "
                    "for creating specialized AI agents. When you receive a "
                    "request to create an agent, you define their role, "
                    "capabilities, system prompt, and configuration. You ensure "
                    "each agent has a clear purpose and the right tools to "
                    "succeed."
                ),
            },
        )

        # Add agents to database
        db.session.add(driver)
        db.session.add(creator)
        db.session.add(generator)
        db.session.commit()

        print("✅ Core agents initialized successfully!")
        print(f"  - Driver (ID: {driver.id})")
        print(f"  - Creator (ID: {creator.id})")
        print(f"  - Generator (ID: {generator.id})")


if __name__ == "__main__":
    init_core_agents()

