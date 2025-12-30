from abc import ABC, abstractmethod
import logging

class AbstractNode(ABC):
    """
    Abstract base class for all machine nodes (e.g., motor controllers, arm controllers, sensors).
    Nodes are responsible for interacting with hardware or simulated components.
    """
    def __init__(self, state):
        self.state = state
        self.log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def start(self):
        """Initializes and starts the node. Implement specific setup logic here."""
        pass

    @abstractmethod
    def stop(self):
        """Stops and cleans up the node. Implement specific shutdown logic here."""
        pass

    @abstractmethod
    def update(self):
        """
        Performs periodic updates for the node. This method should be fast and non-blocking.
        It's called repeatedly in the main control loop.
        """
        pass
