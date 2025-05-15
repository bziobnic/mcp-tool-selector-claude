# MCP Tool Selector - User Guide

## Introduction

MCP Tool Selector is a graphical application for managing MCP server tools stored in JSON configuration files. This guide will help you understand how to use the application effectively.

## Getting Started

### Installation

1. Clone the repository
2. Create a virtual environment: `uv venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install the package: `pip install -e .`

### Running the Application

Run the application using one of the following methods:

```bash
# Using the entry point script
python main.py

# Using the module
python -m mcp_tool_selector
```

## Using the Application

### Opening a Configuration File

When you start the application, you'll be prompted to:
- Open an existing configuration file
- Create a new configuration file
- Cancel and exit the application

If you choose to open an existing file, a file dialog will appear where you can select your JSON configuration file.

If you choose to create a new file, a file dialog will appear where you can specify the name and location of the new file.

### Main Interface

The application has two main tabs:

1. **Tool List**: Displays all available tools and their status
2. **Add Tool**: Allows you to add new tools by pasting JSON definitions

#### Tool List Tab

The Tool List tab displays all the tools in your configuration file. For each tool, you'll see:

- The tool name
- The current status (Enabled or Disabled)
- A button to enable or disable the tool
- A button to remove the tool
- Details about the tool's configuration (command, arguments, environment variables)

To enable or disable a tool, click the corresponding button. When you disable a tool, it will be backed up and removed from the main configuration file. When you enable a tool, it will be restored from the backup and added back to the configuration file.

#### Add Tool Tab

The Add Tool tab allows you to add new tools to your configuration file. To add a tool:

1. Paste a valid JSON definition in the text area
2. Click "Validate" to check if the JSON is valid
3. Click "Add Tool(s)" to add the tool(s) to your configuration

The JSON definition must follow this format:

```json
{
  "mcpServers": {
    "tool-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2", ...],
      "env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2"
      }
    }
  }
}
```

The `args` and `env` fields are optional.

### Menu Options

The application has the following menu options:

- **File**
  - **Open Config**: Open an existing configuration file
  - **New Config**: Create a new configuration file
  - **Exit**: Exit the application

- **Tools**
  - **Refresh**: Refresh the tool list from the configuration file

- **Help**
  - **About**: Show information about the application

## Configuration File Format

The configuration file is a JSON file with the following structure:

```json
{
  "mcpServers": {
    "tool-name-1": {
      "command": "command-to-run",
      "args": ["arg1", "arg2", ...],
      "env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2"
      }
    },
    "tool-name-2": {
      "command": "command-to-run",
      "args": ["arg1", "arg2", ...]
    }
  }
}
```

Each tool has the following properties:

- `command`: The command to run (required)
- `args`: An array of command-line arguments (optional)
- `env`: An object containing environment variables (optional)

## Backup File

When you disable a tool, it is backed up to a file with the same name as your configuration file but with a `.backup` extension. For example, if your configuration file is `config.json`, the backup file will be `config.json.backup`.

The backup file has the same structure as the configuration file and contains all the disabled tools.

## Troubleshooting

### Common Issues

1. **Invalid JSON**: If you get an error when adding a tool, check that your JSON is valid and follows the required format.

2. **File Permissions**: If you get an error when saving the configuration file, check that you have write permissions for the file and its directory.

3. **Missing Tools**: If tools are missing from the list, try clicking the "Refresh" button in the Tools menu.

### Error Messages

The application will display error messages when something goes wrong. These messages will help you understand what the problem is and how to fix it.

## Conclusion

MCP Tool Selector provides a simple and intuitive way to manage your MCP server tools. If you have any questions or issues, please refer to the documentation or contact the developers.
