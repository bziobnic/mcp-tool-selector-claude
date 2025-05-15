#!/usr/bin/env python
"""Main entry point for the MCP Tool Selector application.

This script allows the application to be run directly from the command line.
"""

import sys
import os

# Add the parent directory to the path to allow importing the package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from mcp_tool_selector.app import main

if __name__ == "__main__":
    main()
