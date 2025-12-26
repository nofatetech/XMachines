# Core Python imports
import time
import json
import socket
import logging

# Textual imports
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log, Button, Label
from textual.containers import Container, Horizontal, Vertical
from textual.binding import Binding
from textual.logging import TextualHandler
from textual.message import Message
from textual_slider import Slider

import asyncio

# Local project imports
from state import MachineState
from lifecycle import Lifecycle

# Emojis for the UI
EMOJI_ROBOT = "🤖"
EMOJI_STATUS = "📡"
EMOJI_MODE = "🕹️"
EMOJI_CMD_TIME = "⏱️"
EMOJI_LINEAR = "💨"
EMOJI_ANGULAR = "🔄"
EMOJI_ACTIVE = "🟢"
EMOJI_IDLE = "🟡"
EMOJI_SHUTDOWN = "🔴"

class MachineStatus(Static):
    """A widget to display machine status."""
    def __init__(self, state: MachineState):
        super().__init__()
        self.state = state
        self.set_interval(0.1, self.update_status)

    def update_status(self) -> None:
        """Update the status display."""
        status_text = f"""
        [bold]{EMOJI_ROBOT} MACHINE ID:[/bold] {self.state.machine_id}
        [bold]{EMOJI_STATUS} LIFECYCLE:[/bold] {self.state.lifecycle.name}
        [bold]{EMOJI_MODE} MODE:[/bold] {self.state.mode}
        [bold]{EMOJI_CMD_TIME} LAST CMD:[/bold] {time.time() - self.state.last_command_ts:.2f}s ago
        """
        self.update(status_text)

class MotorControl(Static):
    """A widget for controlling the machine's motors."""
    class Changed(Message):
        """Posted when the slider value changes."""
        def __init__(self, linear: float, angular: float) -> None:
            self.linear = linear
            self.angular = angular
            super().__init__()

    def __init__(self) -> None:
        super().__init__()
        self.linear = 0.0
        self.angular = 0.0

    def compose(self) -> ComposeResult:
        yield Label("Motor Controls")
        yield Label(f"{EMOJI_LINEAR} Linear: {self.linear:.2f}", id="linear_label")
        yield Slider(min=-100, max=100, step=10, value=0, id="linear_slider")
        yield Label(f"{EMOJI_ANGULAR} Angular: {self.angular:.2f}", id="angular_label")
        yield Slider(min=-100, max=100, step=10, value=0, id="angular_slider")

    def on_slider_value_changed(self, event: Slider.Changed) -> None:
        if event.slider.id == "linear_slider":
            self.linear = event.value / 100.0
            self.query_one("#linear_label").update(f"{EMOJI_LINEAR} Linear: {self.linear:.2f}")
        elif event.slider.id == "angular_slider":
            self.angular = event.value / 100.0
            self.query_one("#angular_label").update(f"{EMOJI_ANGULAR} Angular: {self.angular:.2f}")
        self.post_message(self.Changed(self.linear, self.angular))


class LifecycleControl(Static):
    """A widget for controlling the machine's lifecycle."""
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Button(f"{EMOJI_ACTIVE} Activate", id="activate", variant="success")
            yield Button(f"{EMOJI_IDLE} Idle", id="idle", variant="warning")
            yield Button(f"{EMOJI_SHUTDOWN} Shutdown", id="shutdown", variant="error")


class MachineTUI(App):
    """A Textual TUI for monitoring and controlling the machine."""

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    DEFAULT_CSS = """
    Container {
        layout: vertical;
        height: 100%;
        width: 100%;
    }
    Horizontal {
        height: 1fr;
        width: 100%;
    }
    #left-pane {
        width: 40%;
        height: 100%;
    }
    #right-pane {
        width: 1fr;
        height: 100%;
    }
    Log {
        height: 100%;
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
        yield Header(name="X-Machine Control")
        with Container():
            with Horizontal():
                with Vertical(id="left-pane"):
                    yield MachineStatus(self.state)
                    yield MotorControl()
                    yield LifecycleControl()
                with Vertical(id="right-pane"):
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

    def on_motor_control_changed(self, message: MotorControl.Changed) -> None:
        """Called when the motor control values change."""
        self.send_drive_command(message.linear, message.angular)

    def send_drive_command(self, linear: float, angular: float) -> None:
        """Send a drive command to the machine."""
        command = {"linear": linear, "angular": angular}
        self.sock.sendto(json.dumps(command).encode(), self.target)


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "activate":
            self.state.lifecycle = Lifecycle.ACTIVE
        elif event.button.id == "idle":
            self.state.lifecycle = Lifecycle.IDLE
        elif event.button.id == "shutdown":
            self.state.lifecycle = Lifecycle.SHUTDOWN


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
    logging.warning("This is a test warning.")
    logging.debug("This is a test debug message.")
    logging.error("This is a test error message.")

    app.run()
