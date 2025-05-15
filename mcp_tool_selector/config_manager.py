"""Configuration manager for MCP Tool Selector.

This module handles reading and writing JSON configuration files,
creating backups of disabled tools, and restoring tools from backups.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages the MCP server tool configuration files."""

    def __init__(self, config_path: str, backup_path: Optional[str] = None):
        """Initialize the configuration manager.

        Args:
            config_path: Path to the main configuration file
            backup_path: Path to the backup file for disabled tools
                         (defaults to config_path + '.backup')
        """
        self.config_path = config_path
        self.backup_path = backup_path or f"{config_path}.backup"
        
    def read_config(self) -> Dict[str, Any]:
        """Read the configuration file.

        Returns:
            The configuration as a dictionary
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            json.JSONDecodeError: If the configuration file contains invalid JSON
        """
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"Configuration file not found: {self.config_path}")
                return {"mcpServers": {}}
                
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            # Ensure the config has the expected structure
            if "mcpServers" not in config:
                config["mcpServers"] = {}
                
            return config
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading configuration file: {e}")
            raise
    
    def write_config(self, config: Dict[str, Any]) -> None:
        """Write the configuration to the file.

        Args:
            config: The configuration dictionary to write
            
        Raises:
            PermissionError: If the file cannot be written due to permissions
            OSError: If there's an error writing the file
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            logger.info(f"Configuration written to {self.config_path}")
        except (PermissionError, OSError) as e:
            logger.error(f"Error writing configuration file: {e}")
            raise
    
    def read_backup(self) -> Dict[str, Any]:
        """Read the backup file for disabled tools.

        Returns:
            The backup configuration as a dictionary
        """
        try:
            if not os.path.exists(self.backup_path):
                logger.info(f"Backup file not found: {self.backup_path}")
                return {"mcpServers": {}}
                
            with open(self.backup_path, 'r') as f:
                backup = json.load(f)
                
            # Ensure the backup has the expected structure
            if "mcpServers" not in backup:
                backup["mcpServers"] = {}
                
            return backup
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in backup file: {e}")
            return {"mcpServers": {}}
        except Exception as e:
            logger.warning(f"Error reading backup file: {e}")
            return {"mcpServers": {}}
    
    def write_backup(self, backup: Dict[str, Any]) -> None:
        """Write the backup configuration to the file.

        Args:
            backup: The backup configuration dictionary to write
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(self.backup_path)), exist_ok=True)
            
            with open(self.backup_path, 'w') as f:
                json.dump(backup, f, indent=2)
                
            logger.info(f"Backup written to {self.backup_path}")
        except Exception as e:
            logger.error(f"Error writing backup file: {e}")
            # We don't raise here to avoid disrupting the main functionality
    
    def backup_tool(self, tool_name: str, tool_config: Dict[str, Any]) -> None:
        """Backup a disabled tool.

        Args:
            tool_name: Name of the tool to backup
            tool_config: Configuration of the tool to backup
        """
        backup = self.read_backup()
        backup["mcpServers"][tool_name] = tool_config
        self.write_backup(backup)
        logger.info(f"Tool '{tool_name}' backed up")
    
    def restore_tool(self, tool_name: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Restore a tool from backup.

        Args:
            tool_name: Name of the tool to restore
            
        Returns:
            A tuple containing:
            - Boolean indicating success
            - The tool configuration if successful, None otherwise
        """
        backup = self.read_backup()
        
        if tool_name not in backup.get("mcpServers", {}):
            logger.warning(f"Tool '{tool_name}' not found in backup")
            return False, None
        
        tool_config = backup["mcpServers"][tool_name]
        
        # Remove from backup
        del backup["mcpServers"][tool_name]
        self.write_backup(backup)
        
        logger.info(f"Tool '{tool_name}' restored from backup")
        return True, tool_config
    
    def validate_json_string(self, json_str: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """Validate a JSON string containing tool definitions.

        Args:
            json_str: The JSON string to validate
            
        Returns:
            A tuple containing:
            - Boolean indicating if the JSON is valid
            - The parsed JSON if valid, None otherwise
            - Error message if invalid, None otherwise
        """
        try:
            config = json.loads(json_str)
            
            # Check if the JSON has the expected structure
            if "mcpServers" not in config:
                return False, None, "JSON must contain an 'mcpServers' object"
                
            if not isinstance(config["mcpServers"], dict):
                return False, None, "'mcpServers' must be an object"
                
            # Validate each tool
            for tool_name, tool_config in config["mcpServers"].items():
                if not isinstance(tool_config, dict):
                    return False, None, f"Tool '{tool_name}' configuration must be an object"
                    
                if "command" not in tool_config:
                    return False, None, f"Tool '{tool_name}' must have a 'command' property"
                    
                if not isinstance(tool_config["command"], str):
                    return False, None, f"Tool '{tool_name}' 'command' must be a string"
                    
                if "args" in tool_config and not isinstance(tool_config["args"], list):
                    return False, None, f"Tool '{tool_name}' 'args' must be an array"
                    
                if "env" in tool_config and not isinstance(tool_config["env"], dict):
                    return False, None, f"Tool '{tool_name}' 'env' must be an object"
            
            return True, config, None
        except json.JSONDecodeError as e:
            return False, None, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, None, f"Error validating JSON: {str(e)}"
