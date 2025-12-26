import logging
import sys
from logging import StreamHandler

import logging
import sys
from logging import StreamHandler

def setup_logging():
    """
    Configures the root logger to redirect standard print statements
    and integrate with Textual's logging system.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create a stream handler to output to stderr (which Textual can capture)
    # Textual's log widget will typically capture stderr.
    handler = StreamHandler(sys.stderr)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add the handler to the root logger
    root_logger.addHandler(handler)

    print("Logging configured.")

