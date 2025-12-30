from abc import ABC, abstractmethod
import threading
import logging

class AbstractService(ABC):
    """
    Abstract base class for all background services (e.g., API server, heartbeat sender).
    Services typically run in their own threads and handle non-realtime operations.
    """
    def __init__(self, state):
        self.state = state
        self.log = logging.getLogger(self.__class__.__name__)
        self._thread = None
        self._running = False

    @abstractmethod
    def _run(self):
        """Implement the main logic of the service here."""
        pass

    def start(self):
        """
        Starts the service in a new background thread.
        """
        if not self._running:
            self.log.info(f"Starting service {self.__class__.__name__}")
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        else:
            self.log.warning(f"Service {self.__class__.__name__} is already running.")

    def stop(self):
        """
        Stops the service.
        """
        if self._running:
            self.log.info(f"Stopping service {self.__class__.__name__}")
            self._running = False
            if self._thread and self._thread.is_alive():
                # Give the thread a moment to shut down gracefully
                self._thread.join(timeout=1.0)
            self.log.info(f"Service {self.__class__.__name__} stopped.")
        else:
            self.log.warning(f"Service {self.__class__.__name__} is not running.")

    def is_running(self):
        """
        Checks if the service is currently running.
        """
        return self._running and self._thread and self._thread.is_alive()
