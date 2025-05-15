"""Tests for the configuration manager."""

import json
import os
import tempfile
import pytest
from pathlib import Path

from mcp_tool_selector.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for the ConfigManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "config.json")
        self.backup_path = os.path.join(self.temp_dir.name, "config.json.backup")
        
        # Create a test configuration
        self.test_config = {
            "mcpServers": {
                "test-tool": {
                    "command": "npx",
                    "args": ["-y", "@test/tool"]
                }
            }
        }
        
        # Write the test configuration to the file
        with open(self.config_path, "w") as f:
            json.dump(self.test_config, f)
        
        # Create the config manager
        self.config_manager = ConfigManager(self.config_path)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_read_config(self):
        """Test reading a configuration file."""
        config = self.config_manager.read_config()
        assert config == self.test_config
        assert "mcpServers" in config
        assert "test-tool" in config["mcpServers"]
    
    def test_read_nonexistent_config(self):
        """Test reading a non-existent configuration file."""
        # Create a config manager with a non-existent file
        nonexistent_path = os.path.join(self.temp_dir.name, "nonexistent.json")
        config_manager = ConfigManager(nonexistent_path)
        
        # Reading should return an empty config
        config = config_manager.read_config()
        assert config == {"mcpServers": {}}
    
    def test_write_config(self):
        """Test writing a configuration file."""
        # Modify the configuration
        modified_config = {
            "mcpServers": {
                "test-tool": {
                    "command": "npx",
                    "args": ["-y", "@modified/tool"]
                }
            }
        }
        
        # Write the modified configuration
        self.config_manager.write_config(modified_config)
        
        # Read the configuration back
        with open(self.config_path, "r") as f:
            config = json.load(f)
        
        assert config == modified_config
    
    def test_backup_tool(self):
        """Test backing up a tool."""
        tool_name = "test-tool"
        tool_config = self.test_config["mcpServers"][tool_name]
        
        # Backup the tool
        self.config_manager.backup_tool(tool_name, tool_config)
        
        # Check if the backup file exists
        assert os.path.exists(self.backup_path)
        
        # Read the backup file
        with open(self.backup_path, "r") as f:
            backup = json.load(f)
        
        assert "mcpServers" in backup
        assert tool_name in backup["mcpServers"]
        assert backup["mcpServers"][tool_name] == tool_config
    
    def test_restore_tool(self):
        """Test restoring a tool from backup."""
        tool_name = "test-tool"
        tool_config = self.test_config["mcpServers"][tool_name]
        
        # Backup the tool
        self.config_manager.backup_tool(tool_name, tool_config)
        
        # Restore the tool
        success, restored_config = self.config_manager.restore_tool(tool_name)
        
        assert success
        assert restored_config == tool_config
        
        # Check if the tool was removed from the backup
        backup = self.config_manager.read_backup()
        assert tool_name not in backup["mcpServers"]
    
    def test_validate_json_string_valid(self):
        """Test validating a valid JSON string."""
        json_str = json.dumps(self.test_config)
        valid, config, error = self.config_manager.validate_json_string(json_str)
        
        assert valid
        assert config == self.test_config
        assert error is None
    
    def test_validate_json_string_invalid(self):
        """Test validating an invalid JSON string."""
        # Invalid JSON syntax
        json_str = "{\"mcpServers\": {\"test-tool\": {\"command\": \"npx\",}"
        valid, config, error = self.config_manager.validate_json_string(json_str)
        
        assert not valid
        assert config is None
        assert error is not None
        
        # Missing required fields
        json_str = '{"mcpServers": {"test-tool": {"args": ["-y", "@test/tool"]}}}'  # Missing command
        valid, config, error = self.config_manager.validate_json_string(json_str)
        
        assert not valid
        assert config is None
        assert error is not None
