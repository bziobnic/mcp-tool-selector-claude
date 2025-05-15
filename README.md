# MCP Tool Selector

A graphical tool for enabling and disabling MCP server tools stored in a JSON configuration file.

## Project Overview

This application allows users to:

- View all available MCP server tools in a configuration file
- Enable or disable individual tools
- Add new tools by pasting JSON definitions
- Maintain a backup of disabled tools
- Visually distinguish between active and disabled tools

## Technical Requirements

- Python 3.8+
- Cross-platform compatibility (Windows, macOS, Linux)
- GUI framework: Tkinter (built into Python standard library)
- JSON parsing and manipulation

## Project Structure

```
mcp-tool-selector/
├── README.md                # Project documentation
├── TODO.md                 # Implementation plan
├── AI-SPECIFIC.md          # AI-specific notes
├── requirements.txt        # Python dependencies
├── mcp_tool_selector/
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Main application entry point
│   ├── config_manager.py   # JSON configuration file management
│   ├── tool_manager.py     # Tool enabling/disabling logic
│   └── ui/
│       ├── __init__.py     # UI package initialization
│       ├── main_window.py  # Main application window
│       ├── tool_list.py    # Tool listing and status display
│       └── tool_editor.py  # Tool addition interface
└── tests/
    ├── __init__.py         # Test package initialization
    ├── test_config.py      # Configuration manager tests
    └── test_tool.py        # Tool manager tests
```

## Implementation Plan

See [TODO.md](TODO.md) for the detailed implementation plan.

## Features

1. **Tool Listing**: Display all tools with their status (enabled/disabled)
2. **Tool Management**: Enable or disable tools with a simple toggle
3. **Tool Addition**: Add new tools by pasting JSON definitions
4. **Configuration Backup**: Automatically backup disabled tools
5. **Visual Indicators**: Clear visual distinction between active and disabled tools

## Usage

1. Run the application: `python -m mcp_tool_selector`
2. View the list of available tools
3. Toggle tools on/off as needed
4. Add new tools by pasting JSON definitions in the provided interface
5. Changes are automatically saved to the configuration file

## Development

1. Clone the repository
2. Create a virtual environment: `uv venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `uv pip install -r requirements.txt`
5. Run tests: `pytest`

## License

MIT

## Version

0.1.0
