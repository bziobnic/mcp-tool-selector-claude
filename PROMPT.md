  
I want a simple, graphical tool for enabling / disabling tools that are stored in a json file. The file has this basic format: 

{
  "mcpServers": {
    "mcp_server_1": {
      "command": "npx",
      "args": [
        "-y",
        "@user96/mcp-server-1"
      ]
    },
    "mcp_server_2": {
      "command": "npx",
      "args": [
        "-y",
        "@user99/mcp-server-2"
      ],
    }
  }
}


The program should allow the user to paste in an MCP server definition like this: 

{
  "mcpServers": {
    "mcp_server_3": {
      "command": "uvx",
      "args": [
        "@user01/mcp-server-3"
      ]
    }
  }
}


and the program will handle extracting the "windows-cli" tool from the list and updating the existing config file. If the user disables a tool, the program should create or amend a backup file for disabled tools. disabled tools should be displayed in a disabled state, while active tools should be displayed in an active state. The tools should use cross-platform Python code. Please create a step-by-step project plan and save it as README.md