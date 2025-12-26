# Core Python imports
import time
import socket
import logging
import asyncio

# Textual imports
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log
from textual.binding import Binding
from textual.logging import TextualHandler

# Local project imports
from state import MachineState
from lifecycle import Lifecycle

# Emojis for the UI
EMOJI_ROBOT = "🤖"
EMOJI_STATUS = "📡"
EMOJI_CMD_TIME = "⏱️"

class MachineStatus(Static):
    """A widget to display machine status."""
    def __init__(self, state: MachineState):
        super().__init__()
        self.state = state
        self.set_interval(0.1, self.update_status)

    def update_status(self) -> None:
        """Update the status display."""
        # Single line status display
        status_text = (
            f"[bold]{EMOJI_ROBOT} ID:[/bold] {self.state.machine_id} | "
            f"[bold]{EMOJI_STATUS} STATE:[/bold] {self.state.lifecycle.name} | "
            f"[bold]{EMOJI_CMD_TIME} LAST CMD:[/bold] {time.time() - self.state.last_command_ts:.2f}s ago"
        )
        self.update(status_text)


class MachineTUI(App):
    """A Textual TUI for monitoring the machine."""

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    DEFAULT_CSS = """
    App {
        layout: vertical;
    }
    MachineStatus {
        height: 1;
        dock: top;
        content-align: center middle;
    }
    Log {
        height: 1fr;
    }
    """

    def __init__(self, state: MachineState):
        super().__init__()
        self.state = state
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target = ("127.0.0.1", 9999) # TODO: Get from config

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        logging.info("TUI: compose method called.")
        yield Header(name="X-Machine Logs")
        yield MachineStatus(self.state)
        yield Log(id="log")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        logging.info("TUI: on_mount method called.")
        log_widget = self.query_one(Log)

        # Get the root logger and add TextualHandler
        root_logger = logging.getLogger()
        # Remove existing TextualHandlers to prevent duplicates if on_mount is called multiple times
        for handler in root_logger.handlers[:]:
            if isinstance(handler, TextualHandler):
                root_logger.removeHandler(handler)
        root_logger.addHandler(TextualHandler(log_widget))

    async def on_ready(self) -> None:
        """Called when the app is mounted and the DOM is ready."""
        logging.info("TUI: on_ready method called.")

    async def action_quit(self) -> None:
        """Called when the 'q' key is pressed."""
        logging.info("TUI: Quitting application...")
        self.state.lifecycle = Lifecycle.SHUTDOWN
        await asyncio.sleep(1) # Give some time for logs to appear
        self.exit()

if __name__ == "__main__":
    # This is a placeholder for running the TUI with a mock state.
    # In the actual application, the TUI will be launched with the real machine state.
    mock_state = MachineState()
    app = MachineTUI(mock_state)
    
    # Example of how to use the logger
    logging.info("TUI is starting up...")

    app.run()
