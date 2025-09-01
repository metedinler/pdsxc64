#!/usr/bin/env python3
"""
🔧 Configuration Manager v2.0
Enhanced Universal Disk Reader Configuration & Setup Interface

Converts GUI selector functionality to intelligent configuration management
for external assemblers, programming languages, and development environments.

Author: Enhanced Universal Disk Reader Team
Version: 2.0
Date: 2025-01-20
"""

import os
import sys
import json
import platform
import subprocess
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple

class ConfigurationManager:
    """
    🎯 Intelligent Configuration Manager
    
    Features:
    - External assembler detection and setup (64TASS, ACME, DASM, KickAss, etc.)
    - Programming language environment configuration
    - IDE integration setup (CrossViper, etc.)
    - Path management and validation
    - Configuration persistence
    """
    
    def __init__(self, parent=None):
        self.parent = parent
        self.root = None
        self.config_file = Path("config/system_configuration.json")
        self.detected_tools_file = Path("config/detected_tools.json")  # Yeni: Persistent detected tools
        self.config_file.parent.mkdir(exist_ok=True)
        
        # Default configuration template (streamlined for basic tools)
        self.default_config = {
            "assemblers": {
                "64tass": {"path": "", "version": "", "enabled": False, "verified": False},
                "acme": {"path": "", "version": "", "enabled": False, "verified": False},
                "dasm": {"path": "", "version": "", "enabled": False, "verified": False},
                "kickass": {"path": "", "version": "", "enabled": False, "verified": False},
                "ca65": {"path": "", "version": "", "enabled": False, "verified": False},
                "xa": {"path": "", "version": "", "enabled": False, "verified": False}
            },
            "compilers": {
                "cc65": {"path": "", "version": "", "enabled": False, "verified": False},
                "oscar64": {"path": "", "version": "", "enabled": False, "verified": False}
            },
            "interpreters": {
                "python": {"path": "", "version": "", "enabled": True, "verified": False},
                "qbasic": {"path": "", "version": "", "enabled": False, "verified": False}
            },
            "ides": {
                "vscode": {"path": "", "version": "", "enabled": False, "verified": False},
                "crossviper": {"path": "", "version": "", "enabled": False, "verified": False}
            },
            "emulators": {
                "vice": {"path": "", "version": "", "enabled": False, "verified": False},
                "ccs64": {"path": "", "version": "", "enabled": False, "verified": False}
            },
            "preferences": {
                "default_assembler": "64tass",
                "default_language": "c",
                "output_format": "native",
                "auto_detect": True,
                "theme": "light",
                "use_basic_tools": True,
                "use_extended_tools": False
            }
        }
        
        self.config = self.load_configuration()
        self.setup_logging()
        
        # Tool detection patterns loaded from JSON files
        self.tool_patterns = self.load_tool_patterns()
        
        # Load previously detected tools
        self.detected_tools_data = self.load_detected_tools()
        
    def load_detected_tools(self):
        """Load previously detected tools from persistent storage"""
        try:
            if self.detected_tools_file.exists():
                with open(self.detected_tools_file, 'r', encoding='utf-8') as f:
                    detected_data = json.load(f)
                    self.logger.info(f"✅ Önceki tespit sonuçları yüklendi: {len(detected_data.get('tools', {}))} kategori")
                    return detected_data
            else:
                # Create default structure
                default_structure = {
                    "last_detection": "",
                    "detection_count": 0,
                    "tools": {
                        "assemblers": {},
                        "compilers": {},
                        "interpreters": {},
                        "ides": {},
                        "emulators": {},
                        "utilities": {}
                    },
                    "tool_usage": {
                        "command_templates": {},
                        "help_info": {},
                        "usage_examples": {}
                    },
                    "variables": {
                        "%YOL%": "working_directory",
                        "%DOSYAADI%": "input_filename", 
                        "%CIKTI%": "output_filename",
                        "%BASLANGIC%": "start_address",
                        "%FORMAT%": "output_format"
                    }
                }
                return default_structure
        except Exception as e:
            self.logger.error(f"❌ Detected tools yüklenemedi: {e}")
            return {"tools": {}, "tool_usage": {}, "variables": {}}
    
    def save_detected_tools(self, detected_results):
        """Save detected tools to persistent storage with timestamp"""
        try:
            import datetime
            
            # Update detected tools data
            self.detected_tools_data["last_detection"] = datetime.datetime.now().isoformat()
            self.detected_tools_data["detection_count"] = self.detected_tools_data.get("detection_count", 0) + 1
            
            # Store detected tools with their verification status
            for category, tools in detected_results.items():
                if category not in self.detected_tools_data["tools"]:
                    self.detected_tools_data["tools"][category] = {}
                
                for tool_name, tool_path, verified in tools:
                    self.detected_tools_data["tools"][category][tool_name] = {
                        "path": tool_path,
                        "verified": verified,
                        "enabled": verified,  # Auto-enable verified tools
                        "version": self.config.get(category, {}).get(tool_name, {}).get("version", ""),
                        "detection_date": datetime.datetime.now().isoformat(),
                        "category": category
                    }
            
            # Save to file
            with open(self.detected_tools_file, 'w', encoding='utf-8') as f:
                json.dump(self.detected_tools_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Tespit sonuçları kaydedildi: {self.detected_tools_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Detected tools kaydedilemedi: {e}")
            return False
    
    def get_available_tools(self):
        """Get list of available (previously detected) tools"""
        available = {}
        
        for category, tools in self.detected_tools_data.get("tools", {}).items():
            available[category] = {}
            for tool_name, tool_info in tools.items():
                if tool_info.get("enabled", False) and os.path.exists(tool_info.get("path", "")):
                    available[category][tool_name] = tool_info
        
        return available
    
    def learn_tool_usage(self, tool_name, tool_path, category):
        """Learn tool usage by executing help commands and save to log"""
        self.logger.info(f"📚 {tool_name} kullanım bilgileri öğreniliyor...")
        
        help_commands = ["--help", "-h", "--version", "-v", "-?", "/?"]
        usage_info = {
            "tool_name": tool_name,
            "tool_path": tool_path,
            "category": category,
            "help_outputs": {},
            "command_templates": [],
            "variables_used": []
        }
        
        # Create logs directory
        logs_dir = Path("logs/tool_usage")
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = logs_dir / f"{tool_name}_usage.txt"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {tool_name.upper()} USAGE LEARNING SESSION ===\n")
            f.write(f"Tool Path: {tool_path}\n")
            f.write(f"Category: {category}\n")
            f.write(f"Learning Date: {datetime.datetime.now()}\n")
            f.write("=" * 60 + "\n\n")
            
            for cmd in help_commands:
                try:
                    self.logger.info(f"🔍 Deneniyor: {tool_name} {cmd}")
                    f.write(f"COMMAND: {tool_name} {cmd}\n")
                    f.write("-" * 40 + "\n")
                    
                    # Special handling for different tool types
                    if tool_path.endswith('.jar'):
                        # Java applications
                        result = subprocess.run(['java', '-jar', tool_path, cmd], 
                                              capture_output=True, text=True, timeout=10)
                    else:
                        # Regular executables
                        result = subprocess.run([tool_path, cmd], 
                                              capture_output=True, text=True, timeout=10)
                    
                    # Capture both stdout and stderr
                    output = ""
                    if result.stdout:
                        output += "STDOUT:\n" + result.stdout + "\n"
                    if result.stderr:
                        output += "STDERR:\n" + result.stderr + "\n"
                    
                    if output.strip():
                        f.write(output)
                        usage_info["help_outputs"][cmd] = {
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                            "returncode": result.returncode
                        }
                        
                        # Parse for command templates and variables
                        self._parse_usage_patterns(output, usage_info)
                        
                        self.logger.info(f"✅ {cmd} başarılı")
                    else:
                        f.write("No output received\n")
                        self.logger.debug(f"⚠️ {cmd} çıktı vermedi")
                    
                    f.write(f"Return Code: {result.returncode}\n")
                    f.write("\n" + "="*60 + "\n\n")
                    
                except subprocess.TimeoutExpired:
                    f.write("TIMEOUT: Command took too long to execute\n\n")
                    self.logger.warning(f"⏰ {tool_name} {cmd} zaman aşımı")
                except Exception as e:
                    f.write(f"ERROR: {str(e)}\n\n")
                    self.logger.error(f"❌ {tool_name} {cmd} hatası: {e}")
        
        # Save usage info to detected tools data
        if "tool_usage" not in self.detected_tools_data:
            self.detected_tools_data["tool_usage"] = {}
        
        self.detected_tools_data["tool_usage"][tool_name] = usage_info
        
        # Generate command templates based on tool type
        self._generate_command_templates(tool_name, usage_info)
        
        self.logger.info(f"📚 {tool_name} kullanım bilgileri kaydedildi: {log_file}")
        return usage_info
    
    def _parse_usage_patterns(self, output, usage_info):
        """Parse output to find usage patterns and variables"""
        import re
        
        # Common patterns to look for
        patterns = {
            "input_file": r"(?i)(?:input|source|file).*?\.(?:prg|d64|asm|s|src)",
            "output_file": r"(?i)(?:output|dest|target).*?\.(?:asm|prg|bin|obj)",
            "options": r"(?i)-[a-z]|--[a-z-]+",
            "addresses": r"\$[0-9a-fA-F]+|0x[0-9a-fA-F]+",
            "formats": r"(?i)(?:format|mode).*?(?:tass|kick|dasm|acme|ca65)"
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, output)
            if matches:
                usage_info["variables_used"].extend(matches)
    
    def _generate_command_templates(self, tool_name, usage_info):
        """Generate command templates based on tool type and learned usage"""
        templates = []
        
        # Template generation based on tool type
        if tool_name == "64tass":
            templates = [
                "%TOOL_PATH% %DOSYAADI% -o %CIKTI%",
                "%TOOL_PATH% --verbose %DOSYAADI% -o %CIKTI%", 
                "%TOOL_PATH% --list %DOSYAADI% -o %CIKTI% --list=%CIKTI%.lst",
                "%TOOL_PATH% --labels %DOSYAADI% -o %CIKTI% --labels=%CIKTI%.lbl"
            ]
        elif tool_name == "acme":
            templates = [
                "%TOOL_PATH% %DOSYAADI%",
                "%TOOL_PATH% --outfile %CIKTI% %DOSYAADI%",
                "%TOOL_PATH% --format cbm %DOSYAADI%"
            ]
        elif tool_name == "dasm":
            templates = [
                "%TOOL_PATH% %DOSYAADI% -o%CIKTI%",
                "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -l%CIKTI%.lst",
                "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -s%CIKTI%.sym"
            ]
        elif tool_name == "kickass":
            templates = [
                "java -jar %TOOL_PATH% %DOSYAADI%",
                "java -jar %TOOL_PATH% -o %CIKTI% %DOSYAADI%",
                "java -jar %TOOL_PATH% -symbolfile -vicesymbols %DOSYAADI%"
            ]
        elif tool_name == "cc65":
            templates = [
                "%TOOL_PATH% -t c64 %DOSYAADI%",
                "%TOOL_PATH% -t c64 -O %DOSYAADI% -o %CIKTI%"
            ]
        elif tool_name == "oscar64":
            templates = [
                "%TOOL_PATH% %DOSYAADI% -o %CIKTI%",
                "%TOOL_PATH% -tm=c64 %DOSYAADI% -o %CIKTI%"
            ]
        elif tool_name == "python":
            templates = [
                "%TOOL_PATH% %DOSYAADI%",
                "%TOOL_PATH% -m %MODULE% %DOSYAADI%"
            ]
        else:
            # Generic templates
            templates = [
                "%TOOL_PATH% %DOSYAADI%",
                "%TOOL_PATH% %DOSYAADI% %CIKTI%",
                "%TOOL_PATH% --help"
            ]
        
        # Save templates
        if "command_templates" not in self.detected_tools_data["tool_usage"]:
            self.detected_tools_data["tool_usage"]["command_templates"] = {}
        
        self.detected_tools_data["tool_usage"]["command_templates"][tool_name] = templates
        usage_info["command_templates"] = templates
    
    def execute_tool_command(self, tool_name, command_template, variables=None):
        """Execute a tool command with variable substitution"""
        if not variables:
            variables = {}
        
        # Get tool info
        tool_info = None
        for category, tools in self.detected_tools_data.get("tools", {}).items():
            if tool_name in tools:
                tool_info = tools[tool_name]
                break
        
        if not tool_info:
            self.logger.error(f"❌ Tool not found: {tool_name}")
            return None
        
        # Substitute variables
        command = command_template
        command = command.replace("%TOOL_PATH%", tool_info["path"])
        
        # Standard variable substitutions
        substitutions = {
            "%YOL%": variables.get("working_directory", os.getcwd()),
            "%DOSYAADI%": variables.get("input_filename", ""),
            "%CIKTI%": variables.get("output_filename", "output.prg"),
            "%BASLANGIC%": variables.get("start_address", "$0801"),
            "%FORMAT%": variables.get("output_format", "prg")
        }
        
        for var, value in substitutions.items():
            command = command.replace(var, str(value))
        
        self.logger.info(f"🚀 Executing: {command}")
        
        # Execute command
        try:
            # Create execution log
            exec_log_dir = Path("logs/tool_execution")
            exec_log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = exec_log_dir / f"{tool_name}_execution_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== {tool_name.upper()} EXECUTION LOG ===\n")
                f.write(f"Command: {command}\n")
                f.write(f"Working Directory: {variables.get('working_directory', os.getcwd())}\n")
                f.write(f"Execution Time: {datetime.datetime.now()}\n")
                f.write("=" * 60 + "\n\n")
                
                # Execute
                result = subprocess.run(command, shell=True, 
                                      capture_output=True, text=True, 
                                      cwd=variables.get("working_directory", os.getcwd()))
                
                f.write(f"RETURN CODE: {result.returncode}\n\n")
                
                if result.stdout:
                    f.write("STDOUT:\n")
                    f.write(result.stdout)
                    f.write("\n\n")
                
                if result.stderr:
                    f.write("STDERR:\n")
                    f.write(result.stderr)
                    f.write("\n\n")
            
            self.logger.info(f"✅ Command executed, log saved: {log_file}")
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command,
                "log_file": str(log_file)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Command execution failed: {e}")
            return None
        
    def load_tool_patterns(self):
        """Load tool patterns from JSON configuration files"""
        patterns = {}
        
        # Load basic tools (always loaded)
        basic_tools_file = Path("config/basic_tools.json")
        if basic_tools_file.exists():
            try:
                with open(basic_tools_file, 'r', encoding='utf-8') as f:
                    basic_tools = json.load(f)
                    patterns.update(basic_tools)
                    self.logger.info(f"✅ Temel araçlar yüklendi: {basic_tools_file}")
            except Exception as e:
                self.logger.error(f"❌ Temel araç listesi yüklenemedi: {e}")
        
        # Load extended tools if enabled
        if self.config.get("preferences", {}).get("use_extended_tools", False):
            extended_tools_file = Path("config/extended_tools.json")
            if extended_tools_file.exists():
                try:
                    with open(extended_tools_file, 'r', encoding='utf-8') as f:
                        extended_tools = json.load(f)
                        # Merge extended tools with basic tools
                        for category, tools in extended_tools.items():
                            if category in patterns:
                                patterns[category].update(tools)
                            else:
                                patterns[category] = tools
                        self.logger.info(f"✅ Genişletilmiş araçlar yüklendi: {extended_tools_file}")
                except Exception as e:
                    self.logger.error(f"❌ Genişletilmiş araç listesi yüklenemedi: {e}")
        
        return patterns
    
    def setup_logging(self):
        """Setup enhanced logging for configuration manager"""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - [Config Manager] - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def load_configuration(self) -> Dict:
        """Load configuration from file or create default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Merge with default config to ensure all keys exist
                merged_config = self.default_config.copy()
                self._deep_merge(merged_config, config)
                return merged_config
            else:
                return self.default_config.copy()
        except Exception as e:
            self.logger.error(f"Configuration load error: {e}")
            return self.default_config.copy()
    
    def save_configuration(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Configuration saved: {self.config_file}")
            return True
        except Exception as e:
            self.logger.error(f"Configuration save error: {e}")
            return False
    
    def _deep_merge(self, base: Dict, update: Dict):
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def detect_tools(self) -> Dict[str, List[Tuple[str, str, bool]]]:
        """
        🔍 Auto-detect installed development tools with comprehensive search
        Returns: {category: [(name, path, verified), ...]}
        """
        detected = {
            "assemblers": [],
            "compilers": [],
            "interpreters": [],
            "ides": [],
            "emulators": []
        }
        
        # Expanded search paths with recursive search and user configuration
        base_search_paths = []
        
        # Add default paths if enabled
        if getattr(self, 'use_default_paths', None) is None or self.use_default_paths.get():
            if platform.system() == "Windows":
                base_search_paths = [
                    "C:\\Program Files\\",
                    "C:\\Program Files (x86)\\",
                    "C:\\Tools\\",
                    "C:\\dev\\",
                    "C:\\development\\",
                    "C:\\coding\\",
                    "C:\\emulators\\",
                    "C:\\assemblers\\",
                    "C:\\compilers\\",
                    os.path.expanduser("~\\AppData\\Local\\"),
                    os.path.expanduser("~\\Desktop\\"),
                    os.path.expanduser("~\\Downloads\\"),
                    os.path.expanduser("~\\Documents\\"),
                    os.path.expanduser("~\\tools\\"),
                    os.path.expanduser("~\\dev\\"),
                    os.getcwd(),
                    "D:\\",
                    "E:\\",
                    "F:\\"
                ]
            else:
                base_search_paths = [
                    "/usr/bin/",
                    "/usr/local/bin/",
                    "/opt/",
                    "/usr/share/",
                    "/usr/local/share/",
                    os.path.expanduser("~/bin/"),
                    os.path.expanduser("~/tools/"),
                    os.path.expanduser("~/dev/"),
                    os.path.expanduser("~/Downloads/"),
                    os.path.expanduser("~/Desktop/"),
                    os.getcwd()
                ]
        
        # Add custom search directories
        if hasattr(self, 'custom_search_dirs') and self.custom_search_dirs:
            base_search_paths.extend(self.custom_search_dirs)
            self.logger.info(f"🎯 {len(self.custom_search_dirs)} özel arama dizini eklendi")
        
        # Add PATH directories if not in fast mode
        if not (hasattr(self, 'fast_mode') and self.fast_mode.get()):
            path_dirs = os.environ.get('PATH', '').split(os.pathsep)
            base_search_paths.extend([p for p in path_dirs if p and os.path.exists(p)])
        
        # Determine search depth based on settings
        max_depth = 1  # Default: shallow search
        if hasattr(self, 'deep_search') and self.deep_search.get():
            max_depth = 7  # 7 seviye derin arama
        elif hasattr(self, 'fast_mode') and self.fast_mode.get():
            max_depth = 0  # Only direct paths, no subdirs
        
        # Generate comprehensive search paths with configurable depth
        search_paths = []
        for base_path in base_search_paths:
            if os.path.exists(base_path):
                search_paths.append(base_path)
                
                # Add subdirectories based on settings
                if max_depth > 0:
                    try:
                        for root, dirs, files in os.walk(base_path):
                            # Filter hidden directories if not enabled
                            if not (hasattr(self, 'search_hidden') and self.search_hidden.get()):
                                dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('$')]
                            
                            # Limit depth
                            level = root.replace(base_path, '').count(os.sep)
                            if level < max_depth:
                                search_paths.append(root)
                            else:
                                dirs[:] = []  # Don't go deeper
                    except (PermissionError, OSError) as e:
                        self.logger.debug(f"Erişim engeli: {base_path} - {e}")
                        continue
        
    def detect_tools(self) -> Dict[str, List[Tuple[str, str, bool]]]:
        """
        🔍 Optimized tool detection with JSON-based patterns
        Returns: {category: [(name, path, verified), ...]}
        """
        detected = {
            "assemblers": [],
            "compilers": [],
            "interpreters": [],
            "ides": [],
            "emulators": [],
            "utilities": []
        }
        
        # Get search paths with optimization
        search_paths = self._get_optimized_search_paths()
        
        self.logger.info(f"🔍 Başlıyor optimized araç tespiti - {len(search_paths)} lokasyon")
        
        # Get tool patterns from loaded JSON
        if not hasattr(self, 'tool_patterns') or not self.tool_patterns:
            self.tool_patterns = self.load_tool_patterns()
        
        # Progress tracking
        total_searches = sum(len(tools) for tools in self.tool_patterns.values())
        current_search = 0
        found_tools = set()  # Prevent duplicates
        
        # Search with priority-based optimization
        for category, tools in self.tool_patterns.items():
            if category not in detected:
                detected[category] = []
                
            self.logger.info(f"🔍 Kategori: {category.title()}")
            
            # Sort tools by priority for faster detection
            sorted_tools = sorted(tools.items(), 
                                key=lambda x: x[1].get('priority', 999))
            
            for tool_name, tool_config in sorted_tools:
                current_search += 1
                
                # Skip if already found
                if tool_name in found_tools:
                    continue
                
                # Update progress in GUI
                if hasattr(self, 'summary_stats'):
                    progress_text = f"⏳ Aranan: {tool_name} ({current_search}/{total_searches})"
                    self.summary_stats.config(text=progress_text)
                    if hasattr(self, 'root'):
                        self.root.update()
                
                patterns = tool_config.get('patterns', [])
                found_path = self._search_tool_in_paths(tool_name, patterns, search_paths)
                
                if found_path:
                    self.logger.info(f"✅ Bulundu: {tool_name} -> {found_path}")
                    
                    # Quick verification
                    verified = self._quick_verify_tool(found_path, tool_name, tool_config)
                    detected[category].append((tool_name, found_path, verified))
                    found_tools.add(tool_name)
                    
                    # Update configuration
                    if category in self.config and tool_name in self.config[category]:
                        self.config[category][tool_name]["path"] = found_path
                        self.config[category][tool_name]["verified"] = verified
                        self.config[category][tool_name]["enabled"] = verified
                    
                    # Early exit for fast mode
                    if hasattr(self, 'fast_mode') and self.fast_mode.get():
                        break
        
        # Log final results
        total_found = sum(len(tools) for tools in detected.values())
        self.logger.info(f"🎯 Tespit tamamlandı: {total_found} araç bulundu")
        
        # Save detected tools to persistent storage
        if total_found > 0:
            self.save_detected_tools(detected)
            self.logger.info("💾 Tespit sonuçları persistent storage'a kaydedildi")
        
        return detected
    
    def _get_optimized_search_paths(self):
        """Get optimized search paths based on user settings"""
        search_paths = []
        
        # Add custom search directories first (highest priority)
        if hasattr(self, 'custom_search_dirs') and self.custom_search_dirs:
            search_paths.extend(self.custom_search_dirs)
        
        # Add PATH directories for quick access
        if not (hasattr(self, 'fast_mode') and self.fast_mode.get()):
            path_dirs = os.environ.get('PATH', '').split(os.pathsep)
            search_paths.extend([p for p in path_dirs if p and os.path.exists(p)])
        
        # Add default paths if enabled
        if getattr(self, 'use_default_paths', None) is None or self.use_default_paths.get():
            if platform.system() == "Windows":
                default_paths = [
                    "C:\\Program Files\\",
                    "C:\\Program Files (x86)\\",
                    os.path.expanduser("~\\AppData\\Local\\"),
                    os.path.expanduser("~\\Documents\\"),
                    os.getcwd()
                ]
            else:
                default_paths = [
                    "/usr/bin/",
                    "/usr/local/bin/",
                    os.path.expanduser("~/bin/"),
                    os.getcwd()
                ]
            search_paths.extend(default_paths)
        
        # Remove duplicates while preserving order
        unique_paths = []
        seen = set()
        for path in search_paths:
            if path not in seen and os.path.exists(path):
                unique_paths.append(path)
                seen.add(path)
        
        return unique_paths
    
    def _search_tool_in_paths(self, tool_name, patterns, search_paths):
        """Search for a specific tool in given paths"""
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            # Direct search in path
            for pattern in patterns:
                tool_path = Path(search_path) / pattern
                if tool_path.exists() and tool_path.is_file():
                    return str(tool_path)
            
            # Limited depth search if not in fast mode
            if not (hasattr(self, 'fast_mode') and self.fast_mode.get()):
                max_depth = 2 if hasattr(self, 'deep_search') and self.deep_search.get() else 1
                
                try:
                    for root, dirs, files in os.walk(search_path):
                        # Limit depth
                        level = root.replace(search_path, '').count(os.sep)
                        if level >= max_depth:
                            dirs[:] = []  # Don't go deeper
                            continue
                        
                        # Filter hidden directories
                        if not (hasattr(self, 'search_hidden') and self.search_hidden.get()):
                            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('$')]
                        
                        # Search for patterns in current directory
                        for pattern in patterns:
                            if pattern in files:
                                return str(Path(root) / pattern)
                        
                except (PermissionError, OSError):
                    continue
        
        return None
    
    def _quick_verify_tool(self, tool_path, tool_name, tool_config):
        """Quick tool verification to avoid hanging"""
        try:
            verification_commands = tool_config.get('verification', ['--version'])
            
            for cmd in verification_commands:
                try:
                    if cmd == 'java' and tool_path.endswith('.jar'):
                        # Special handling for Java applications
                        result = subprocess.run(['java', '-jar', tool_path, '--version'], 
                                              capture_output=True, text=True, timeout=3)
                    else:
                        result = subprocess.run([tool_path, cmd], 
                                              capture_output=True, text=True, timeout=3)
                    
                    if result.returncode == 0:
                        # Extract version info if available
                        version = (result.stdout + result.stderr)[:100].strip()
                        if tool_name in self.config.get(self._get_tool_category(tool_name), {}):
                            category = self._get_tool_category(tool_name)
                            self.config[category][tool_name]["version"] = version
                        return True
                except subprocess.TimeoutExpired:
                    self.logger.warning(f"⏰ Doğrulama zaman aşımı: {tool_name}")
                    continue
                except:
                    continue
            
            # If verification fails, still consider as found but unverified
            return os.path.isfile(tool_path) and os.access(tool_path, os.X_OK)
            
        except Exception as e:
            self.logger.debug(f"Doğrulama hatası {tool_path}: {e}")
            return False
    
    def _get_tool_category(self, tool_name):
        """Get category of a tool"""
        for category, tools in self.tool_patterns.items():
            if tool_name in tools:
                return category
        return "utilities"
    
    def _verify_tool(self, tool_path: str, tool_name: str) -> bool:
        """Verify if tool is working and get version info"""
        try:
            if tool_name == "python":
                result = subprocess.run([tool_path, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip() or result.stderr.strip()
                    if tool_name in self.config.get("interpreters", {}):
                        self.config["interpreters"][tool_name]["version"] = version
                    return True
            
            elif tool_name in ["64tass", "acme", "dasm", "ca65", "xa"]:
                # Try version command
                for version_cmd in ["--version", "-V", "--help"]:
                    try:
                        result = subprocess.run([tool_path, version_cmd], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            version = (result.stdout + result.stderr)[:100]
                            if tool_name in self.config.get("assemblers", {}):
                                self.config["assemblers"][tool_name]["version"] = version
                            return True
                    except:
                        continue
            
            elif tool_path.endswith(".jar"):
                # Java applications
                try:
                    result = subprocess.run(["java", "-jar", tool_path, "--version"], 
                                          capture_output=True, text=True, timeout=5)
                    return result.returncode == 0
                except:
                    return False
            
            elif tool_path.endswith(".exe") or not tool_path.endswith((".jar", ".py")):
                # Executable files - check if they exist and are executable
                return os.path.isfile(tool_path) and os.access(tool_path, os.X_OK)
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Tool verification failed for {tool_path}: {e}")
            return False
    
    def create_configuration_gui(self):
        """Create comprehensive configuration GUI"""
        if self.root:
            self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title("🔧 Enhanced Universal Disk Reader - Configuration Manager v2.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Auto Detection
        detection_frame = ttk.Frame(notebook)
        notebook.add(detection_frame, text="🔍 Auto Detection")
        self._create_detection_tab(detection_frame)
        
        # Tab 2: Manual Configuration
        manual_frame = ttk.Frame(notebook)
        notebook.add(manual_frame, text="⚙️ Manual Setup")
        self._create_manual_tab(manual_frame)
        
        # Tab 3: Preferences
        prefs_frame = ttk.Frame(notebook)
        notebook.add(prefs_frame, text="🎯 Preferences")
        self._create_preferences_tab(prefs_frame)
        
        # Tab 4: Export/Import
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="💾 Export/Import")
        self._create_export_tab(export_frame)
        
        # Bottom button frame - simplified (GUI button moved to detection tab)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Left side buttons
        left_frame = ttk.Frame(button_frame)
        left_frame.pack(side=tk.LEFT)
        
        ttk.Button(left_frame, text="💾 Save Configuration", 
                  command=self.save_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_frame, text="🔄 Reload", 
                  command=self._reload_configuration).pack(side=tk.LEFT, padx=5)
        
        # Right side buttons
        right_frame = ttk.Frame(button_frame)
        right_frame.pack(side=tk.RIGHT)
        
        ttk.Button(right_frame, text="❌ Close", 
                  command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _create_detection_tab(self, parent):
        """Create auto-detection tab with improved layout and manual search paths"""
        # Header section - reorganized with left/right alignment
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Top row with title and description
        title_row = ttk.Frame(header_frame)
        title_row.pack(fill=tk.X, pady=(0, 6))
        
        # Left side - title
        info_label = ttk.Label(title_row, 
                              text="🔍 Otomatik Araç Tespiti",
                              font=("Arial", 14, "bold"))
        info_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Right side - description (same font size)
        desc_label = ttk.Label(title_row, 
                              text="Sisteminizde yüklü geliştirme araçları tespit edilir ve yapılandırılır",
                              font=("Arial", 10))
        desc_label.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Search Configuration Section - moved up 2 pixels
        search_config_frame = ttk.LabelFrame(header_frame, text="🎯 Arama Yapılandırması")
        search_config_frame.pack(fill=tk.X, pady=(0, 3))
        
        # Default search areas - checkbox aligned right
        default_frame = ttk.Frame(search_config_frame)
        default_frame.pack(fill=tk.X, padx=10, pady=2)
        
        self.use_default_paths = tk.BooleanVar(value=True)
        ttk.Checkbutton(default_frame, text="✅ Varsayılan konumları tara (Program Files, Tools, PATH vb.)", 
                       variable=self.use_default_paths).pack(anchor=tk.E)
        
        # Custom search directories - moved up
        custom_frame = ttk.Frame(search_config_frame)
        custom_frame.pack(fill=tk.X, padx=10, pady=(0, 2))
        
        ttk.Label(custom_frame, text="📁 Ek Arama Dizinleri:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        # Main control layout - entry and buttons in organized layout
        control_frame = ttk.Frame(custom_frame)
        control_frame.pack(fill=tk.X, pady=(2, 2))
        
        # Top row - entry with browse and add buttons
        entry_row = ttk.Frame(control_frame)
        entry_row.pack(fill=tk.X, pady=(0, 2))
        
        self.custom_search_var = tk.StringVar()
        self.custom_search_entry = ttk.Entry(entry_row, textvariable=self.custom_search_var, 
                                           font=("Arial", 9), width=40)
        self.custom_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Browse and Add buttons
        ttk.Button(entry_row, text="📁 Gözat", width=8,
                  command=self._browse_custom_search_dir).pack(side=tk.LEFT, padx=2)
        ttk.Button(entry_row, text="➕ Ekle", width=8,
                  command=self._add_custom_search_dir).pack(side=tk.LEFT, padx=2)
        
        # Bottom row - search options and action buttons
        bottom_row = ttk.Frame(control_frame)
        bottom_row.pack(fill=tk.X, pady=(2, 0))
        
        # Left side - search options (horizontal)
        options_left = ttk.Frame(bottom_row)
        options_left.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(options_left, text="⚙️ Arama Seçenekleri:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        options_checkboxes = ttk.Frame(options_left)
        options_checkboxes.pack(anchor=tk.W, pady=(1, 0))
        
        self.deep_search = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_checkboxes, text="🔍 Derin arama (7 seviye)", 
                       variable=self.deep_search).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_hidden = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_checkboxes, text="👁️ Gizli klasörler", 
                       variable=self.search_hidden).pack(side=tk.LEFT, padx=(0, 10))
        
        self.fast_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_checkboxes, text="⚡ Hızlı mod", 
                       variable=self.fast_mode).pack(side=tk.LEFT)
        
        # Right side - action buttons (aligned with entry top)
        options_right = ttk.Frame(bottom_row)
        options_right.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Button row
        button_row = ttk.Frame(options_right)
        button_row.pack()
        
        # Compact button sizes
        button_width = 8
        
        # Main action button
        ttk.Button(button_row, text="🔍 Ara", width=button_width,
                  command=self._run_auto_detection).pack(side=tk.LEFT, padx=1)
        
        # Additional function buttons - compact layout
        ttk.Button(button_row, text="🔄 Yenile", width=button_width,
                  command=self._refresh_detection_results).pack(side=tk.LEFT, padx=1)
        ttk.Button(button_row, text="📋 Rapor", width=button_width,
                  command=self._show_detection_summary).pack(side=tk.LEFT, padx=1)
        ttk.Button(button_row, text="💾 Kaydet", width=button_width,
                  command=self._save_detected_tools).pack(side=tk.LEFT, padx=1)
        
        # New buttons for tool learning and execution
        ttk.Button(button_row, text="📚 Öğren", width=button_width,
                  command=self._learn_selected_tools).pack(side=tk.LEFT, padx=1)
        ttk.Button(button_row, text="🚀 Test", width=button_width,
                  command=self._test_selected_tool).pack(side=tk.LEFT, padx=1)
        
        # Custom directories list
        self.custom_dirs_frame = ttk.Frame(custom_frame)
        self.custom_dirs_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Custom directories storage
        self.custom_search_dirs = []
        
        # Main control panel with summary and GUI launch button
        control_panel = ttk.Frame(parent)
        control_panel.pack(fill=tk.X, padx=10, pady=(3, 4))
        
        # Left side - compact summary (1/3 width)
        summary_frame = ttk.LabelFrame(control_panel, text="📊 Özet")
        summary_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Create compact summary label
        self.summary_stats = ttk.Label(summary_frame, 
                                      text="⏳ Hazır",
                                      font=("Arial", 8))
        self.summary_stats.pack(padx=8, pady=3)
        
        # Center - prominent GUI launch button (1/3 width)
        gui_launch_frame = ttk.Frame(control_panel)
        gui_launch_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Create the big GUI launch button
        self.gui_launch_button = tk.Button(gui_launch_frame, 
                                          text="🚀 ANA GUI'YE GEÇ",
                                          font=("Arial", 12, "bold"),
                                          bg="#4CAF50",
                                          fg="white",
                                          relief="raised",
                                          bd=3,
                                          command=self._launch_main_gui)
        self.gui_launch_button.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Right side - quick info (1/3 width)
        info_frame = ttk.LabelFrame(control_panel, text="ℹ️ Durum")
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        self.status_info = ttk.Label(info_frame, 
                                    text="Hazır",
                                    font=("Arial", 8))
        self.status_info.pack(padx=8, pady=3)
        
        # Results frame with scrollbar - expanded upward
        results_frame = ttk.LabelFrame(parent, text="🔧 Detaylı Tespit Sonuçları")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Add explanation label for status
        status_info_frame = ttk.Frame(results_frame)
        status_info_frame.pack(fill=tk.X, padx=5, pady=(2, 3))
        
        info_text = "ℹ️ Durum Açıklaması: '✅ Doğrulandı' = Araç çalışır durumda ve versiyon bilgisi alınabildi  •  '⚠️ Bulundu' = Dosya mevcut ancak çalışabilirliği belirsiz"
        ttk.Label(status_info_frame, text=info_text, font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
        
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
        
        # Create treeview for results with increased height
        columns = ("Tool", "Category", "Path", "Status", "Version")
        self.detection_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)
        
        # Configure columns with explanatory tooltips
        self.detection_tree.heading("Tool", text="🔧 Araç Adı")
        self.detection_tree.heading("Category", text="📂 Kategori")
        self.detection_tree.heading("Path", text="📁 Dosya Yolu")
        self.detection_tree.heading("Status", text="✅ Durum")
        self.detection_tree.heading("Version", text="🏷️ Versiyon")
        
        self.detection_tree.column("Tool", width=150, minwidth=100)
        self.detection_tree.column("Category", width=120, minwidth=80)
        self.detection_tree.column("Path", width=300, minwidth=200)
        self.detection_tree.column("Status", width=100, minwidth=80)
        self.detection_tree.column("Version", width=100, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, 
                                   command=self.detection_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, 
                                   command=self.detection_tree.xview)
        
        self.detection_tree.configure(yscrollcommand=v_scrollbar.set,
                                     xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.detection_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu for tree items
        self._create_tree_context_menu()
        
        # Update custom directories display
        self._update_custom_dirs_display()
    
    def _create_manual_tab(self, parent):
        """Create manual configuration tab"""
        # Category selection
        cat_frame = ttk.LabelFrame(parent, text="📂 Tool Categories")
        cat_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.category_var = tk.StringVar(value="assemblers")
        categories = [
            ("🔧 Assemblers", "assemblers"),
            ("⚡ Compilers", "compilers"), 
            ("🐍 Interpreters", "interpreters"),
            ("💻 IDEs", "ides"),
            ("🎮 Emulators", "emulators")
        ]
        
        for i, (label, value) in enumerate(categories):
            ttk.Radiobutton(cat_frame, text=label, variable=self.category_var, 
                           value=value, command=self._update_tool_list).grid(
                           row=0, column=i, padx=10, pady=5)
        
        # Tool configuration area
        config_frame = ttk.LabelFrame(parent, text="⚙️ Tool Configuration")
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Quick access tools panel
        quick_tools_frame = ttk.LabelFrame(config_frame, text="🚀 Available Tools Quick Access")
        quick_tools_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self._create_available_tools_buttons(quick_tools_frame)
        
        # Main tool configuration area
        main_config_frame = ttk.Frame(config_frame)
        main_config_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tool listbox
        list_frame = ttk.Frame(main_config_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Header with refresh and add buttons
        list_header = ttk.Frame(list_frame)
        list_header.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(list_header, text="Available Tools:").pack(side=tk.LEFT)
        
        # Right side buttons
        button_frame = ttk.Frame(list_header)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="➕", width=3,
                  command=self._add_new_tool).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(button_frame, text="🔄", width=3,
                  command=self._refresh_manual_tools).pack(side=tk.LEFT)
        
        self.tool_listbox = tk.Listbox(list_frame, width=20)
        self.tool_listbox.pack(fill=tk.Y, expand=True)
        self.tool_listbox.bind('<<ListboxSelect>>', self._on_tool_select)
        
        # Configuration panel
        detail_frame = ttk.Frame(main_config_frame)
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tool details
        ttk.Label(detail_frame, text="Tool Path:").grid(row=0, column=0, sticky="w", pady=2)
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(detail_frame, textvariable=self.path_var, width=40)
        path_entry.grid(row=0, column=1, pady=2, padx=5)
        ttk.Button(detail_frame, text="📁", command=self._browse_tool_path).grid(row=0, column=2, pady=2)
        
        ttk.Label(detail_frame, text="Version:").grid(row=1, column=0, sticky="w", pady=2)
        self.version_var = tk.StringVar()
        ttk.Entry(detail_frame, textvariable=self.version_var, width=40, state="readonly").grid(row=1, column=1, pady=2, padx=5)
        
        self.enabled_var = tk.BooleanVar()
        ttk.Checkbutton(detail_frame, text="✅ Enabled", variable=self.enabled_var).grid(row=2, column=0, sticky="w", pady=2)
        
        self.verified_var = tk.BooleanVar()
        ttk.Checkbutton(detail_frame, text="🔍 Verified", variable=self.verified_var, state="disabled").grid(row=2, column=1, sticky="w", pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(detail_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="🔍 Verify Tool", command=self._verify_current_tool).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💾 Save Tool", command=self._save_current_tool).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Delete Tool", command=self._delete_current_tool).pack(side=tk.LEFT, padx=5)
        
        detail_frame.grid_columnconfigure(1, weight=1)
        
        # Initialize tool list
        self._update_tool_list()
    
    def _create_available_tools_buttons(self, parent):
        """Create quick access buttons for available tools"""
        # Get available verified tools
        available_tools = []
        
        for category, tools in self.detected_tools_data.get("tools", {}).items():
            for tool_name, tool_info in tools.items():
                if tool_info.get("verified", False) and tool_info.get("enabled", False):
                    available_tools.append((tool_name, category, tool_info.get("path", "")))
        
        if not available_tools:
            ttk.Label(parent, text="No verified tools available. Run detection first.").pack(pady=5)
            return
        
        # Create buttons in rows of 6
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        row = 0
        col = 0
        max_cols = 6
        
        for tool_name, category, tool_path in available_tools[:18]:  # Limit to 18 tools
            # Create tool button
            btn_text = f"🔧 {tool_name}"
            if category == "compilers":
                btn_text = f"⚡ {tool_name}"
            elif category == "interpreters":
                btn_text = f"🐍 {tool_name}"
            elif category == "ides":
                btn_text = f"💻 {tool_name}"
            elif category == "emulators":
                btn_text = f"🎮 {tool_name}"
            
            btn = ttk.Button(button_frame, text=btn_text, width=15,
                           command=lambda t=tool_name, c=category: self._quick_select_tool(t, c))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="w")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Add management buttons
        if available_tools:
            mgmt_frame = ttk.Frame(parent)
            mgmt_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
            
            ttk.Button(mgmt_frame, text="➕ Add Tool", 
                      command=self._add_new_tool).pack(side=tk.LEFT, padx=5)
            ttk.Button(mgmt_frame, text="🔍 Verify All", 
                      command=self._verify_all_tools).pack(side=tk.LEFT, padx=5)
            ttk.Button(mgmt_frame, text="🔄 Refresh Tools", 
                      command=self._refresh_available_tools).pack(side=tk.LEFT, padx=5)
            ttk.Button(mgmt_frame, text="💾 Save All", 
                      command=self.save_configuration).pack(side=tk.LEFT, padx=5)
            ttk.Button(mgmt_frame, text="❌ Delete Selected", 
                      command=self._delete_current_tool).pack(side=tk.LEFT, padx=5)
    
    def _quick_select_tool(self, tool_name, category):
        """Quick select tool from available tools"""
        # Set category
        self.category_var.set(category)
        self._update_tool_list()
        
        # Select tool in listbox
        for i in range(self.tool_listbox.size()):
            if self.tool_listbox.get(i) == tool_name:
                self.tool_listbox.select_set(i)
                self._on_tool_select(None)
                break
    
    def _verify_all_tools(self):
        """Verify all detected tools"""
        try:
            verified_count = 0
            total_count = 0
            
            for category, tools in self.detected_tools_data.get("tools", {}).items():
                for tool_name, tool_info in tools.items():
                    total_count += 1
                    # Run verification for each tool
                    self._verify_and_learn_tool(tool_name, category)
                    if self.detected_tools_data.get("tools", {}).get(category, {}).get(tool_name, {}).get("verified", False):
                        verified_count += 1
            
            messagebox.showinfo("Verification Complete", 
                              f"✅ Verification completed!\n\n"
                              f"📊 Results: {verified_count}/{total_count} tools verified\n"
                              f"🔄 Tool buttons refreshed")
            
            self._refresh_available_tools()
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Verification failed:\n{str(e)}")
    
    def _refresh_available_tools(self):
        """Refresh available tools display"""
        # Reload detected tools
        self.detected_tools_data = self.load_detected_tools()
        
        # Recreate the manual tab to refresh available tools
        messagebox.showinfo("Refreshed", "🔄 Available tools refreshed!\nReopen Manual Setup tab to see changes.")
    
    def _create_preferences_tab(self, parent):
        """Create preferences configuration tab"""
        prefs_frame = ttk.LabelFrame(parent, text="🎯 Global Preferences")
        prefs_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Default assembler
        ttk.Label(prefs_frame, text="Default Assembler:").grid(row=0, column=0, sticky="w", pady=5)
        self.default_assembler_var = tk.StringVar(value=self.config["preferences"]["default_assembler"])
        assembler_combo = ttk.Combobox(prefs_frame, textvariable=self.default_assembler_var,
                                      values=list(self.config["assemblers"].keys()))
        assembler_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        # Default language
        ttk.Label(prefs_frame, text="Default Language:").grid(row=1, column=0, sticky="w", pady=5)
        self.default_language_var = tk.StringVar(value=self.config["preferences"]["default_language"])
        language_combo = ttk.Combobox(prefs_frame, textvariable=self.default_language_var,
                                     values=["c", "cpp", "qbasic", "commodore_basic", "asm"])
        language_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        
        # Output format
        ttk.Label(prefs_frame, text="Output Format:").grid(row=2, column=0, sticky="w", pady=5)
        self.output_format_var = tk.StringVar(value=self.config["preferences"]["output_format"])
        format_combo = ttk.Combobox(prefs_frame, textvariable=self.output_format_var,
                                   values=["native", "tass", "kickass", "dasm", "acme", "ca65"])
        format_combo.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        
        # Theme
        ttk.Label(prefs_frame, text="GUI Theme:").grid(row=3, column=0, sticky="w", pady=5)
        self.theme_var = tk.StringVar(value=self.config["preferences"]["theme"])
        theme_combo = ttk.Combobox(prefs_frame, textvariable=self.theme_var,
                                  values=["light", "dark"])
        theme_combo.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        
        # Auto-detect
        self.auto_detect_var = tk.BooleanVar(value=self.config["preferences"]["auto_detect"])
        ttk.Checkbutton(prefs_frame, text="🔍 Auto-detect tools on startup", 
                       variable=self.auto_detect_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=5)
        
        prefs_frame.grid_columnconfigure(1, weight=1)
        
        # Bind variables to save preferences
        for var in [self.default_assembler_var, self.default_language_var, 
                   self.output_format_var, self.theme_var, self.auto_detect_var]:
            var.trace("w", self._save_preferences)
    
    def _create_export_tab(self, parent):
        """Create export/import configuration tab"""
        export_frame = ttk.LabelFrame(parent, text="💾 Configuration Export/Import")
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Export section
        ttk.Label(export_frame, text="📤 Export Configuration:", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        ttk.Button(export_frame, text="💾 Export to File", 
                  command=self._export_config).grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(export_frame, text="📋 Copy to Clipboard", 
                  command=self._copy_config).grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Import section
        ttk.Label(export_frame, text="📥 Import Configuration:", 
                 font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", pady=(20,5))
        
        ttk.Button(export_frame, text="📁 Import from File", 
                  command=self._import_config).grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(export_frame, text="📋 Paste from Clipboard", 
                  command=self._paste_config).grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        # Reset section
        ttk.Label(export_frame, text="🔄 Reset Configuration:", 
                 font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", pady=(20,5))
        
        ttk.Button(export_frame, text="🔄 Reset to Defaults", 
                  command=self._reset_config).grid(row=5, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(export_frame, text="🗑️ Clear All Settings", 
                  command=self._clear_config).grid(row=5, column=1, pady=5, padx=5, sticky="ew")
        
        export_frame.grid_columnconfigure(0, weight=1)
        export_frame.grid_columnconfigure(1, weight=1)
    
    def _run_auto_detection(self):
        """Run auto-detection and display results"""
        # Clear previous results
        for item in self.detection_tree.get_children():
            self.detection_tree.delete(item)
        
        # Show progress in summary area
        self.summary_stats.config(text="⏳ Arama yapılıyor, lütfen bekleyin...", foreground="orange")
        self.root.update()
        
        # Run detection
        self.detection_tree.insert("", tk.END, values=("⏳", "Arama", "Araç tespiti başlatılıyor...", "⏳", ""))
        self.root.update()
        
        detected = self.detect_tools()
        
        # Clear loading message
        for item in self.detection_tree.get_children():
            self.detection_tree.delete(item)
        
        # Display results
        for category, tools in detected.items():
            if tools:
                # Add category header
                self.detection_tree.insert("", tk.END, values=(
                    f"📂 {category.title()}", "", "", "", ""
                ))
                
                for tool_name, tool_path, verified in tools:
                    status = "✅ Doğrulandı" if verified else "⚠️ Bulundu"
                    version = self.config.get(category, {}).get(tool_name, {}).get("version", "Bilinmiyor")
                    
                    self.detection_tree.insert("", tk.END, values=(
                        f"  🔧 {tool_name}", category, tool_path, status, version
                    ))
        
        # Save configuration after detection
        self.save_configuration()
        
        # Save detected tools to persistent storage
        if detected:
            self.save_detected_tools(detected)
            self.logger.info("💾 Tespit sonuçları persistent storage'a kaydedildi")
            
            # Update manual configuration tab if tool_listbox exists
            if hasattr(self, 'tool_listbox'):
                self._update_tool_list()
                self.logger.info("🔄 Manual configuration tab updated")
        
        # Count detected tools
        total_tools = 0
        verified_tools = 0
        found_tools = 0
        categories_found = []
        
        for category, tools in detected.items():
            if tools:
                categories_found.append(category.title())
                for tool_name, tool_path, verified in tools:
                    total_tools += 1
                    if verified:
                        verified_tools += 1
                    else:
                        found_tools += 1
        
        # Update summary stats in compact format
        if total_tools > 0:
            summary_text = f"{verified_tools}/{total_tools} araç"
            self.summary_stats.config(text=summary_text, foreground="green")
            
            if hasattr(self, 'status_info'):
                self.status_info.config(text="Tespit OK")
        else:
            self.summary_stats.config(text="0 araç", foreground="red")
            if hasattr(self, 'status_info'):
                self.status_info.config(text="Bulunamadı")
        
        # Create detailed message
        if total_tools > 0:
            message = f"🔍 Araç Tespiti Tamamlandı!\n\n"
            message += f"📊 SONUÇLAR:\n"
            message += f"   ✅ Doğrulanmış araçlar: {verified_tools}\n"
            message += f"   ⚠️ Bulunan araçlar: {found_tools}\n"
            message += f"   📦 Toplam: {total_tools} araç\n\n"
            
            if categories_found:
                message += f"📂 BULUNAN KATEGORİLER:\n"
                for cat in categories_found:
                    message += f"   • {cat}\n"
                message += f"\n"
            
            message += f"💾 Yapılandırma kaydedildi:\n{self.config_file}"
        else:
            message = f"🔍 Araç Tespiti Tamamlandı!\n\n"
            message += f"❌ Hiçbir geliştirme aracı bulunamadı.\n\n"
            message += f"💡 Öneriler:\n"
            message += f"   • 64TASS, ACME, DASM gibi assembler'ları yükleyin\n"
            message += f"   • Python, Node.js gibi dilleri PATH'e ekleyin\n"
            message += f"   • VICE emulator'ünü kurun\n\n"
            message += f"💾 Yapılandırma kaydedildi:\n{self.config_file}"
        
        messagebox.showinfo("Tespit Tamamlandı", message)
    
    def _update_tool_list(self):
        """Update tool list based on selected category - includes detected tools"""
        category = self.category_var.get()
        self.tool_listbox.delete(0, tk.END)
        
        # Combine tools from config and detected tools
        all_tools = {}
        
        # Add tools from main config
        if category in self.config:
            for tool_name, tool_info in self.config[category].items():
                all_tools[tool_name] = tool_info
        
        # Add/update with detected tools
        detected_tools = self.detected_tools_data.get("tools", {})
        if category in detected_tools:
            for tool_name, tool_info in detected_tools[category].items():
                all_tools[tool_name] = tool_info
        
        # Display combined tool list
        for tool_name, tool_info in all_tools.items():
            enabled = "✅" if tool_info.get("enabled", False) else "❌"
            verified = "🔍" if tool_info.get("verified", False) else "❓"
            path_status = "📁" if tool_info.get("path") and os.path.exists(tool_info.get("path", "")) else "💥"
            self.tool_listbox.insert(tk.END, f"{enabled}{verified}{path_status} {tool_name}")
        
        # Add info if no tools found
        if not all_tools:
            self.tool_listbox.insert(tk.END, "❌ Bu kategoride araç bulunamadı")
            self.tool_listbox.insert(tk.END, "💡 Auto Detection sekmesinden araç tespiti yapın")
    
    def _on_tool_select(self, event):
        """Handle tool selection - works with detected tools"""
        selection = self.tool_listbox.curselection()
        if selection:
            selected_text = self.tool_listbox.get(selection[0])
            
            # Skip info messages
            if selected_text.startswith("❌") or selected_text.startswith("💡"):
                return
            
            tool_name = selected_text.split()[-1]  # Get tool name (last word)
            category = self.category_var.get()
            
            # Look for tool in config first, then in detected tools
            tool_config = None
            
            if category in self.config and tool_name in self.config[category]:
                tool_config = self.config[category][tool_name]
            elif category in self.detected_tools_data.get("tools", {}) and tool_name in self.detected_tools_data["tools"][category]:
                tool_config = self.detected_tools_data["tools"][category][tool_name]
            
            if tool_config:
                self.path_var.set(tool_config.get("path", ""))
                self.version_var.set(tool_config.get("version", ""))
                self.enabled_var.set(tool_config.get("enabled", False))
                self.verified_var.set(tool_config.get("verified", False))
            else:
                # Clear fields if tool not found
                self.path_var.set("")
                self.version_var.set("")
                self.enabled_var.set(False)
                self.verified_var.set(False)
    
    def _refresh_manual_tools(self):
        """Refresh manual tools list with latest detected tools"""
        # Reload detected tools data
        self.detected_tools_data = self.load_detected_tools()
        
        # Update tool list display
        self._update_tool_list()
        
        # Show info message
        total_tools = 0
        for category, tools in self.detected_tools_data.get("tools", {}).items():
            total_tools += len(tools)
        
        messagebox.showinfo("Refresh Complete", 
                          f"🔄 Tool list refreshed!\n"
                          f"📦 Total tools available: {total_tools}\n"
                          f"📅 Last detection: {self.detected_tools_data.get('last_detection', 'Never')}")
    
    def _add_new_tool(self):
        """Add new tool dialog"""
        category = self.category_var.get()
        category_name = {
            "assemblers": "🔧 Assembler",
            "compilers": "⚡ Compiler", 
            "interpreters": "🐍 Interpreter",
            "ides": "💻 IDE",
            "emulators": "🎮 Emulator"
        }.get(category, "Tool")
        
        # Create add tool dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"➕ Add New {category_name}")
        dialog.geometry("500x400")
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.LabelFrame(main_frame, text=f"📝 New {category_name} Configuration")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text=f"Adding new tool to: {category_name}s", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        # Form fields
        form_frame = ttk.LabelFrame(main_frame, text="🔧 Tool Information")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Tool name
        ttk.Label(form_frame, text="Tool Name:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        tool_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=tool_name_var, width=40).grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        description_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=description_var, width=40).grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Tool path
        ttk.Label(form_frame, text="Tool Path:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        tool_path_var = tk.StringVar()
        path_frame = ttk.Frame(form_frame)
        path_frame.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        ttk.Entry(path_frame, textvariable=tool_path_var, width=35).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="📁", width=3, 
                  command=lambda: self._browse_file_for_dialog(tool_path_var)).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        priority_var = tk.StringVar(value="2")
        priority_combo = ttk.Combobox(form_frame, textvariable=priority_var, width=37, state="readonly")
        priority_combo['values'] = ("1 - High Priority", "2 - Normal Priority", "3 - Low Priority", "4 - Very Low Priority")
        priority_combo.set("2 - Normal Priority")
        priority_combo.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        # Verification commands
        ttk.Label(form_frame, text="Verify Commands:").grid(row=4, column=0, sticky="nw", pady=5, padx=5)
        verify_frame = ttk.Frame(form_frame)
        verify_frame.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        
        verify_vars = []
        common_verifies = ["--version", "--help", "-V", "-h", "/?"]
        for i, cmd in enumerate(common_verifies):
            var = tk.BooleanVar()
            if cmd in ["--version", "--help"]:  # Default selections
                var.set(True)
            verify_vars.append((cmd, var))
            ttk.Checkbutton(verify_frame, text=cmd, variable=var).grid(row=i//3, column=i%3, sticky="w", padx=5)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Left side - verify button
        ttk.Button(button_frame, text="🔍 Verify Tool", 
                  command=lambda: self._verify_new_tool(tool_path_var.get(), verify_vars, dialog)).pack(side=tk.LEFT)
        
        # Right side - action buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        ttk.Button(right_buttons, text="💾 Add Tool", 
                  command=lambda: self._save_new_tool(category, tool_name_var.get(), description_var.get(), 
                                                    tool_path_var.get(), int(priority_var.get()[0]), 
                                                    verify_vars, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(right_buttons, text="❌ Cancel", 
                  command=dialog.destroy).pack(side=tk.LEFT)
    
    def _browse_file_for_dialog(self, path_var):
        """Browse for executable file in dialog"""
        filetypes = [("Executable files", "*.exe"), ("JAR files", "*.jar"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(
            title="Select Tool Executable",
            filetypes=filetypes
        )
        if filename:
            path_var.set(filename)
    
    def _verify_new_tool(self, tool_path, verify_vars, dialog):
        """Verify new tool functionality"""
        if not tool_path or not os.path.exists(tool_path):
            messagebox.showerror("Error", "❌ Please select a valid tool path first!")
            return
        
        # Get selected verification commands
        verify_commands = [cmd for cmd, var in verify_vars if var.get()]
        if not verify_commands:
            # If no verification commands selected, just check if file exists and is executable
            messagebox.showinfo("Verification Results", 
                              f"🔍 Tool Verification Results:\n\n"
                              f"✅ File exists: {tool_path}\n"
                              f"📁 File size: {os.path.getsize(tool_path)} bytes\n"
                              f"💡 No verification commands selected - tool will be added without verification")
            return
        
        # Try verification commands
        verification_results = []
        for cmd in verify_commands:
            try:
                if tool_path.endswith('.jar'):
                    full_cmd = ['java', '-jar', tool_path] + ([cmd] if cmd != tool_path else [])
                else:
                    full_cmd = [tool_path, cmd]
                
                self.logger.info(f"🔍 Testing: {' '.join(full_cmd)}")
                result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 or "version" in result.stdout.lower() or "help" in result.stdout.lower():
                    verification_results.append(f"✅ {cmd}: SUCCESS")
                    if result.stdout.strip():
                        # Try to extract version
                        lines = result.stdout.strip().split('\n')
                        if lines:
                            verification_results.append(f"   📋 Output: {lines[0][:50]}...")
                else:
                    verification_results.append(f"⚠️ {cmd}: No output (but tool may still work)")
                    
            except subprocess.TimeoutExpired:
                verification_results.append(f"⏱️ {cmd}: Timeout (tool may be interactive)")
            except Exception as e:
                verification_results.append(f"❌ {cmd}: Error ({str(e)[:30]}...)")
        
        # Show results
        result_text = "\n".join(verification_results)
        messagebox.showinfo("Verification Results", 
                          f"🔍 Tool Verification Results:\n\n{result_text}\n\n"
                          f"💡 Note: Tool can be added regardless of verification results")
    
    def _save_new_tool(self, category, tool_name, description, tool_path, priority, verify_vars, dialog):
        """Save new tool to configuration"""
        # Validate inputs
        if not tool_name.strip():
            messagebox.showerror("Error", "❌ Please enter a tool name!")
            return
        if not tool_path.strip():
            messagebox.showerror("Error", "❌ Please select a tool path!")
            return
        if not os.path.exists(tool_path):
            messagebox.showerror("Error", "❌ Tool path does not exist!")
            return
        
        # Get selected verification commands (opsiyonel)
        verify_commands = [cmd for cmd, var in verify_vars if var.get()]
        if not verify_commands:
            verify_commands = ["--help"]  # Default fallback, but not required to work
        
        # Create tool entry
        tool_entry = {
            "patterns": [os.path.basename(tool_path)],
            "description": description.strip() or f"{tool_name} Tool",
            "priority": priority,
            "verification": verify_commands,
            "source": "manual"
        }
        
        # Add to detected tools
        if category not in self.detected_tools_data["tools"]:
            self.detected_tools_data["tools"][category] = {}
        
        self.detected_tools_data["tools"][category][tool_name.lower()] = {
            "path": tool_path,
            "verified": False,  # Will be verified after save
            "enabled": True,
            "version": "",
            "detection_date": datetime.datetime.now().isoformat(),
            "category": category,
            "source": "manual"
        }
        
        # Update main config too
        if category not in self.config:
            self.config[category] = {}
        
        self.config[category][tool_name.lower()] = tool_entry
        
        # Save both configurations
        try:
            # Save main config
            self.save_configuration()
            
            # Save detected tools
            with open(self.detected_tools_file, 'w', encoding='utf-8') as f:
                json.dump(self.detected_tools_data, f, indent=2, ensure_ascii=False)
            
            # Close dialog
            dialog.destroy()
            
            # Refresh tool list
            self._update_tool_list()
            
            # Show success and offer verification
            result = messagebox.askyesno("Tool Added", 
                                       f"✅ {tool_name} added successfully!\n\n"
                                       f"📁 Category: {category}\n"
                                       f"📂 Path: {tool_path}\n\n"
                                       f"🔍 Would you like to verify the tool now?")
            
            if result:
                # Auto-verify the new tool
                self._verify_and_learn_tool(tool_name.lower(), category)
            
            self.logger.info(f"✅ New tool added: {tool_name} in {category}")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save tool:\n{str(e)}")
            self.logger.error(f"❌ Failed to save new tool: {e}")
    
    def _verify_and_learn_tool(self, tool_name, category):
        """Verify and learn about a specific tool - version is optional"""
        try:
            tools_data = self.detected_tools_data.get("tools", {}).get(category, {})
            if tool_name not in tools_data:
                return
            
            tool_info = tools_data[tool_name]
            tool_path = tool_info.get("path", "")
            
            if not tool_path or not os.path.exists(tool_path):
                return
            
            # Get verification commands from config
            tool_config = self.config.get(category, {}).get(tool_name, {})
            verify_commands = tool_config.get("verification", ["--help"])
            
            verified = False
            version_info = ""
            working_command = None
            
            # Try verification - more forgiving approach
            for cmd in verify_commands:
                try:
                    if tool_path.endswith('.jar'):
                        full_cmd = ['java', '-jar', tool_path] + ([cmd] if cmd != tool_path else [])
                    else:
                        full_cmd = [tool_path, cmd]
                    
                    result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)
                    
                    # More lenient verification - even error output can be useful
                    if (result.returncode == 0 or 
                        "version" in result.stdout.lower() or 
                        "help" in result.stdout.lower() or
                        "usage" in result.stdout.lower() or
                        result.stdout.strip() or  # Any output is good
                        result.stderr.strip()):   # Even error output means tool responds
                        
                        verified = True
                        working_command = cmd
                        
                        # Try to extract version info from stdout or stderr
                        output_text = result.stdout.strip() or result.stderr.strip()
                        if output_text:
                            # Look for version patterns
                            lines = output_text.split('\n')
                            for line in lines:
                                if any(word in line.lower() for word in ['version', 'ver.', 'v.', 'build']):
                                    version_info = line.strip()[:100]
                                    break
                            
                            # If no version found, use first meaningful line
                            if not version_info and lines:
                                for line in lines:
                                    if line.strip() and len(line.strip()) > 3:
                                        version_info = line.strip()[:100]
                                        break
                        break
                        
                except subprocess.TimeoutExpired:
                    # Timeout might mean interactive tool - that's still verification
                    verified = True
                    working_command = cmd
                    version_info = "Interactive tool (timeout)"
                    break
                except Exception:
                    continue
            
            # Update tool info - even if version not found, mark as verified if tool responded
            self.detected_tools_data["tools"][category][tool_name]["verified"] = verified
            if version_info:
                self.detected_tools_data["tools"][category][tool_name]["version"] = version_info
            else:
                # Set a generic "available" status if no version found but tool works
                if verified:
                    self.detected_tools_data["tools"][category][tool_name]["version"] = "Available"
            
            # Save updated data
            with open(self.detected_tools_file, 'w', encoding='utf-8') as f:
                json.dump(self.detected_tools_data, f, indent=2, ensure_ascii=False)
            
            # Learn tool usage (help commands) - even if version not found
            if verified:
                self.learn_tool_usage(tool_name, tool_path, category)
            
            # Show result
            if verified:
                status = "✅ Verified and Working"
                details = f"🔧 Working command: {working_command}\n🏷️ Info: {version_info or 'Tool responds but no version info'}"
            else:
                status = "⚠️ Tool found but not responding"
                details = f"💡 Tool exists at path but verification commands failed\nTool may still be usable manually"
            
            messagebox.showinfo("Verification Complete", 
                              f"🔍 Tool verification complete!\n\n"
                              f"🔧 Tool: {tool_name}\n"
                              f"📊 Status: {status}\n"
                              f"{details}")
            
        except Exception as e:
            self.logger.error(f"❌ Verification failed for {tool_name}: {e}")
            # Don't show error to user - tool can still be added
    
    def _browse_tool_path(self):
        """Browse for tool executable"""
        filetypes = [("Executable files", "*.exe"), ("JAR files", "*.jar"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select Tool Executable", filetypes=filetypes)
        if filename:
            self.path_var.set(filename)
    
    def _verify_current_tool(self):
        """Verify currently selected tool"""
        selection = self.tool_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a tool to verify.")
            return
        
        selected_text = self.tool_listbox.get(selection[0])
        tool_name = selected_text.split()[-1]
        tool_path = self.path_var.get()
        
        if not tool_path:
            messagebox.showwarning("No Path", "Please specify a path for the tool.")
            return
        
        verified = self._verify_tool(tool_path, tool_name)
        self.verified_var.set(verified)
        
        status = "✅ Tool verified successfully!" if verified else "❌ Tool verification failed!"
        messagebox.showinfo("Verification Result", status)
    
    def _save_current_tool(self):
        """Save current tool configuration to both config and detected tools"""
        selection = self.tool_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a tool to save.")
            return
        
        selected_text = self.tool_listbox.get(selection[0])
        
        # Skip info messages
        if selected_text.startswith("❌") or selected_text.startswith("💡"):
            return
        
        tool_name = selected_text.split()[-1]
        category = self.category_var.get()
        
        # Prepare tool configuration
        tool_config = {
            "path": self.path_var.get(),
            "version": self.version_var.get(),
            "enabled": self.enabled_var.get(),
            "verified": self.verified_var.get()
        }
        
        # Save to main config
        if category not in self.config:
            self.config[category] = {}
        self.config[category][tool_name] = tool_config.copy()
        
        # Save to detected tools if it exists there
        if (category in self.detected_tools_data.get("tools", {}) and 
            tool_name in self.detected_tools_data["tools"][category]):
            
            self.detected_tools_data["tools"][category][tool_name].update({
                "path": self.path_var.get(),
                "enabled": self.enabled_var.get(),
                "verified": self.verified_var.get(),
                "version": self.version_var.get()
            })
            
            # Save detected tools file
            try:
                with open(self.detected_tools_file, 'w', encoding='utf-8') as f:
                    json.dump(self.detected_tools_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                self.logger.error(f"Failed to save detected tools: {e}")
        
        # Save main configuration
        self.save_configuration()
        
        # Update tool list display
        self._update_tool_list()
        
        messagebox.showinfo("Saved", f"✅ Configuration saved for {tool_name}\n"
                                   f"📁 Path: {self.path_var.get()}\n"
                                   f"✅ Enabled: {self.enabled_var.get()}\n"
                                   f"🔍 Verified: {self.verified_var.get()}")
    
    def _delete_current_tool(self):
        """Delete selected tool from configuration"""
        # Get current selection
        selection = self.tool_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "❌ Please select a tool to delete!")
            return
        
        tool_name = self.tool_listbox.get(selection[0])
        category = self.category_var.get()
        
        # Confirm deletion
        result = messagebox.askyesno("Delete Tool", 
                                   f"⚠️ Are you sure you want to delete this tool?\n\n"
                                   f"🔧 Tool: {tool_name}\n"
                                   f"📂 Category: {category}\n"
                                   f"📁 Path: {self.path_var.get()}\n\n"
                                   f"❗ This action cannot be undone!")
        
        if not result:
            return
        
        try:
            deleted_from = []
            
            # Remove from main config
            if category in self.config and tool_name in self.config[category]:
                del self.config[category][tool_name]
                deleted_from.append("main configuration")
                
                # Clean up empty categories
                if not self.config[category]:
                    del self.config[category]
            
            # Remove from detected tools
            if (category in self.detected_tools_data.get("tools", {}) and 
                tool_name in self.detected_tools_data["tools"][category]):
                
                del self.detected_tools_data["tools"][category][tool_name]
                deleted_from.append("detected tools")
                
                # Clean up empty categories
                if not self.detected_tools_data["tools"][category]:
                    del self.detected_tools_data["tools"][category]
                
                # Save detected tools file
                with open(self.detected_tools_file, 'w', encoding='utf-8') as f:
                    json.dump(self.detected_tools_data, f, indent=2, ensure_ascii=False)
            
            # Remove from tool usage data if exists
            if "tool_usage" in self.detected_tools_data:
                for usage_type in ["command_templates", "help_info", "usage_examples"]:
                    if usage_type in self.detected_tools_data["tool_usage"]:
                        self.detected_tools_data["tool_usage"][usage_type].pop(tool_name, None)
            
            # Save main configuration
            self.save_configuration()
            
            # Clear current selection fields
            self.path_var.set("")
            self.version_var.set("")
            self.enabled_var.set(False)
            self.verified_var.set(False)
            
            # Update tool list display
            self._update_tool_list()
            
            # Show success message
            locations = " and ".join(deleted_from) if deleted_from else "configuration"
            messagebox.showinfo("Deleted", 
                              f"✅ Tool deleted successfully!\n\n"
                              f"🔧 Tool: {tool_name}\n"
                              f"📂 Category: {category}\n"
                              f"📁 Removed from: {locations}\n\n"
                              f"🔄 Tool list has been refreshed")
            
            self.logger.info(f"✅ Tool deleted: {tool_name} from {category}")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to delete tool:\n{str(e)}")
            self.logger.error(f"❌ Failed to delete tool {tool_name}: {e}")
    
    def _save_preferences(self, *args):
        """Save preferences automatically"""
        self.config["preferences"]["default_assembler"] = self.default_assembler_var.get()
        self.config["preferences"]["default_language"] = self.default_language_var.get()
        self.config["preferences"]["output_format"] = self.output_format_var.get()
        self.config["preferences"]["theme"] = self.theme_var.get()
        self.config["preferences"]["auto_detect"] = self.auto_detect_var.get()
    
    def _export_config(self):
        """Export configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Export Complete", f"Configuration exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export configuration:\n{e}")
    
    def _copy_config(self):
        """Copy configuration to clipboard"""
        try:
            config_text = json.dumps(self.config, indent=2, ensure_ascii=False)
            self.root.clipboard_clear()
            self.root.clipboard_append(config_text)
            messagebox.showinfo("Copied", "Configuration copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy configuration:\n{e}")
    
    def _import_config(self):
        """Import configuration from file"""
        filename = filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)
                self._deep_merge(self.config, imported_config)
                self._update_tool_list()
                messagebox.showinfo("Import Complete", "Configuration imported successfully!")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import configuration:\n{e}")
    
    def _paste_config(self):
        """Paste configuration from clipboard"""
        try:
            config_text = self.root.clipboard_get()
            imported_config = json.loads(config_text)
            self._deep_merge(self.config, imported_config)
            self._update_tool_list()
            messagebox.showinfo("Paste Complete", "Configuration pasted successfully!")
        except Exception as e:
            messagebox.showerror("Paste Error", f"Failed to paste configuration:\n{e}")
    
    def _reset_config(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Reset Configuration", 
                              "Are you sure you want to reset all settings to defaults?\n"
                              "This will overwrite your current configuration."):
            self.config = self.default_config.copy()
            self._update_tool_list()
            messagebox.showinfo("Reset Complete", "Configuration reset to defaults!")
    
    def _clear_config(self):
        """Clear all configuration"""
        if messagebox.askyesno("Clear Configuration", 
                              "Are you sure you want to clear ALL settings?\n"
                              "This will remove all tool paths and preferences."):
            # Clear all tool configurations but keep structure
            for category in self.config:
                if isinstance(self.config[category], dict):
                    for tool in self.config[category]:
                        if isinstance(self.config[category][tool], dict):
                            self.config[category][tool] = {
                                "path": "", "version": "", "enabled": False, "verified": False
                            }
            self._update_tool_list()
            messagebox.showinfo("Clear Complete", "All settings cleared!")
    
    def _browse_custom_search_dir(self):
        """Browse for custom search directory"""
        directory = filedialog.askdirectory(
            title="Arama Dizini Seçin",
            initialdir=os.path.expanduser("~")
        )
        if directory:
            self.custom_search_var.set(directory)
    
    def _add_custom_search_dir(self):
        """Add custom search directory to list"""
        directory = self.custom_search_var.get().strip()
        if directory and os.path.exists(directory):
            if directory not in self.custom_search_dirs:
                self.custom_search_dirs.append(directory)
                self._update_custom_dirs_display()
                self.custom_search_var.set("")  # Clear input
                messagebox.showinfo("Dizin Eklendi", f"📁 Arama dizini eklendi:\n{directory}")
            else:
                messagebox.showwarning("Zaten Var", "Bu dizin zaten arama listesinde mevcut.")
        elif directory:
            messagebox.showerror("Hata", f"Dizin bulunamadı:\n{directory}")
        else:
            messagebox.showwarning("Boş Dizin", "Lütfen geçerli bir dizin yolu girin.")
    
    def _remove_custom_search_dir(self, directory):
        """Remove custom search directory from list"""
        if directory in self.custom_search_dirs:
            self.custom_search_dirs.remove(directory)
            self._update_custom_dirs_display()
            messagebox.showinfo("Dizin Kaldırıldı", f"📁 Arama dizini kaldırıldı:\n{directory}")
    
    def _update_custom_dirs_display(self):
        """Update the display of custom search directories"""
        # Clear existing display
        for widget in self.custom_dirs_frame.winfo_children():
            widget.destroy()
        
        if self.custom_search_dirs:
            # Header
            header_label = ttk.Label(self.custom_dirs_frame, 
                                   text=f"📁 Ek Arama Dizinleri ({len(self.custom_search_dirs)}):",
                                   font=("Arial", 9, "bold"))
            header_label.pack(anchor=tk.W, pady=(5, 2))
            
            # Directory list
            for i, directory in enumerate(self.custom_search_dirs):
                dir_frame = ttk.Frame(self.custom_dirs_frame)
                dir_frame.pack(fill=tk.X, pady=1)
                
                # Directory path
                dir_label = ttk.Label(dir_frame, text=f"   {i+1}. {directory}", 
                                    font=("Arial", 8), foreground="blue")
                dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Remove button
                remove_btn = ttk.Button(dir_frame, text="❌", width=3,
                                      command=lambda d=directory: self._remove_custom_search_dir(d))
                remove_btn.pack(side=tk.RIGHT, padx=2)

    def _create_tree_context_menu(self):
        """Create context menu for tree items"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="🔍 Test Tool", command=self._test_selected_tool)
        self.context_menu.add_command(label="✅ Enable Tool", command=self._enable_selected_tool)
        self.context_menu.add_command(label="❌ Disable Tool", command=self._disable_selected_tool)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📁 Show in Explorer", command=self._show_tool_in_explorer)
        self.context_menu.add_command(label="📋 Copy Path", command=self._copy_tool_path)
        
        # Bind right-click to tree
        self.detection_tree.bind("<Button-3>", self._show_context_menu)
        
    def _show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.detection_tree.identify_row(event.y)
        if item:
            self.detection_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _refresh_detection_results(self):
        """Refresh detection results"""
        self.status_label.config(text="🔄 Tespit sonuçları yenileniyor...")
        self.root.update()
        
        # Clear current results
        for item in self.detection_tree.get_children():
            self.detection_tree.delete(item)
        
        # Re-run detection
        self._run_auto_detection()
    
    def _show_detection_summary(self):
        """Show detailed detection summary"""
        available_tools = self.get_available_tools()
        
        summary = "🔍 DETECTED TOOLS SUMMARY\n"
        summary += "=" * 50 + "\n\n"
        
        total_tools = 0
        for category, tools in available_tools.items():
            if tools:
                summary += f"📂 {category.upper()}:\n"
                for tool_name, tool_info in tools.items():
                    status = "✅" if tool_info.get("verified") else "⚠️"
                    summary += f"   {status} {tool_name}: {tool_info.get('path', 'N/A')}\n"
                    total_tools += 1
                summary += "\n"
        
        if total_tools == 0:
            summary += "❌ No tools detected yet.\n"
            summary += "💡 Run auto-detection first.\n"
        else:
            summary += f"📊 Total: {total_tools} tools available\n"
            summary += f"📁 Storage: {self.detected_tools_file}\n"
        
        messagebox.showinfo("Detection Summary", summary)
    
    def _learn_selected_tools(self):
        """Learn usage for all detected tools"""
        available_tools = self.get_available_tools()
        
        if not any(available_tools.values()):
            messagebox.showwarning("No Tools", "No tools available for learning.\nRun auto-detection first.")
            return
        
        # Ask user for confirmation
        total_tools = sum(len(tools) for tools in available_tools.values())
        if not messagebox.askyesno("Learn Tool Usage", 
                                  f"Bu işlem {total_tools} aracın kullanım bilgilerini öğrenecek.\n"
                                  f"Her araç için help komutları çalıştırılacak.\n\n"
                                  f"Devam etmek istiyor musunuz?"):
            return
        
        # Create progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("📚 Learning Tool Usage")
        progress_window.geometry("400x200")
        progress_window.transient(self.root)
        
        progress_label = ttk.Label(progress_window, text="Initializing...")
        progress_label.pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_window, mode='determinate', maximum=total_tools)
        progress_bar.pack(pady=10, padx=20, fill=tk.X)
        
        log_text = tk.Text(progress_window, height=6, width=50)
        log_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        progress_window.update()
        
        # Learn each tool
        current_tool = 0
        learned_tools = []
        
        for category, tools in available_tools.items():
            for tool_name, tool_info in tools.items():
                current_tool += 1
                
                progress_label.config(text=f"Learning: {tool_name} ({current_tool}/{total_tools})")
                progress_bar.config(value=current_tool)
                log_text.insert(tk.END, f"📚 Learning {tool_name}...\n")
                log_text.see(tk.END)
                progress_window.update()
                
                try:
                    usage_info = self.learn_tool_usage(tool_name, tool_info["path"], category)
                    if usage_info:
                        learned_tools.append(tool_name)
                        log_text.insert(tk.END, f"✅ {tool_name} learned successfully\n")
                    else:
                        log_text.insert(tk.END, f"⚠️ {tool_name} learning failed\n")
                except Exception as e:
                    log_text.insert(tk.END, f"❌ {tool_name} error: {str(e)[:50]}...\n")
                
                log_text.see(tk.END)
                progress_window.update()
        
        # Save learned data
        with open(self.detected_tools_file, 'w', encoding='utf-8') as f:
            json.dump(self.detected_tools_data, f, indent=2, ensure_ascii=False)
        
        # Show completion
        progress_label.config(text=f"✅ Learning completed!")
        log_text.insert(tk.END, f"\n📚 Learning completed: {len(learned_tools)}/{total_tools} tools\n")
        log_text.insert(tk.END, f"💾 Usage data saved to: {self.detected_tools_file}\n")
        log_text.see(tk.END)
        
        # Auto close after 3 seconds
        progress_window.after(3000, progress_window.destroy)
    
    def _test_selected_tool(self):
        """Test a selected tool from the detection tree"""
        selection = self.detection_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a tool from the list to test.")
            return
        
        item = self.detection_tree.item(selection[0])
        values = item['values']
        
        if len(values) < 3 or not values[0].strip().startswith('🔧'):
            messagebox.showwarning("Invalid Selection", "Please select a tool (not a category) to test.")
            return
        
        tool_name = values[0].replace('🔧', '').strip()
        tool_path = values[2]
        category = values[1]
        
        # Test window
        test_window = tk.Toplevel(self.root)
        test_window.title(f"🚀 Test Tool: {tool_name}")
        test_window.geometry("600x400")
        test_window.transient(self.root)
        
        # Tool info
        info_frame = ttk.LabelFrame(test_window, text="Tool Information")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text=f"Name: {tool_name}").pack(anchor=tk.W, padx=5)
        ttk.Label(info_frame, text=f"Path: {tool_path}").pack(anchor=tk.W, padx=5)
        ttk.Label(info_frame, text=f"Category: {category}").pack(anchor=tk.W, padx=5)
        
        # Command templates
        cmd_frame = ttk.LabelFrame(test_window, text="Command Templates")
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Get available templates
        templates = self.detected_tools_data.get("tool_usage", {}).get("command_templates", {}).get(tool_name, [])
        if not templates:
            # Generate basic templates
            self._generate_command_templates(tool_name, {})
            templates = self.detected_tools_data.get("tool_usage", {}).get("command_templates", {}).get(tool_name, [])
        
        selected_template = tk.StringVar()
        if templates:
            selected_template.set(templates[0])
            
        template_combo = ttk.Combobox(cmd_frame, textvariable=selected_template, values=templates, width=70)
        template_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Variables frame
        var_frame = ttk.LabelFrame(test_window, text="Variables")
        var_frame.pack(fill=tk.X, padx=10, pady=5)
        
        variables = {}
        var_entries = {}
        
        # Common variables
        common_vars = [
            ("Input File (%DOSYAADI%)", "input_filename", "test.asm"),
            ("Output File (%CIKTI%)", "output_filename", "output.prg"),
            ("Working Dir (%YOL%)", "working_directory", os.getcwd())
        ]
        
        for i, (label, var_key, default) in enumerate(common_vars):
            ttk.Label(var_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry_var = tk.StringVar(value=default)
            entry = ttk.Entry(var_frame, textvariable=entry_var, width=40)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
            var_entries[var_key] = entry_var
        
        var_frame.grid_columnconfigure(1, weight=1)
        
        # Output frame
        output_frame = ttk.LabelFrame(test_window, text="Execution Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        output_text = tk.Text(output_frame, height=10, wrap=tk.WORD)
        output_scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
        output_text.configure(yscrollcommand=output_scrollbar.set)
        
        output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(test_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def execute_test():
            template = selected_template.get()
            if not template:
                output_text.insert(tk.END, "❌ No command template selected\n")
                return
            
            # Prepare variables
            test_vars = {}
            for var_key, entry_var in var_entries.items():
                test_vars[var_key] = entry_var.get()
            
            output_text.insert(tk.END, f"🚀 Executing: {tool_name}\n")
            output_text.insert(tk.END, f"Template: {template}\n")
            output_text.insert(tk.END, "=" * 50 + "\n")
            output_text.see(tk.END)
            test_window.update()
            
            # Execute
            result = self.execute_tool_command(tool_name, template, test_vars)
            
            if result:
                output_text.insert(tk.END, f"Command: {result['command']}\n")
                output_text.insert(tk.END, f"Return Code: {result['returncode']}\n\n")
                
                if result['stdout']:
                    output_text.insert(tk.END, "STDOUT:\n")
                    output_text.insert(tk.END, result['stdout'])
                    output_text.insert(tk.END, "\n\n")
                
                if result['stderr']:
                    output_text.insert(tk.END, "STDERR:\n")
                    output_text.insert(tk.END, result['stderr'])
                    output_text.insert(tk.END, "\n\n")
                
                output_text.insert(tk.END, f"📁 Log saved: {result['log_file']}\n")
            else:
                output_text.insert(tk.END, "❌ Execution failed\n")
            
            output_text.see(tk.END)
        
        ttk.Button(btn_frame, text="🚀 Execute", command=execute_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📚 Learn Usage", 
                  command=lambda: self.learn_tool_usage(tool_name, tool_path, category)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Close", command=test_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _save_detected_tools(self):
        """Save current detection results"""
        # Get current detection results from tree
        detected = {
            "assemblers": [],
            "compilers": [],
            "interpreters": [],
            "ides": [],
            "emulators": [],
            "utilities": []
        }
        
        for item in self.detection_tree.get_children():
            values = self.detection_tree.item(item)['values']
            
            if len(values) >= 4 and values[0].strip().startswith('🔧'):
                tool_name = values[0].replace('🔧', '').strip()
                category = values[1]
                tool_path = values[2]
                verified = values[3] == "✅ Doğrulandı"
                
                if category in detected:
                    detected[category].append((tool_name, tool_path, verified))
        
        if any(detected.values()):
            self.save_detected_tools(detected)
            messagebox.showinfo("Saved", "Detected tools saved to persistent storage!")
        else:
            messagebox.showwarning("No Data", "No detection data to save. Run auto-detection first.")
    
    def _refresh_detection_results(self):
        """Refresh detection results display"""
        # Clear current display
        for item in self.detection_tree.get_children():
            self.detection_tree.delete(item)
        
        # Load from persistent storage
        available_tools = self.get_available_tools()
        
        for category, tools in available_tools.items():
            if tools:
                # Add category header
                self.detection_tree.insert("", tk.END, values=(
                    f"📂 {category.title()}", "", "", "", ""
                ))
                
                for tool_name, tool_info in tools.items():
                    status = "✅ Doğrulandı" if tool_info.get("verified") else "⚠️ Bulundu"
                    version = tool_info.get("version", "Bilinmiyor")
                    
                    self.detection_tree.insert("", tk.END, values=(
                        f"  🔧 {tool_name}", category, tool_info["path"], status, version
                    ))
        
        # Update summary
        total_tools = sum(len(tools) for tools in available_tools.values())
        if total_tools > 0:
            self.summary_stats.config(text=f"✅ Loaded: {total_tools} tools from storage", foreground="green")
        else:
            self.summary_stats.config(text="❌ No tools in storage", foreground="red")
        """Show detailed summary of detection results"""
        detected = self.detect_tools()
        
        # Count tools
        total_tools = 0
        verified_tools = 0
        categories_found = []
        tool_details = []
        
        for category, tools in detected.items():
            if tools:
                categories_found.append(category.title())
                for tool_name, tool_path, verified in tools:
                    total_tools += 1
                    if verified:
                        verified_tools += 1
                    tool_details.append((category, tool_name, tool_path, verified))
        
        # Create summary window
        summary_window = tk.Toplevel(self.root)
        summary_window.title("📊 Tespit Özet Raporu")
        summary_window.geometry("600x500")
        summary_window.resizable(True, True)
        
        # Header
        header_label = ttk.Label(summary_window, 
                                text="📊 Araç Tespit Özet Raporu",
                                font=("Arial", 14, "bold"))
        header_label.pack(pady=10)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(summary_window, text="📈 İstatistikler")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats_text = f"🔧 Toplam araç: {total_tools}\n"
        stats_text += f"✅ Doğrulanmış: {verified_tools}\n"
        stats_text += f"⚠️ Bulunan: {total_tools - verified_tools}\n"
        stats_text += f"📂 Kategori sayısı: {len(categories_found)}"
        
        ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT).pack(pady=10, padx=10)
        
        # Categories frame
        if categories_found:
            cat_frame = ttk.LabelFrame(summary_window, text="📂 Bulunan Kategoriler")
            cat_frame.pack(fill=tk.X, padx=10, pady=5)
            
            cat_text = " • ".join(categories_found)
            ttk.Label(cat_frame, text=cat_text, wraplength=550, justify=tk.LEFT).pack(pady=10, padx=10)
        
        # Tools list frame
        tools_frame = ttk.LabelFrame(summary_window, text="🔧 Tespit Edilen Araçlar")
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(tools_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Populate text widget
        for category, tool_name, tool_path, verified in tool_details:
            status = "✅ Doğrulandı" if verified else "⚠️ Bulundu"
            text_widget.insert(tk.END, f"🔧 {tool_name} ({category.title()})\n")
            text_widget.insert(tk.END, f"   📁 {tool_path}\n")
            text_widget.insert(tk.END, f"   {status}\n\n")
        
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Close button
        ttk.Button(summary_window, text="❌ Kapat", 
                  command=summary_window.destroy).pack(pady=10)
    
    def _save_detected_tools(self):
        """Save currently detected tools to configuration"""
        try:
            self.save_configuration()
            detected_count = len([item for item in self.detection_tree.get_children() 
                                if not item.startswith("📂")])
            messagebox.showinfo("Kayıt Başarılı", 
                               f"✅ {detected_count} araç yapılandırması kaydedildi!\n\n"
                               f"📁 Dosya: {self.config_file}")
        except Exception as e:
            messagebox.showerror("Kayıt Hatası", f"❌ Ayarlar kaydedilemedi:\n{e}")
    
    def _test_selected_tool(self):
        """Test selected tool functionality"""
        selection = self.detection_tree.selection()
        if not selection:
            messagebox.showwarning("Seçim Yok", "Lütfen test edilecek bir araç seçin.")
            return
        
        item = selection[0]
        values = self.detection_tree.item(item, 'values')
        
        if len(values) >= 3 and values[2]:  # Has path
            tool_path = values[2]
            tool_name = values[0].replace("  🔧 ", "").replace("📂 ", "")
            
            # Test tool by running it with version flag
            test_result = self._verify_tool(tool_path, tool_name)
            
            result_msg = f"✅ {tool_name} test başarılı!" if test_result else f"❌ {tool_name} test başarısız!"
            messagebox.showinfo("Test Sonucu", result_msg)
        else:
            messagebox.showwarning("Test Edilemez", "Seçilen öğe test edilebilir bir araç değil.")
    
    def _enable_selected_tool(self):
        """Enable selected tool"""
        self._toggle_tool_status(True)
    
    def _disable_selected_tool(self):
        """Disable selected tool"""
        self._toggle_tool_status(False)
    
    def _toggle_tool_status(self, enabled):
        """Toggle tool enabled status"""
        selection = self.detection_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.detection_tree.item(item, 'values')
        
        if len(values) >= 2:
            tool_name = values[0].replace("  🔧 ", "").replace("📂 ", "")
            category = values[1]
            
            if category in self.config and tool_name in self.config[category]:
                self.config[category][tool_name]["enabled"] = enabled
                status_text = "aktif" if enabled else "pasif"
                messagebox.showinfo("Durum Değişti", f"🔧 {tool_name} artık {status_text}")
                
                # Refresh the display
                self._refresh_detection_results()
    
    def _show_tool_in_explorer(self):
        """Show selected tool in file explorer"""
        selection = self.detection_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.detection_tree.item(item, 'values')
        
        if len(values) >= 3 and values[2]:  # Has path
            tool_path = Path(values[2])
            if tool_path.exists():
                try:
                    if platform.system() == "Windows":
                        subprocess.run(f'explorer /select,"{tool_path}"', shell=True)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", "-R", str(tool_path)])
                    else:  # Linux
                        subprocess.run(["xdg-open", str(tool_path.parent)])
                except Exception as e:
                    messagebox.showerror("Explorer Hatası", f"Dosya gezgini açılamadı:\n{e}")
            else:
                messagebox.showwarning("Dosya Bulunamadı", "Araç dosyası artık mevcut değil.")
    
    def _copy_tool_path(self):
        """Copy selected tool path to clipboard"""
        selection = self.detection_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.detection_tree.item(item, 'values')
        
        if len(values) >= 3 and values[2]:  # Has path
            self.root.clipboard_clear()
            self.root.clipboard_append(values[2])
            messagebox.showinfo("Kopyalandı", f"📋 Dosya yolu panoya kopyalandı:\n{values[2]}")

    def _reload_configuration(self):
        """Reload configuration from file"""
        self.config = self.load_configuration()
        self._update_tool_list()
        messagebox.showinfo("Reload Complete", "Configuration reloaded from file!")
    
    def _launch_main_gui(self):
        """Launch main GUI with current configuration"""
        self.save_configuration()
        
        # Set environment variables for main GUI
        os.environ['GUI_THEME'] = self.config["preferences"]["theme"]
        os.environ['DEFAULT_ASSEMBLER'] = self.config["preferences"]["default_assembler"]
        os.environ['DEFAULT_LANGUAGE'] = self.config["preferences"]["default_language"]
        
        try:
            # Close configuration manager
            self.root.destroy()
            
            # Launch main GUI
            from gui_manager import D64ConverterGUI
            import tkinter as tk
            
            root = tk.Tk()
            app = D64ConverterGUI(root)
            root.mainloop()
            
        except ImportError as e:
            messagebox.showerror("Launch Error", 
                                f"Failed to launch main GUI:\n{e}\n\n"
                                f"Make sure gui_manager.py exists and is accessible.")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Unexpected error launching GUI:\n{e}")
    
    def run(self):
        """Run the configuration manager"""
        self.create_configuration_gui()
        
        # Check if we have previously detected tools
        has_detected_tools = (self.detected_tools_data.get("tools") and 
                             any(tools for tools in self.detected_tools_data["tools"].values()))
        
        # Only auto-detect if no previous results exist AND auto_detect is enabled
        if (self.config["preferences"]["auto_detect"] and not has_detected_tools):
            self.logger.info("🔍 Kaydedilmiş araç bulunamadı, otomatik tespit başlatılıyor...")
            self.root.after(1000, self._run_auto_detection)  # Run after 1 second
        elif has_detected_tools:
            self.logger.info("✅ Kaydedilmiş araçlar bulundu, otomatik tespit atlanıyor...")
            # Load and display existing results
            self.root.after(500, self._load_existing_results)
        
        self.root.mainloop()
    
    def _load_existing_results(self):
        """Load and display existing detection results"""
        try:
            # Clear the tree first
            for item in self.detection_tree.get_children():
                self.detection_tree.delete(item)
            
            total_tools = 0
            verified_tools = 0
            
            # Display tools from detected_tools.json
            for category, tools in self.detected_tools_data.get("tools", {}).items():
                for tool_name, tool_info in tools.items():
                    if isinstance(tool_info, dict) and "path" in tool_info:
                        total_tools += 1
                        if tool_info.get("verified", False):
                            verified_tools += 1
                            status = "✅ Doğrulandı"
                        else:
                            status = "❌ Bulunamadı"
                        
                        # Insert into tree
                        self.detection_tree.insert("", "end", values=(
                            tool_name,
                            category.capitalize(),
                            tool_info.get("path", ""),
                            status,
                            tool_info.get("version", "")
                        ))
            
            # Update summary with compact format
            last_detection = self.detected_tools_data.get("last_detection", "")
            if last_detection:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_detection.replace('Z', '+00:00'))
                    last_detection = dt.strftime("%d.%m %H:%M")
                except:
                    last_detection = "Bilinmiyor"
            else:
                last_detection = "Yok"
            
            summary_text = f"{verified_tools}/{total_tools} araç"
            self.summary_stats.config(text=summary_text)
            
            status_text = f"Son: {last_detection}"
            if hasattr(self, 'status_info'):
                self.status_info.config(text=status_text)
            
            self.logger.info(f"✅ Kaydedilmiş tespit sonuçları görüntülendi: {verified_tools}/{total_tools} araç")
            
        except Exception as e:
            self.logger.error(f"❌ Kaydedilmiş sonuçlar yüklenemedi: {e}")
            self.summary_stats.config(text="❌ Kaydedilmiş sonuçlar yüklenemedi")

def main():
    """Main entry point for configuration manager"""
    config_manager = ConfigurationManager()
    config_manager.run()

if __name__ == "__main__":
    main()
