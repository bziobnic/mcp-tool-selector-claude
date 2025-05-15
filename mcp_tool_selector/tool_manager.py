"""Tool manager for MCP Tool Selector.

This module handles the management of MCP server tools,
including enabling, disabling, and adding new tools.
"""

import logging
from typing import Dict, Any, List, Tuple, Optional
from .config_manager import ConfigManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Tool:
    """Represents an MCP server tool."""

    def __init__(self, name: str, config: Dict[str, Any], enabled: bool = True):
        """Initialize a tool.

        Args:
            name: The name of the tool
            config: The tool's configuration
            enabled: Whether the tool is enabled
        """
        self.name = name
        self.config = config
        self.enabled = enabled

    def __repr__(self) -> str:
        """Return a string representation of the tool."""
        return f"Tool(name={self.name}, enabled={self.enabled})"


class ToolManager:
    """Manages MCP server tools."""

    def __init__(self, config_manager: ConfigManager):
        """Initialize the tool manager.

        Args:
            config_manager: The configuration manager to use
        """
        self.config_manager = config_manager
        self.tools: Dict[str, Tool] = {}
        self.load_tools()

    def load_tools(self) -> None:
        """Load tools from the configuration file."""
        try:
            config = self.config_manager.read_config()
            for tool_name, tool_config in config.get("mcpServers", {}).items():
                self.tools[tool_name] = Tool(tool_name, tool_config)
            logger.info(f"Loaded {len(self.tools)} tools from configuration")
        except Exception as e:
            logger.error(f"Error loading tools: {e}")
            # Initialize with empty tools dictionary
            self.tools = {}

    def get_tools(self) -> List[Tool]:
        """Get all tools.

        Returns:
            A list of all tools
        """
        return list(self.tools.values())

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name.

        Args:
            name: The name of the tool to get

        Returns:
            The tool if found, None otherwise
        """
        return self.tools.get(name)

    def add_tool(self, name: str, config: Dict[str, Any]) -> bool:
        """Add a new tool.

        Args:
            name: The name of the tool to add
            config: The tool's configuration

        Returns:
            True if the tool was added, False otherwise
        """
        if name in self.tools:
            logger.warning(f"Tool '{name}' already exists")
            return False

        self.tools[name] = Tool(name, config)
        self._save_config()
        logger.info(f"Added tool '{name}'")
        return True

    def update_tool(self, name: str, config: Dict[str, Any]) -> bool:
        """Update an existing tool.

        Args:
            name: The name of the tool to update
            config: The new tool configuration

        Returns:
            True if the tool was updated, False otherwise
        """
        if name not in self.tools:
            logger.warning(f"Tool '{name}' does not exist")
            return False

        self.tools[name].config = config
        self._save_config()
        logger.info(f"Updated tool '{name}'")
        return True

    def enable_tool(self, name: str) -> bool:
        """Enable a tool.

        Args:
            name: The name of the tool to enable

        Returns:
            True if the tool was enabled, False otherwise
        """
        if name not in self.tools:
            logger.warning(f"Tool '{name}' does not exist")
            return False

        # Check if the tool is already enabled
        if self.tools[name].enabled:
            logger.info(f"Tool '{name}' is already enabled")
            return True

        # Restore from backup if needed
        success, tool_config = self.config_manager.restore_tool(name)
        if success and tool_config:
            self.tools[name].config = tool_config

        self.tools[name].enabled = True
        self._save_config()
        logger.info(f"Enabled tool '{name}'")
        return True

    def disable_tool(self, name: str) -> bool:
        """Disable a tool.

        Args:
            name: The name of the tool to disable

        Returns:
            True if the tool was disabled, False otherwise
        """
        if name not in self.tools:
            logger.warning(f"Tool '{name}' does not exist")
            return False

        # Check if the tool is already disabled
        if not self.tools[name].enabled:
            logger.info(f"Tool '{name}' is already disabled")
            return True

        # Backup the tool configuration
        self.config_manager.backup_tool(name, self.tools[name].config)

        self.tools[name].enabled = False
        self._save_config()
        logger.info(f"Disabled tool '{name}'")
        return True

    def remove_tool(self, name: str) -> bool:
        """Remove a tool.

        Args:
            name: The name of the tool to remove

        Returns:
            True if the tool was removed, False otherwise
        """
        if name not in self.tools:
            logger.warning(f"Tool '{name}' does not exist")
            return False

        # Backup the tool configuration if it's enabled
        if self.tools[name].enabled:
            self.config_manager.backup_tool(name, self.tools[name].config)

        del self.tools[name]
        self._save_config()
        logger.info(f"Removed tool '{name}'")
        return True

    def add_tools_from_json(self, json_str: str) -> Tuple[bool, Optional[str], List[str]]:
        """Add tools from a JSON string.

        Args:
            json_str: The JSON string containing tool definitions

        Returns:
            A tuple containing:
            - Boolean indicating success
            - Error message if unsuccessful, None otherwise
            - List of tool names that were added
        """
        # Validate the JSON string
        valid, config, error = self.config_manager.validate_json_string(json_str)
        if not valid or config is None:
            return False, error, []

        # Add each tool
        added_tools = []
        for tool_name, tool_config in config.get("mcpServers", {}).items():
            if self.add_tool(tool_name, tool_config):
                added_tools.append(tool_name)

        if added_tools:
            logger.info(f"Added {len(added_tools)} tools from JSON")
            return True, None, added_tools
        else:
            return False, "No tools were added", []

    def _save_config(self) -> None:
        """Save the current tool configuration."""
        config = {"mcpServers": {}}
        for name, tool in self.tools.items():
            if tool.enabled:  # Only include enabled tools in the main config
                config["mcpServers"][name] = tool.config

        try:
            self.config_manager.write_config(config)
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
