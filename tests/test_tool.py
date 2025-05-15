"""Tests for the tool manager."""

import json
import os
import tempfile
import pytest
from pathlib import Path

from mcp_tool_selector.config_manager import ConfigManager
from mcp_tool_selector.tool_manager import ToolManager, Tool


class TestToolManager:
    """Test cases for the ToolManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "config.json")
        self.backup_path = os.path.join(self.temp_dir.name, "config.json.backup")
        
        # Create a test configuration
        self.test_config = {
            "mcpServers": {
                "test-tool-1": {
                    "command": "npx",
                    "args": ["-y", "@test/tool-1"]
                },
                "test-tool-2": {
                    "command": "npx",
                    "args": ["-y", "@test/tool-2"],
                    "env": {
                        "TEST_VAR": "test-value"
                    }
                }
            }
        }
        
        # Write the test configuration to the file
        with open(self.config_path, "w") as f:
            json.dump(self.test_config, f)
        
        # Create the config manager and tool manager
        self.config_manager = ConfigManager(self.config_path)
        self.tool_manager = ToolManager(self.config_manager)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_load_tools(self):
        """Test loading tools from configuration."""
        # Tools should be loaded in the constructor
        tools = self.tool_manager.get_tools()
        
        assert len(tools) == 2
        assert any(tool.name == "test-tool-1" for tool in tools)
        assert any(tool.name == "test-tool-2" for tool in tools)
    
    def test_get_tool(self):
        """Test getting a tool by name."""
        tool = self.tool_manager.get_tool("test-tool-1")
        
        assert tool is not None
        assert tool.name == "test-tool-1"
        assert tool.config["command"] == "npx"
        assert tool.config["args"] == ["-y", "@test/tool-1"]
        
        # Test getting a non-existent tool
        tool = self.tool_manager.get_tool("non-existent-tool")
        assert tool is None
    
    def test_add_tool(self):
        """Test adding a new tool."""
        tool_name = "new-tool"
        tool_config = {
            "command": "npx",
            "args": ["-y", "@new/tool"]
        }
        
        # Add the tool
        success = self.tool_manager.add_tool(tool_name, tool_config)
        
        assert success
        
        # Check if the tool was added
        tool = self.tool_manager.get_tool(tool_name)
        assert tool is not None
        assert tool.name == tool_name
        assert tool.config == tool_config
        
        # Check if the tool was saved to the configuration file
        config = self.config_manager.read_config()
        assert tool_name in config["mcpServers"]
        assert config["mcpServers"][tool_name] == tool_config
    
    def test_update_tool(self):
        """Test updating an existing tool."""
        tool_name = "test-tool-1"
        updated_config = {
            "command": "npx",
            "args": ["-y", "@updated/tool"]
        }
        
        # Update the tool
        success = self.tool_manager.update_tool(tool_name, updated_config)
        
        assert success
        
        # Check if the tool was updated
        tool = self.tool_manager.get_tool(tool_name)
        assert tool is not None
        assert tool.config == updated_config
        
        # Check if the tool was saved to the configuration file
        config = self.config_manager.read_config()
        assert config["mcpServers"][tool_name] == updated_config
    
    def test_enable_disable_tool(self):
        """Test enabling and disabling a tool."""
        tool_name = "test-tool-1"
        
        # Disable the tool
        success = self.tool_manager.disable_tool(tool_name)
        
        assert success
        
        # Check if the tool was disabled
        tool = self.tool_manager.get_tool(tool_name)
        assert tool is not None
        assert not tool.enabled
        
        # Check if the tool was removed from the configuration file
        config = self.config_manager.read_config()
        assert tool_name not in config["mcpServers"]
        
        # Check if the tool was backed up
        backup = self.config_manager.read_backup()
        assert tool_name in backup["mcpServers"]
        
        # Enable the tool
        success = self.tool_manager.enable_tool(tool_name)
        
        assert success
        
        # Check if the tool was enabled
        tool = self.tool_manager.get_tool(tool_name)
        assert tool is not None
        assert tool.enabled
        
        # Check if the tool was added back to the configuration file
        config = self.config_manager.read_config()
        assert tool_name in config["mcpServers"]
        
        # Check if the tool was removed from the backup
        backup = self.config_manager.read_backup()
        assert tool_name not in backup["mcpServers"]
    
    def test_remove_tool(self):
        """Test removing a tool."""
        tool_name = "test-tool-1"
        
        # Remove the tool
        success = self.tool_manager.remove_tool(tool_name)
        
        assert success
        
        # Check if the tool was removed
        tool = self.tool_manager.get_tool(tool_name)
        assert tool is None
        
        # Check if the tool was removed from the configuration file
        config = self.config_manager.read_config()
        assert tool_name not in config["mcpServers"]
        
        # Check if the tool was backed up
        backup = self.config_manager.read_backup()
        assert tool_name in backup["mcpServers"]
    
    def test_add_tools_from_json(self):
        """Test adding tools from a JSON string."""
        json_str = json.dumps({
            "mcpServers": {
                "json-tool-1": {
                    "command": "npx",
                    "args": ["-y", "@json/tool-1"]
                },
                "json-tool-2": {
                    "command": "npx",
                    "args": ["-y", "@json/tool-2"]
                }
            }
        })
        
        # Add the tools
        success, error, added_tools = self.tool_manager.add_tools_from_json(json_str)
        
        assert success
        assert error is None
        assert len(added_tools) == 2
        assert "json-tool-1" in added_tools
        assert "json-tool-2" in added_tools
        
        # Check if the tools were added
        tool1 = self.tool_manager.get_tool("json-tool-1")
        tool2 = self.tool_manager.get_tool("json-tool-2")
        
        assert tool1 is not None
        assert tool2 is not None
        
        # Check if the tools were saved to the configuration file
        config = self.config_manager.read_config()
        assert "json-tool-1" in config["mcpServers"]
        assert "json-tool-2" in config["mcpServers"]
    
    def test_add_tools_from_invalid_json(self):
        """Test adding tools from an invalid JSON string."""
        # Invalid JSON syntax
        json_str = "{\"mcpServers\": {\"test-tool\": {\"command\": \"npx\",}"
        
        success, error, added_tools = self.tool_manager.add_tools_from_json(json_str)
        
        assert not success
        assert error is not None
        assert len(added_tools) == 0
