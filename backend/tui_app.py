"""Three-Pane Terminal User Interface for Virtual Startup."""

import asyncio
from datetime import datetime
from textwrap import wrap
from typing import Iterable
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, DataTable, Log, Input, Static
from textual.binding import Binding
from textual.events import Resize
import requests

API_URL = "http://localhost:5000/api"


class AgentTable(DataTable):
    """Table showing agent status."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_agents: list[dict] = []

    def on_mount(self) -> None:
        """Setup table columns when mounted."""
        self.add_columns("ID", "Name", "Role", "Status")
        self.cursor_type = "row"

    def refresh_agents(self) -> list[dict]:
        """Fetch and display agents from API."""
        agents: list[dict] = []
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
                        agent["status"],
                    )
                if agents:
                    self.cursor_coordinate = (0, 0)
        except Exception as e:
            self.clear()
            self.add_row("Error", str(e)[:20], "", "")
            agents = []

        self.last_agents = agents
        return agents


class PlainLog(Log):
    """Log widget with newline-aware helpers."""

    def write_line(self, text: str = "", *, scroll_end: bool | None = None) -> None:
        """Write a line to the log ensuring it ends with a newline."""
        super().write(f"{text}\n", scroll_end=scroll_end)

    def write_lines(self, lines: Iterable[str], *, scroll_end: bool | None = None) -> None:
        """Write multiple lines to the log."""
        for line in lines:
            self.write_line(line, scroll_end=scroll_end)


class ChatLog(PlainLog):
    """Chat window for agent interactions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_width = 80  # Default width, will be updated on mount

    def on_mount(self) -> None:
        """Initialize chat log."""
        self._update_max_width()
        self.write_line("Welcome to Virtual Startup Chat!")
        self.write_line("Select an agent from the left and start typing...")
        self.write_line()  # Add spacing

    def on_resize(self, event: Resize) -> None:
        """Update wrapping width when the widget resizes."""
        self._update_max_width(event.size.width)

    def _update_max_width(self, width: int | None = None) -> None:
        """Compute the available width for wrapping."""
        current_width = width if width is not None else self.size.width
        if current_width and current_width > 0:
            self.max_width = max(20, current_width - 4)

    def write_wrapped(self, text: str) -> None:
        """Write text with proper wrapping."""
        if not text.strip():
            self.write_line()
            return

        available_width = self.max_width

        for paragraph in text.splitlines() or [""]:
            if not paragraph.strip():
                self.write_line()
                continue

            wrapped_lines = wrap(
                paragraph,
                width=available_width,
                break_long_words=True,
                break_on_hyphens=True,
            )
            if not wrapped_lines:
                self.write_line()
                continue

            for line in wrapped_lines:
                self.write_line(line)


