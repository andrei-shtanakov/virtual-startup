"""Three-Pane Terminal User Interface for Virtual Startup."""

import asyncio
from datetime import datetime
from textwrap import fill
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, DataTable, Log, Input, Static
from textual.binding import Binding
import requests

API_URL = "http://localhost:5000/api"


class AgentTable(DataTable):
    """Table showing agent status."""

    def on_mount(self) -> None:
        """Setup table columns when mounted."""
        self.add_columns("ID", "Name", "Role", "Status")
        self.cursor_type = "row"
        self.refresh_agents()

    def refresh_agents(self) -> None:
        """Fetch and display agents from API."""
        try:
            response = requests.get(f"{API_URL}/agents", timeout=2)
            if response.ok:
                agents = response.json()
                self.clear()
                for agent in agents:
                    self.add_row(
                        str(agent["id"]),
                        agent["name"],
                        agent["role"][:30],  # Truncate long roles
                        agent["status"]
                    )
        except Exception as e:
            self.clear()
            self.add_row("Error", str(e)[:20], "", "")


class ChatLog(Log):
    """Chat window for agent interactions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_id = 1  # Default to Driver
        self.max_width = 80  # Default width, will be updated on mount

    def on_mount(self) -> None:
        """Initialize chat log."""
        # Calculate max width based on panel size
        self.max_width = max(40, self.size.width - 4)  # Leave padding
        self.write("Welcome to Virtual Startup Chat!")
        self.write("Select an agent from the left and start typing...")
        self.write("")  # Add spacing

    def write_wrapped(self, text: str) -> None:
        """Write text with proper wrapping."""
        if not text.strip():
            self.write("")
            return

        # Wrap text to fit within the panel width
        wrapped = fill(text, width=self.max_width, break_long_words=True, break_on_hyphens=True)
        self.write(wrapped)


class CLILog(Log):
    """CLI command output window."""

    def on_mount(self) -> None:
        """Initialize CLI log."""
        self.write("Virtual Startup CLI v1.0.0")
        self.write("Type /help for available commands")


class ChatInput(Input):
    """Input field for chat messages."""

    def __init__(self, **kwargs):
        super().__init__(placeholder="Type a message...", **kwargs)


class CLIInput(Input):
    """Input field for CLI commands."""

    def __init__(self, **kwargs):
        super().__init__(placeholder="Type a command (e.g., /status)...", **kwargs)


class VirtualStartupTUI(App):
    """Three-pane TUI application for Virtual Startup."""

    CSS = """
    Screen {
        background: $background;
    }

    #left-panel {
        width: 30;
        border: solid $accent;
        padding: 1;
    }

    #center-panel {
        width: 1fr;
        border: solid $accent;
        padding: 1;
    }

    #right-panel {
        width: 40;
        border: solid $accent;
        padding: 1;
    }

    .panel-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    DataTable {
        height: 100%;
    }

    Log {
        height: 1fr;
        border: solid $primary;
        overflow-x: hidden;
        overflow-y: auto;
    }

    #chat-log {
        height: 1fr;
    }

    Input {
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "refresh", "Refresh Agents"),
        Binding("c", "clear_chat", "Clear Chat"),
        Binding("ctrl+l", "clear_cli", "Clear CLI"),
    ]

    TITLE = "Virtual Startup - AI Agent Management"

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()

        with Horizontal():
            # Left Panel: Agent Status
            with Vertical(id="left-panel"):
                yield Static("🤖 Agents", classes="panel-title")
                yield AgentTable()

            # Center Panel: Chat
            with Vertical(id="center-panel"):
                yield Static("💬 Chat", classes="panel-title")
                yield ChatLog(id="chat-log")
                yield ChatInput(id="chat-input")

            # Right Panel: CLI
            with Vertical(id="right-panel"):
                yield Static("⌨️  CLI", classes="panel-title")
                yield CLILog(id="cli-log")
                yield CLIInput(id="cli-input")

        yield Footer()

    def on_mount(self) -> None:
        """Setup application state."""
        self.selected_agent_id = 1
        self.query_one(ChatInput).focus()

    def action_refresh(self) -> None:
        """Refresh agent list."""
        agent_table = self.query_one(AgentTable)
        agent_table.refresh_agents()
        cli_log = self.query_one("#cli-log", CLILog)
        cli_log.write(f"[{datetime.now().strftime('%H:%M:%S')}] Agents refreshed")

    def action_clear_chat(self) -> None:
        """Clear chat log."""
        chat_log = self.query_one("#chat-log", ChatLog)
        chat_log.clear()
        chat_log.write("Chat cleared")

    def action_clear_cli(self) -> None:
        """Clear CLI log."""
        cli_log = self.query_one("#cli-log", CLILog)
        cli_log.clear()
        cli_log.write("CLI cleared")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle agent selection."""
        row_key = event.row_key
        table = event.data_table
        row_data = table.get_row(row_key)

        self.selected_agent_id = int(row_data[0])
        agent_name = row_data[1]

        chat_log = self.query_one("#chat-log", ChatLog)
        chat_log.write("")
        chat_log.write(f"--- Switched to {agent_name} (ID: {self.selected_agent_id}) ---")
        chat_log.write("")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "chat-input":
            await self.handle_chat_message(event.value)
        elif event.input.id == "cli-input":
            await self.handle_cli_command(event.value)

        event.input.value = ""

    async def handle_chat_message(self, message: str) -> None:
        """Send chat message to agent."""
        if not message.strip():
            return

        chat_log = self.query_one("#chat-log", ChatLog)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Write user message - each on a new line with wrapping
        chat_log.write("")  # Blank line before message
        chat_log.write(f"[{timestamp}] You:")
        chat_log.write_wrapped(message)

        try:
            # Send message to backend
            response = await asyncio.to_thread(
                requests.post,
                f"{API_URL}/agents/{self.selected_agent_id}/message",
                json={"message": message},
                timeout=10
            )

            if response.ok:
                data = response.json()
                response_text = data.get("response", "No response")
                # Write agent response - each on a new line with wrapping
                chat_log.write("")  # Blank line before message
                chat_log.write(f"[{timestamp}] Agent:")
                chat_log.write_wrapped(response_text)
            else:
                chat_log.write("")
                chat_log.write(f"[{timestamp}] Error: {response.status_code}")
        except Exception as e:
            chat_log.write("")
            chat_log.write(f"[{timestamp}] Error: {str(e)}")

    async def handle_cli_command(self, command: str) -> None:
        """Execute CLI command."""
        if not command.strip():
            return

        cli_log = self.query_one("#cli-log", CLILog)
        timestamp = datetime.now().strftime("%H:%M:%S")

        cli_log.write(f"[{timestamp}] $ {command}")

        cmd = command.strip().lower()

        if cmd in ["/help", "/?", "/h"]:
            cli_log.write("Available commands:")
            cli_log.write("  /status    - Show system status")
            cli_log.write("  /agents    - List all agents")
            cli_log.write("  /clear     - Clear CLI output")
            cli_log.write("  /help      - Show this help")

        elif cmd == "/status":
            try:
                response = await asyncio.to_thread(
                    requests.get,
                    f"{API_URL}/status",
                    timeout=2
                )
                if response.ok:
                    data = response.json()
                    cli_log.write(f"  API: {data.get('api', 'unknown')}")
                    cli_log.write(f"  Agents: {data.get('agents_initialized', False)}")
                    cli_log.write(f"  Database: {data.get('database', 'unknown')}")
                else:
                    cli_log.write(f"  Error: {response.status_code}")
            except Exception as e:
                cli_log.write(f"  Error: {str(e)}")

        elif cmd == "/agents":
            try:
                response = await asyncio.to_thread(
                    requests.get,
                    f"{API_URL}/agents",
                    timeout=2
                )
                if response.ok:
                    agents = response.json()
                    cli_log.write(f"Found {len(agents)} agent(s):")
                    for agent in agents:
                        cli_log.write(f"  [{agent['id']}] {agent['name']} - {agent['status']}")
                else:
                    cli_log.write(f"  Error: {response.status_code}")
            except Exception as e:
                cli_log.write(f"  Error: {str(e)}")

        elif cmd == "/clear":
            cli_log.clear()
            cli_log.write("CLI cleared")

        else:
            cli_log.write(f"  Unknown command: {command}")
            cli_log.write("  Type /help for available commands")


def main():
    """Run the TUI application."""
    app = VirtualStartupTUI()
    app.run()


if __name__ == "__main__":
    main()
