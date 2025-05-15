"""Tool list frame for the MCP Tool Selector.

This module implements the UI component for displaying and managing tools.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any, Optional

from ..tool_manager import ToolManager, Tool


class ToolListFrame(ttk.Frame):
    """Frame for displaying and managing tools."""

    def __init__(self, parent: ttk.Frame, tool_manager: ToolManager, on_change_callback: Callable[[], None]):
        """Initialize the tool list frame.

        Args:
            parent: The parent frame
            tool_manager: The tool manager to use
            on_change_callback: Callback to call when a tool is changed
        """
        super().__init__(parent)
        self.tool_manager = tool_manager
        self.on_change_callback = on_change_callback
        self.tool_frames: Dict[str, ttk.Frame] = {}

        # Create the main layout
        self._create_widgets()
        self.refresh()

    def _create_widgets(self) -> None:
        """Create the widgets for the tool list frame."""
        # Create a frame for the header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        # Add a title label
        title_label = ttk.Label(header_frame, text="MCP Server Tools", font=("TkDefaultFont", 12, "bold"))
        title_label.pack(side=tk.LEFT, pady=5)

        # Add a refresh button
        refresh_button = ttk.Button(header_frame, text="Refresh", command=self.refresh)
        refresh_button.pack(side=tk.RIGHT, padx=5)

        # Create a separator
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=5)

        # Create a canvas with scrollbar for the tool list
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event: tk.Event) -> None:
        """Handle mouse wheel scrolling.

        Args:
            event: The mouse wheel event
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def refresh(self) -> None:
        """Refresh the tool list."""
        # Clear existing tool frames
        for frame in self.tool_frames.values():
            frame.destroy()
        self.tool_frames = {}

        # Get the list of tools
        tools = self.tool_manager.get_tools()

        if not tools:
            # Display a message if no tools are available
            no_tools_frame = ttk.Frame(self.scrollable_frame)
            no_tools_frame.pack(fill=tk.X, padx=10, pady=5)

            no_tools_label = ttk.Label(
                no_tools_frame,
                text="No tools available. Add tools using the 'Add Tool' tab.",
                foreground="gray"
            )
            no_tools_label.pack(pady=20)

            return

        # Add each tool to the list
        for tool in tools:
            self._add_tool_to_list(tool)

    def _add_tool_to_list(self, tool: Tool) -> None:
        """Add a tool to the list.

        Args:
            tool: The tool to add
        """
        # Create a frame for the tool
        tool_frame = ttk.Frame(self.scrollable_frame)
        tool_frame.pack(fill=tk.X, padx=10, pady=5)

        # Add a border around the frame
        tool_frame.configure(style="Tool.TFrame")
        style = ttk.Style()
        style.configure("Tool.TFrame", relief=tk.GROOVE, borderwidth=1)

        # Create a style for enabled/disabled tools
        style.configure("Enabled.TLabel", foreground="green")
        style.configure("Disabled.TLabel", foreground="red")

        # Add the tool name
        name_label = ttk.Label(tool_frame, text=tool.name, font=("TkDefaultFont", 10, "bold"))
        name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # Add the tool status
        status_text = "Enabled" if tool.enabled else "Disabled"
        status_style = "Enabled.TLabel" if tool.enabled else "Disabled.TLabel"
        status_label = ttk.Label(tool_frame, text=status_text, style=status_style)
        status_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Add the toggle button
        toggle_text = "Disable" if tool.enabled else "Enable"
        toggle_button = ttk.Button(
            tool_frame,
            text=toggle_text,
            command=lambda t=tool: self._toggle_tool(t)
        )
        toggle_button.grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)

        # Add the remove button
        remove_button = ttk.Button(
            tool_frame,
            text="Remove",
            command=lambda t=tool: self._remove_tool(t)
        )
        remove_button.grid(row=0, column=3, sticky=tk.E, padx=5, pady=5)

        # Add the tool details
        details_frame = ttk.Frame(tool_frame)
        details_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)

        # Add the command
        command_label = ttk.Label(details_frame, text=f"Command: {tool.config.get('command', '')}")
        command_label.pack(anchor=tk.W)

        # Add the arguments if available
        args = tool.config.get('args', [])
        if args:
            args_str = " ".join(str(arg) for arg in args)
            args_label = ttk.Label(details_frame, text=f"Args: {args_str}")
            args_label.pack(anchor=tk.W)

        # Add the environment variables if available
        env = tool.config.get('env', {})
        if env:
            env_frame = ttk.Frame(details_frame)
            env_frame.pack(anchor=tk.W, fill=tk.X, pady=(5, 0))

            env_label = ttk.Label(env_frame, text="Environment Variables:")
            env_label.pack(anchor=tk.W)

            for key, value in env.items():
                env_var_label = ttk.Label(env_frame, text=f"  {key}: {value}")
                env_var_label.pack(anchor=tk.W)

        # Store the frame for later reference
        self.tool_frames[tool.name] = tool_frame

    def _toggle_tool(self, tool: Tool) -> None:
        """Toggle a tool's enabled status.

        Args:
            tool: The tool to toggle
        """
        try:
            if tool.enabled:
                self.tool_manager.disable_tool(tool.name)
            else:
                self.tool_manager.enable_tool(tool.name)

            # Refresh the list
            self.refresh()

            # Call the change callback
            if self.on_change_callback:
                self.on_change_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle tool: {str(e)}")

    def _remove_tool(self, tool: Tool) -> None:
        """Remove a tool.

        Args:
            tool: The tool to remove
        """
        # Confirm removal
        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove the tool '{tool.name}'?"
        )

        if not confirm:
            return

        try:
            self.tool_manager.remove_tool(tool.name)

            # Refresh the list
            self.refresh()

            # Call the change callback
            if self.on_change_callback:
                self.on_change_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove tool: {str(e)}")
