"""Tool editor frame for the MCP Tool Selector.

This module implements the UI component for adding new tools.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from ..tool_manager import ToolManager


class ToolEditorFrame(ttk.Frame):
    """Frame for adding new tools."""

    def __init__(self, parent: ttk.Frame, tool_manager: ToolManager, on_add_callback: Callable[[], None]):
        """Initialize the tool editor frame.

        Args:
            parent: The parent frame
            tool_manager: The tool manager to use
            on_add_callback: Callback to call when a tool is added
        """
        super().__init__(parent)
        self.tool_manager = tool_manager
        self.on_add_callback = on_add_callback

        # Create the widgets
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create the widgets for the tool editor frame."""
        # Create a frame for the header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        # Add a title label
        title_label = ttk.Label(header_frame, text="Add New Tool", font=("TkDefaultFont", 12, "bold"))
        title_label.pack(side=tk.LEFT, pady=5)

        # Create a separator
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=5)

        # Add instructions
        instructions_frame = ttk.Frame(self)
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)

        instructions_label = ttk.Label(
            instructions_frame,
            text="Paste a JSON definition for one or more MCP server tools below.",
            wraplength=600,
            justify=tk.LEFT
        )
        instructions_label.pack(anchor=tk.W)

        example_label = ttk.Label(
            instructions_frame,
            text="Example:\n"
                 "{\n"
                 "  \"mcpServers\": {\n"
                 "    \"tool-name\": {\n"
                 "      \"command\": \"npx\",\n"
                 "      \"args\": [\"-y\", \"@example/tool\"]\n"
                 "    }\n"
                 "  }\n"
                 "}",
            font=("Courier", 9),
            justify=tk.LEFT
        )
        example_label.pack(anchor=tk.W, pady=(5, 10))

        # Add the text area for JSON input
        self.json_text = tk.Text(self, height=15, width=80, wrap=tk.NONE)
        self.json_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Add a scrollbar for the text area
        scrollbar_y = ttk.Scrollbar(self.json_text, orient=tk.VERTICAL, command=self.json_text.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.json_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.json_text.xview)
        scrollbar_x.pack(fill=tk.X, padx=10)
        self.json_text.configure(xscrollcommand=scrollbar_x.set)

        # Add the buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        validate_button = ttk.Button(button_frame, text="Validate", command=self._validate_json)
        validate_button.pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(button_frame, text="Add Tool(s)", command=self._add_tools)
        add_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_text)
        clear_button.pack(side=tk.LEFT, padx=5)

    def _validate_json(self) -> None:
        """Validate the JSON input."""
        json_str = self.json_text.get("1.0", tk.END).strip()
        if not json_str:
            messagebox.showwarning("Validation", "Please enter JSON content.")
            return

        valid, _, error = self.tool_manager.config_manager.validate_json_string(json_str)
        if valid:
            messagebox.showinfo("Validation", "JSON is valid.")
        else:
            messagebox.showerror("Validation Error", error or "Invalid JSON format.")

    def _add_tools(self) -> None:
        """Add tools from the JSON input."""
        json_str = self.json_text.get("1.0", tk.END).strip()
        if not json_str:
            messagebox.showwarning("Add Tools", "Please enter JSON content.")
            return

        # Validate and add the tools
        success, error, added_tools = self.tool_manager.add_tools_from_json(json_str)

        if success and added_tools:
            messagebox.showinfo(
                "Success",
                f"Added {len(added_tools)} tool(s):\n{', '.join(added_tools)}"
            )
            self._clear_text()
            if self.on_add_callback:
                self.on_add_callback()
        else:
            messagebox.showerror("Error", error or "Failed to add tools.")

    def _clear_text(self) -> None:
        """Clear the text area."""
        self.json_text.delete("1.0", tk.END)
