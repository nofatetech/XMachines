import logging
import sys
from logging import StreamHandler

def setup_logging():
    """
    Configures the root logger's level. Handlers are expected to be managed
    by the application (e.g., Textual's TextualHandler).
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)


