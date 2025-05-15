"""Main application entry point for the MCP Tool Selector.

This module initializes the application and connects the UI components.
"""

import logging
import sys
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import UI components
try:
    from .ui.main_window import MainWindow
except ImportError as e:
    logger.error(f"Failed to import UI components: {e}")
    sys.exit(1)


def main() -> None:
    """Run the MCP Tool Selector application."""
    try:
        # Create and run the main window
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
