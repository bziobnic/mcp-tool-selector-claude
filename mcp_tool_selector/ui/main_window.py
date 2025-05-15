"""Main window for the MCP Tool Selector.

This module implements the main application window and UI framework.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable

from ..config_manager import ConfigManager
from ..tool_manager import ToolManager
from .tool_list import ToolListFrame
from .tool_editor import ToolEditorFrame


class MainWindow(tk.Tk):
    """Main application window for the MCP Tool Selector."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        self.title("MCP Tool Selector")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Set icon if available
        # self.iconbitmap("path/to/icon.ico")

        # Initialize variables
        self.config_path: Optional[str] = None
        self.config_manager: Optional[ConfigManager] = None
        self.tool_manager: Optional[ToolManager] = None

        # Create the main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the menu bar
        self._create_menu_bar()

        # Create the status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create the notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create frames for tabs
        self.tool_list_frame = ttk.Frame(self.notebook)
        self.tool_editor_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.tool_list_frame, text="Tool List")
        self.notebook.add(self.tool_editor_frame, text="Add Tool")

        # Initialize with empty frames
        self.tool_list = None
        self.tool_editor = None

        # Prompt for config file on startup
        self.after(100, self.prompt_for_config)

    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        self.menu_bar = tk.Menu(self)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Config", command=self.open_config)
        self.file_menu.add_command(label="New Config", command=self.new_config)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tools_menu.add_command(label="Refresh", command=self.refresh_tools)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menu_bar)

    def prompt_for_config(self) -> None:
        """Prompt the user to open or create a configuration file."""
        response = messagebox.askyesnocancel(
            "Configuration",
            "Would you like to open an existing configuration file?\n\n"
            "Yes - Open an existing file\n"
            "No - Create a new file\n"
            "Cancel - Exit the application"
        )

        if response is True:  # Yes
            self.open_config()
        elif response is False:  # No
            self.new_config()
        else:  # Cancel
            self.quit()

    def open_config(self) -> None:
        """Open an existing configuration file."""
        file_path = filedialog.askopenfilename(
            title="Open Configuration File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        if file_path:
            self.load_config(file_path)

    def new_config(self) -> None:
        """Create a new configuration file."""
        file_path = filedialog.asksaveasfilename(
            title="Create Configuration File",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        if file_path:
            # Create an empty config file
            with open(file_path, 'w') as f:
                f.write('{"mcpServers": {}}')

            self.load_config(file_path)

    def load_config(self, config_path: str) -> None:
        """Load a configuration file.

        Args:
            config_path: Path to the configuration file
        """
        try:
            self.config_path = config_path
            self.config_manager = ConfigManager(config_path)
            self.tool_manager = ToolManager(self.config_manager)

            # Update the window title
            self.title(f"MCP Tool Selector - {os.path.basename(config_path)}")

            # Initialize the tool list and editor frames
            if self.tool_list:
                self.tool_list.destroy()

            if self.tool_editor:
                self.tool_editor.destroy()

            self.tool_list = ToolListFrame(self.tool_list_frame, self.tool_manager, self.on_tool_change)
            self.tool_list.pack(fill=tk.BOTH, expand=True)

            self.tool_editor = ToolEditorFrame(self.tool_editor_frame, self.tool_manager, self.on_tool_added)
            self.tool_editor.pack(fill=tk.BOTH, expand=True)

            # Switch to the tool list tab
            self.notebook.select(0)

            self.status_var.set(f"Loaded configuration from {config_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
            self.status_var.set("Error loading configuration")

    def refresh_tools(self) -> None:
        """Refresh the tool list."""
        if self.tool_manager and self.tool_list:
            self.tool_manager.load_tools()
            self.tool_list.refresh()
            self.status_var.set("Tools refreshed")

    def on_tool_change(self) -> None:
        """Handle tool changes."""
        self.status_var.set("Tool configuration updated")

    def on_tool_added(self) -> None:
        """Handle tool addition."""
        self.tool_list.refresh()
        self.notebook.select(0)  # Switch to tool list tab
        self.status_var.set("Tool added")

    def show_about(self) -> None:
        """Show the about dialog."""
        messagebox.showinfo(
            "About MCP Tool Selector",
            "MCP Tool Selector v0.1.0\n\n"
            "A graphical tool for enabling and disabling MCP server tools.\n\n"
            "© 2025"
        )