class CLILog(PlainLog):
    """CLI command output window."""

    def on_mount(self) -> None:
        """Initialize CLI log."""
        self.write_line("Virtual Startup CLI v1.0.0")
        self.write_line("Type /help for available commands")


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
        self.selected_agent_id: int | None = None
        agent_table = self.query_one(AgentTable)
        agents = agent_table.refresh_agents()
        self._ensure_agent_selected(agents, initial=True)
        self.query_one(ChatInput).focus()

    def action_refresh(self) -> None:
        """Refresh agent list."""
        agent_table = self.query_one(AgentTable)
        agents = agent_table.refresh_agents()
        self._ensure_agent_selected(agents)
        cli_log = self.query_one("#cli-log", CLILog)
        cli_log.write_line(f"[{datetime.now().strftime('%H:%M:%S')}] Agents refreshed")

    def action_clear_chat(self) -> None:
        """Clear chat log."""
        chat_log = self.query_one("#chat-log", ChatLog)
        chat_log.clear()
        chat_log.write_line("Chat cleared")

    def action_clear_cli(self) -> None:
        """Clear CLI log."""
        cli_log = self.query_one("#cli-log", CLILog)
        cli_log.clear()
        cli_log.write_line("CLI cleared")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle agent selection."""
        row_key = event.row_key
        table = event.data_table
        row_data = table.get_row(row_key)

        try:
            self.selected_agent_id = int(row_data[0])
        except (TypeError, ValueError):
            self.selected_agent_id = None
            chat_log = self.query_one("#chat-log", ChatLog)
            chat_log.write_line()
            chat_log.write_line("No valid agent selected.")
            return

        agent_name = row_data[1]

        chat_log = self.query_one("#chat-log", ChatLog)
        chat_log.write_line()
        chat_log.write_line(f"--- Switched to {agent_name} (ID: {self.selected_agent_id}) ---")
        chat_log.write_line()

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
        if self.selected_agent_id is None:
            chat_log.write_line()
            chat_log.write_line("No agent is available. Initialize agents and refresh.")
            return
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Write user message - each on a new line with wrapping
        chat_log.write_line()  # Blank line before message
        chat_log.write_line(f"[{timestamp}] You:")
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
                chat_log.write_line()  # Blank line before message
                chat_log.write_line(f"[{timestamp}] Agent:")
                chat_log.write_wrapped(response_text)
            else:
                chat_log.write_line()
                chat_log.write_line(f"[{timestamp}] Error: {response.status_code}")
        except Exception as e:
            chat_log.write_line()
            chat_log.write_line(f"[{timestamp}] Error: {str(e)}")

    async def handle_cli_command(self, command: str) -> None:
        """Execute CLI command."""
        if not command.strip():
            return

        cli_log = self.query_one("#cli-log", CLILog)
        timestamp = datetime.now().strftime("%H:%M:%S")

        cli_log.write_line(f"[{timestamp}] $ {command}")

        cmd = command.strip().lower()

        if cmd in ["/help", "/?", "/h"]:
            cli_log.write_line("Available commands:")
            cli_log.write_line("  /status    - Show system status")
            cli_log.write_line("  /agents    - List all agents")
            cli_log.write_line("  /clear     - Clear CLI output")
            cli_log.write_line("  /help      - Show this help")

        elif cmd == "/status":
            try:
                response = await asyncio.to_thread(
                    requests.get,
                    f"{API_URL}/status",
                    timeout=2
                )
                if response.ok:
                    data = response.json()
                    cli_log.write_line(f"  API: {data.get('api', 'unknown')}")
                    cli_log.write_line(f"  Agents: {data.get('agents_initialized', False)}")
                    cli_log.write_line(f"  Database: {data.get('database', 'unknown')}")
                else:
                    cli_log.write_line(f"  Error: {response.status_code}")
            except Exception as e:
                cli_log.write_line(f"  Error: {str(e)}")

        elif cmd == "/agents":
            try:
                response = await asyncio.to_thread(
                    requests.get,
                    f"{API_URL}/agents",
                    timeout=2
                )
                if response.ok:
                    agents = response.json()
                    cli_log.write_line(f"Found {len(agents)} agent(s):")
                    for agent in agents:
                        cli_log.write_line(f"  [{agent['id']}] {agent['name']} - {agent['status']}")
                else:
                    cli_log.write_line(f"  Error: {response.status_code}")
            except Exception as e:
                cli_log.write_line(f"  Error: {str(e)}")

        elif cmd == "/clear":
            cli_log.clear()
            cli_log.write_line("CLI cleared")

        else:
            cli_log.write_line(f"  Unknown command: {command}")
            cli_log.write_line("  Type /help for available commands")

    def _ensure_agent_selected(
        self, agents: list[dict], initial: bool = False
    ) -> None:
        """Select the first available agent if none is chosen."""
        chat_log = self.query_one("#chat-log", ChatLog)

        if not agents:
            self.selected_agent_id = None
            if initial:
                chat_log.write_line("No agents available yet. Run /api/init when ready.")
            return

        current_ids = {agent["id"] for agent in agents}

        if self.selected_agent_id not in current_ids:
            self.selected_agent_id = agents[0]["id"]
            chat_log.write_line()
            chat_log.write_line(
                f"Defaulting to {agents[0]['name']} (ID: {self.selected_agent_id})."
            )


def main():
    """Run the TUI application."""
    app = VirtualStartupTUI()
    app.run()


if __name__ == "__main__":
    main()
