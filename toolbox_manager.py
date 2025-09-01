#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧰 D64 Converter - Toolbox Manager
==================================

Configured tool'ları ana GUI'de floating toolbox olarak gösterir
ve kolay erişim sağlar.

Features:
- Floating toolbox window
- Configure edilmiş araçları gösterme
- Quick tool launch
- Tool kategorilerini organize etme
- Compact layout for vertical space
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import json
import threading
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional

class ToolboxManager:
    """
    🧰 Configured tools için floating toolbox manager
    """
    
    def __init__(self, parent_window=None, config_manager=None):
        self.parent = parent_window
        self.config_manager = config_manager
        self.toolbox_window = None
        self.visible = False
        
        # Setup logging
        self.logger = logging.getLogger('ToolboxManager')
        
        # Tool launch processes
        self.running_processes = {}
        
    def show_toolbox(self):
        """Show floating toolbox window"""
        if self.toolbox_window is None:
            self._create_toolbox()
        
        if not self.visible:
            self.toolbox_window.deiconify()
            self.visible = True
            
            # Position relative to parent
            if self.parent:
                parent_x = self.parent.winfo_x()
                parent_y = self.parent.winfo_y()
                parent_height = self.parent.winfo_height()
                
                # Position to the right of parent window
                self.toolbox_window.geometry(f"300x{parent_height}+{parent_x + self.parent.winfo_width() + 10}+{parent_y}")
            
            self._refresh_tools()
    
    def hide_toolbox(self):
        """Hide floating toolbox window"""
        if self.toolbox_window and self.visible:
            self.toolbox_window.withdraw()
            self.visible = False
    
    def toggle_toolbox(self):
        """Toggle toolbox visibility"""
        if self.visible:
            self.hide_toolbox()
        else:
            self.show_toolbox()
    
    def _create_toolbox(self):
        """Create the floating toolbox window"""
        self.toolbox_window = tk.Toplevel()
        self.toolbox_window.title("🧰 D64 Converter Toolbox")
        self.toolbox_window.geometry("300x600")
        
        # Window configuration
        self.toolbox_window.configure(bg='#2d2d2d')
        self.toolbox_window.resizable(True, True)
        self.toolbox_window.attributes('-topmost', True)
        
        # Hide instead of destroy when closed
        self.toolbox_window.protocol("WM_DELETE_WINDOW", self.hide_toolbox)
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.toolbox_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="🧰 Configured Tools", 
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = ttk.Button(header_frame, text="🔄", width=3,
                                command=self._refresh_tools)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Configuration button
        config_btn = ttk.Button(header_frame, text="⚙️", width=3,
                               command=self._open_configuration)
        config_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Create scrollable frame for tools
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store references
        self.canvas = canvas
        self.scrollbar = scrollbar
        
        # Bind mouse wheel
        self._bind_mousewheel()
    
    def _bind_mousewheel(self):
        """Bind mouse wheel scrolling to canvas"""
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", on_mousewheel)
    
    def _refresh_tools(self):
        """Refresh tool list from configuration"""
        if not self.config_manager:
            self._show_no_config_message()
            return
        
        # Clear existing tools
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get configured tools
        configured_tools = self._get_configured_tools()
        
        if not configured_tools:
            self._show_no_tools_message()
            return
        
        # Create tool categories
        self._create_tool_categories(configured_tools)
    
    def _get_configured_tools(self) -> Dict[str, List[Tuple[str, str, bool]]]:
        """Get list of configured tools from config manager"""
        if not hasattr(self.config_manager, 'config'):
            return {}
        
        configured = {}
        config = self.config_manager.config
        
        # Categories to display
        categories = ["assemblers", "compilers", "interpreters", "ides", "emulators", "utilities"]
        
        for category in categories:
            if category in config:
                tools = []
                for tool_name, tool_info in config[category].items():
                    if (isinstance(tool_info, dict) and 
                        tool_info.get("enabled", False) and 
                        tool_info.get("path")):
                        
                        path = tool_info["path"]
                        verified = tool_info.get("verified", False)
                        tools.append((tool_name, path, verified))
                
                if tools:
                    configured[category] = tools
        
        return configured
    
    def _create_tool_categories(self, configured_tools: Dict[str, List[Tuple[str, str, bool]]]):
        """Create tool category sections in toolbox"""
        category_icons = {
            "assemblers": "🔧",
            "compilers": "⚙️", 
            "interpreters": "🐍",
            "ides": "💻",
            "emulators": "🎮",
            "utilities": "🛠️"
        }
        
        category_names = {
            "assemblers": "Assemblers",
            "compilers": "Compilers", 
            "interpreters": "Interpreters",
            "ides": "IDEs & Editors",
            "emulators": "Emulators",
            "utilities": "Utilities"
        }
        
        for category, tools in configured_tools.items():
            if not tools:
                continue
            
            # Category header
            category_frame = ttk.LabelFrame(self.scrollable_frame, 
                                          text=f"{category_icons.get(category, '📦')} {category_names.get(category, category.title())}")
            category_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Tools in category
            for tool_name, tool_path, verified in tools:
                self._create_tool_button(category_frame, tool_name, tool_path, verified)
    
    def _create_tool_button(self, parent, tool_name: str, tool_path: str, verified: bool):
        """Create a button for individual tool"""
        tool_frame = ttk.Frame(parent)
        tool_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Status icon
        status_icon = "✅" if verified else "⚠️"
        
        # Tool button
        tool_btn = ttk.Button(tool_frame, 
                             text=f"{status_icon} {tool_name}",
                             command=lambda: self._launch_tool(tool_name, tool_path))
        tool_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Info button (show path on hover)
        info_btn = ttk.Button(tool_frame, text="ℹ️", width=3,
                             command=lambda: self._show_tool_info(tool_name, tool_path, verified))
        info_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Tooltip for path
        self._create_tooltip(tool_btn, f"Path: {tool_path}")
    
    def _create_tooltip(self, widget, text):
        """Create tooltip for widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, 
                           background="#ffffe0", 
                           font=('Segoe UI', 8))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _launch_tool(self, tool_name: str, tool_path: str):
        """Launch selected tool"""
        self.logger.info(f"🚀 Launching tool: {tool_name}")
        
        try:
            # Check if tool exists
            if not os.path.exists(tool_path):
                messagebox.showerror("Error", f"Tool not found: {tool_path}")
                return
            
            # Special handling for different tool types
            if tool_path.endswith('.jar'):
                # Java applications
                process = subprocess.Popen(['java', '-jar', tool_path], 
                                         shell=True)
            elif tool_path.endswith('.exe') or os.access(tool_path, os.X_OK):
                # Executable files
                process = subprocess.Popen([tool_path], 
                                         shell=True,
                                         cwd=os.path.dirname(tool_path))
            else:
                # Try to open with system default
                if os.name == 'nt':  # Windows
                    process = subprocess.Popen(['start', '', tool_path], 
                                             shell=True)
                else:  # Unix-like
                    process = subprocess.Popen(['xdg-open', tool_path])
            
            # Store process reference
            self.running_processes[tool_name] = process
            
            # Show success message
            self._show_launch_status(tool_name, True)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to launch {tool_name}: {e}")
            messagebox.showerror("Launch Error", 
                               f"Failed to launch {tool_name}:\n{str(e)}")
            self._show_launch_status(tool_name, False)
    
    def _show_launch_status(self, tool_name: str, success: bool):
        """Show temporary launch status"""
        status_window = tk.Toplevel(self.toolbox_window)
        status_window.title("Launch Status")
        status_window.geometry("300x100")
        status_window.resizable(False, False)
        
        # Center on toolbox
        if self.toolbox_window:
            x = self.toolbox_window.winfo_x() + 50
            y = self.toolbox_window.winfo_y() + 100
            status_window.geometry(f"300x100+{x}+{y}")
        
        icon = "✅" if success else "❌"
        message = f"Launched: {tool_name}" if success else f"Failed to launch: {tool_name}"
        
        ttk.Label(status_window, text=f"{icon} {message}", 
                 font=('Segoe UI', 10)).pack(pady=20)
        
        ttk.Button(status_window, text="OK", 
                  command=status_window.destroy).pack(pady=10)
        
        # Auto close after 3 seconds
        status_window.after(3000, lambda: status_window.destroy() if status_window.winfo_exists() else None)
    
    def _show_tool_info(self, tool_name: str, tool_path: str, verified: bool):
        """Show detailed tool information"""
        info_window = tk.Toplevel(self.toolbox_window)
        info_window.title(f"Tool Info: {tool_name}")
        info_window.geometry("400x250")
        info_window.resizable(False, False)
        
        # Center on toolbox
        if self.toolbox_window:
            x = self.toolbox_window.winfo_x() + 50
            y = self.toolbox_window.winfo_y() + 50
            info_window.geometry(f"400x250+{x}+{y}")
        
        main_frame = ttk.Frame(info_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tool name
        ttk.Label(main_frame, text=f"Tool: {tool_name}", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Path
        ttk.Label(main_frame, text="Path:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        path_text = tk.Text(main_frame, height=3, width=50, wrap=tk.WORD)
        path_text.insert(tk.END, tool_path)
        path_text.config(state=tk.DISABLED)
        path_text.pack(fill=tk.X, pady=(0, 10))
        
        # Status
        status_text = "✅ Verified" if verified else "⚠️ Not verified"
        ttk.Label(main_frame, text=f"Status: {status_text}").pack(anchor=tk.W, pady=(0, 10))
        
        # File info
        if os.path.exists(tool_path):
            file_size = os.path.getsize(tool_path)
            file_size_mb = file_size / (1024 * 1024)
            ttk.Label(main_frame, text=f"Size: {file_size_mb:.2f} MB").pack(anchor=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Launch", 
                  command=lambda: [self._launch_tool(tool_name, tool_path), info_window.destroy()]).pack(side=tk.LEFT)
        
        ttk.Button(btn_frame, text="Open Folder", 
                  command=lambda: self._open_tool_folder(tool_path)).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(btn_frame, text="Close", 
                  command=info_window.destroy).pack(side=tk.RIGHT)
    
    def _open_tool_folder(self, tool_path: str):
        """Open folder containing the tool"""
        try:
            folder_path = os.path.dirname(tool_path)
            if os.name == 'nt':  # Windows
                subprocess.Popen(['explorer', folder_path])
            else:  # Unix-like
                subprocess.Popen(['xdg-open', folder_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder:\n{str(e)}")
    
    def _open_configuration(self):
        """Open configuration manager"""
        if self.config_manager and hasattr(self.config_manager, 'show'):
            self.config_manager.show()
        else:
            messagebox.showinfo("Info", "Configuration Manager not available")
    
    def _show_no_config_message(self):
        """Show message when no config manager available"""
        msg_frame = ttk.Frame(self.scrollable_frame)
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
        
        ttk.Label(msg_frame, text="⚙️ No Configuration Manager", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(msg_frame, text="Please configure tools first\nusing the Configuration Manager",
                 justify=tk.CENTER).pack(pady=(0, 20))
        
        ttk.Button(msg_frame, text="Open Configuration", 
                  command=self._open_configuration).pack()
    
    def _show_no_tools_message(self):
        """Show message when no tools configured"""
        msg_frame = ttk.Frame(self.scrollable_frame)
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
        
        ttk.Label(msg_frame, text="🔧 No Tools Configured", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(msg_frame, text="No tools have been configured yet.\nUse the Configuration Manager\nto detect and configure tools.",
                 justify=tk.CENTER).pack(pady=(0, 20))
        
        ttk.Button(msg_frame, text="Configure Tools", 
                  command=self._open_configuration).pack()
    
    def cleanup(self):
        """Cleanup running processes and close toolbox"""
        # Terminate running processes
        for tool_name, process in self.running_processes.items():
            try:
                if process.poll() is None:  # Still running
                    process.terminate()
                    self.logger.info(f"🛑 Terminated process: {tool_name}")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to terminate {tool_name}: {e}")
        
        # Close toolbox
        if self.toolbox_window:
            self.toolbox_window.destroy()
            self.toolbox_window = None
            self.visible = False

# Example usage
if __name__ == "__main__":
    # Test window
    root = tk.Tk()
    root.title("Test Parent Window")
    root.geometry("800x600")
    
    # Create toolbox manager
    toolbox = ToolboxManager(parent_window=root)
    
    # Test button
    ttk.Button(root, text="Show Toolbox", 
              command=toolbox.show_toolbox).pack(pady=20)
    
    # Cleanup on close
    root.protocol("WM_DELETE_WINDOW", lambda: [toolbox.cleanup(), root.destroy()])
    
    root.mainloop()
