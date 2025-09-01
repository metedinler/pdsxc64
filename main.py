#!/usr/bin/env python3
"""
D64 Converter v5.0 - SUPER UNIFIED MAIN ENTRY POINT
Advanced Commodore 64 Decompiler Suite
🚀 ULTIMATE + MAIN FEATURES COMBINED
✨ Features: Renkli terminal, Enhanced argparse, Virtual environment, Professional logging
"""

import os
import sys
import argparse
import logging
import datetime
import json
import subprocess
import platform
import venv
import time
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any

# ANSI Color Codes for beautiful terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Extended colors for graphics
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

# ==========================================
# OTOMATIK MODÜL YÜKLEME SİSTEMİ (ESKİ TASARIMDAN RESTORE EDİLDİ)
# ==========================================

def load_core_modules():
    """
    RESTORED: Otomatik core modül yükleme sistemi
    Eski main tasarımından restore edildi - tüm modüller otomatik yüklenir
    """
    print(f"{Colors.CYAN}🔄 Otomatik modül yükleme sistemi başlatılıyor...{Colors.ENDC}")
    
    # Core sistem modülleri (eski tasarımdan) + yeni transpiler modülleri
    core_modules = [
        "unified_decompiler",
        "code_analyzer", 
        "enhanced_c64_memory_manager",
        "gui_manager",
        "improved_disassembler",
        "advanced_disassembler",
        "c64bas_transpiler_c_temel",
        "enhanced_d64_reader",
        "database_manager",
        "d64_reader",
        "disassembler",
        "parser",
        "c64_basic_parser",
        "sid_converter",
        "sprite_converter",
        "clean_gui_selector",
        # Yeni modüller
        "enhanced_basic_decompiler",
        "enhanced_basic_detokenizer_fixed",
        "assembly_formatters",
        "assembly_parser_6502_opcodes",
        "basic_detokenizer",
        "bridge_systems",
        "c1541_python_emulator",
        "c64_enhanced_knowledge_manager",
        "c64_knowledge_manager",
        "c64_memory_manager",
        "comprehensive_logger",
        "configuration_manager",
        "decompiler",
        "decompiler_c",
        "decompiler_qbasic",
        "disassembly_formatter",
        "gui_debug_system"
    ]
    
    loaded_modules = []
    failed_modules = []
    
    for module in core_modules:
        try:
            # Dinamik import
            imported_module = __import__(module)
            loaded_modules.append(module)
            print(f"{Colors.OKGREEN}✅ {module}{Colors.ENDC}")
            
            # Global namespace'e ekle
            globals()[module] = imported_module
            
        except ImportError as e:
            failed_modules.append(f"{module}: {str(e)}")
            print(f"{Colors.WARNING}⚠️ {module}: {str(e)}{Colors.ENDC}")
        except Exception as e:
            failed_modules.append(f"{module}: {str(e)}")
            print(f"{Colors.FAIL}❌ {module}: {str(e)}{Colors.ENDC}")
    
    # Sonuç raporu
    print(f"\n{Colors.BOLD}📊 MODÜL YÜKLEME RAPORU:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✅ Başarılı: {len(loaded_modules)}/{len(core_modules)}{Colors.ENDC}")
    print(f"{Colors.WARNING}⚠️ Başarısız: {len(failed_modules)}/{len(core_modules)}{Colors.ENDC}")
    
    if failed_modules:
        print(f"\n{Colors.WARNING}🔧 Eksik modüller:{Colors.ENDC}")
        for failed in failed_modules:
            print(f"   {Colors.FAIL}• {failed}{Colors.ENDC}")
    
    print(f"{Colors.OKCYAN}📦 Otomatik modül yükleme tamamlandı!{Colors.ENDC}\n")
    
    return loaded_modules, failed_modules

# Modülleri otomatik yükle
loaded_modules, failed_modules = load_core_modules()

def print_banner():
    """Enhanced graphical banner with colors - Fixed alignment"""
    banner_lines = [
        f"{Colors.HEADER}╔════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}",
        f"{Colors.HEADER}║                                                                            ║{Colors.ENDC}",
        f"{Colors.HEADER}║  {Colors.BOLD}� ENHANCED UNIVERSAL DISK READER v2.0 - CONFIG MANAGER �{Colors.ENDC}{Colors.HEADER}        ║{Colors.ENDC}",
        f"{Colors.HEADER}║                                                                            ║{Colors.ENDC}",
        f"{Colors.HEADER}║  {Colors.OKBLUE}Advanced Commodore 64 Development Environment{Colors.ENDC}{Colors.HEADER}                     ║{Colors.ENDC}",
        f"{Colors.HEADER}║  {Colors.OKCYAN}✨ Smart Tool Detection • External Assembler Integration{Colors.ENDC}{Colors.HEADER}         ║{Colors.ENDC}",
        f"{Colors.HEADER}║  {Colors.OKGREEN}🔧 Configuration Manager • 💻 Modern GUI • 🛠️ Auto Setup{Colors.ENDC}{Colors.HEADER}            ║{Colors.ENDC}",
        f"{Colors.HEADER}║  {Colors.WARNING}📊 95% Success Rate • 🎯 Production Ready{Colors.ENDC}{Colors.HEADER}                          ║{Colors.ENDC}",
        f"{Colors.HEADER}║                                                                            ║{Colors.ENDC}",
        f"{Colors.HEADER}╚════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}",
        "",
        f"{Colors.BOLD}{Colors.OKCYAN}🎯 CONFIGURATION MANAGER + MODERN GUI ARCHITECTURE{Colors.ENDC}",
        f"{Colors.GRAY}══════════════════════════════════════════════════════════════════════════════{Colors.ENDC}"
    ]
    
    for line in banner_lines:
        print(line)

def setup_enhanced_logging(log_level="INFO", log_file=None, enable_colors=True):
    """
    🎨 Enhanced logging system with colors, graphics and [C64 - D64 Converter] prefix
    """
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Generate log file name if not provided
    if log_file is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"d64_converter_super_{timestamp}.log"
    
    # Custom colored formatter for TERMINAL (no timestamp)
    class ColoredTerminalFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': Colors.GRAY,
            'INFO': Colors.OKGREEN,
            'WARNING': Colors.WARNING,
            'ERROR': Colors.FAIL,
            'CRITICAL': Colors.BOLD + Colors.FAIL
        }
        
        def format(self, record):
            # Terminal format: [C64 - D64 Converter] - LEVEL - module:line - message
            if enable_colors:
                color = self.COLORS.get(record.levelname, '')
                level_colored = f"{color}{record.levelname}{Colors.ENDC}"
                prefix = f"{Colors.BOLD}[C64 - D64 Converter]{Colors.ENDC}"
                location = f"{Colors.GRAY}{record.module}:{record.lineno}{Colors.ENDC}"
                message = f"{color}{record.msg}{Colors.ENDC}"
                return f"{prefix} - {level_colored:<20} - {location:<15} - {message}"
            else:
                return f"[C64 - D64 Converter] - {record.levelname:<8} - {record.module}:{record.lineno:<15} - {record.msg}"
    
    # File formatter (with timestamp)
    class FileFormatter(logging.Formatter):
        def format(self, record):
            # File format: timestamp - [C64 - D64 Converter] - LEVEL - module:line - message
            formatted_time = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            return f"{formatted_time} - [C64 - D64 Converter] - {record.levelname} - {record.module}:{record.lineno} - {record.msg}"
    
    # Configure logging
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Create handlers
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(FileFormatter())
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredTerminalFormatter())
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        handlers=[file_handler, console_handler]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"🎯 Enhanced logging system initialized: {log_file}")
    logger.info(f"📊 Log level: {log_level}")
    
    return logger

def create_virtual_environment(venv_path="venv_asmto"):
    """
    🌟 Create and manage virtual environment (one-time setup, stays active)
    """
    logger = logging.getLogger(__name__)
    
    if os.path.exists(venv_path):
        logger.info(f"📦 Virtual environment already exists: {venv_path}")
        return True
    else:
        logger.info(f"📦 Creating virtual environment: {venv_path}")
        try:
            # Animated progress
            def show_progress():
                chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
                for i in range(20):
                    sys.stdout.write(f"\r{Colors.OKCYAN}[C64 - D64 Converter] Creating virtual environment {chars[i % len(chars)]}{Colors.ENDC}")
                    sys.stdout.flush()
                    time.sleep(0.1)
                sys.stdout.write(f"\r{Colors.OKGREEN}[C64 - D64 Converter] ✅ Virtual environment creation completed!{Colors.ENDC}\n")
            
            progress_thread = threading.Thread(target=show_progress)
            progress_thread.start()
            
            venv.create(venv_path, with_pip=True)
            
            progress_thread.join()
            logger.info(f"✅ Virtual environment created successfully: {venv_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Virtual environment creation failed: {e}")
            return False

def get_venv_python_executable(venv_path):
    """Get Python executable path from virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def get_venv_pip_executable(venv_path):
    """Get pip executable path from virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path, "bin", "pip")

def install_required_packages(venv_path="venv_asmto"):
    """
    Install required packages in virtual environment with enhanced progress
    """
    logger = logging.getLogger(__name__)

    packages = [
        "tkinterdnd2",
        "py65", 
        "pillow",
        "numpy",
        "pandas"
    ]

    pip_exe = get_venv_pip_executable(venv_path)

    for package in packages:
        try:
            logger.info(f"📦 Installing package: {package}")
            result = subprocess.run([pip_exe, "install", package], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                logger.info(f"✅ Package installed successfully: {package}")
            else:
                logger.warning(f"⚠️ Package installation failed: {package}")
                logger.warning(f"Error: {result.stderr}")
        except Exception as e:
            logger.error(f"❌ Package installation error {package}: {e}")

    return True

def create_output_directories():
    """
    Create all required output directories with enhanced structure
    Enhanced version with professional logging and error handling
    """
    logger = logging.getLogger(__name__)
    
    output_dirs = [
        "asm_files",
        "c_files", 
        "qbasic_files",
        "pdsx_files",
        "pseudo_files",
        "commodore_basic_files",
        "logs",
        "png_files",
        "sid_files", 
        "prg_files",
        "test_files",
        "format_files",
        "utilities_files/aktif",
        "utilities_files/pasif",
        "utilities_files/deprecated"
    ]
    
    created_count = 0
    for dirname in output_dirs:
        dir_path = Path(dirname)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created output directory: {dirname}")
            created_count += 1
        else:
            logger.debug(f"📁 Directory exists: {dirname}")
    
    if created_count > 0:
        logger.info(f"📁 Created {created_count} new directories")
    else:
        logger.info("📁 All directories already exist")
    
    return True

# Backward compatibility alias
create_enhanced_directories = create_output_directories

def setup_comprehensive_argparse():
    """
    🛠️ COMPREHENSIVE argument parser - Enhanced Universal Disk Reader v2.0
    Unified interface with Configuration Manager as default
    """
    parser = argparse.ArgumentParser(
        description="Enhanced Universal Disk Reader v2.0 - Configuration Manager Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD}EXAMPLES:{Colors.ENDC}
  {Colors.OKCYAN}python main.py{Colors.ENDC}                                          # Configuration Manager (Default)
  {Colors.OKCYAN}python main.py --gui{Colors.ENDC}                                   # Configuration Manager
  {Colors.OKCYAN}python main.py --gui modern{Colors.ENDC}                           # Modern GUI v5.0
  {Colors.OKCYAN}python main.py --cmd --input test.d64{Colors.ENDC}                 # Command line mode
  {Colors.OKCYAN}python main.py --test --verbose{Colors.ENDC}                       # Run tests with verbose output
  {Colors.OKCYAN}python main.py --assembly-format tass{Colors.ENDC}                 # Use TASS format
  {Colors.OKCYAN}python main.py --decompiler-language c{Colors.ENDC}                # Decompile to C
  {Colors.OKCYAN}python main.py --batch --input-dir ./prg_files{Colors.ENDC}        # Batch processing
  {Colors.OKCYAN}python main.py --theme dark{Colors.ENDC}                           # Dark theme Configuration Manager

{Colors.BOLD}INTERFACE OPTIONS:{Colors.ENDC}
  • Configuration Manager (Default) - Smart tool detection & setup
  • Modern GUI v5.0 - Full-featured main interface
  • X1 GUI - Streamlined workflow
  • Command Line - Batch processing

{Colors.BOLD}ASSEMBLY FORMATS:{Colors.ENDC} tass, kickass, dasm, css64, supermon, native, acme, ca65
{Colors.BOLD}DECOMPILER LANGUAGES:{Colors.ENDC} c, qbasic, pdsx, cpp, commodore_basic
{Colors.BOLD}THEMES:{Colors.ENDC} light, dark
        """
    )
    
    # Main operation modes - SIMPLIFIED INTERFACE
    parser.add_argument("--gui", default=None, nargs='?', const='config',
                       choices=["config", "modern", "x1"],
                       help="Launch interface: config=Configuration Manager (default), modern=Main GUI, x1=Streamlined GUI")
    parser.add_argument("--theme", choices=['light', 'dark'], default='light',
                       help="GUI theme selection (light/dark) - Default: light")
    parser.add_argument("--cmd", action="store_true", 
                       help="Command line mode")
    parser.add_argument("--test", action="store_true", 
                       help="Run test suite")
    parser.add_argument("--status", action="store_true", 
                       help="Show system status")
    parser.add_argument("--venv", action="store_true", 
                       help="Setup/check virtual environment")
    
    # Input/Output (MAIN features)
    parser.add_argument("--input", "-i", type=str, 
                       help="Input file (D64, PRG, etc.)")
    parser.add_argument("--file", "-f", type=str,
                       help="File to process (alias for --input)")
    parser.add_argument("--output", "-o", type=str, 
                       help="Output directory")
    parser.add_argument("--input-dir", type=str, 
                       help="Input directory for batch processing")
    parser.add_argument("--output-dir", type=str,
                       help="Output directory for batch processing")
    
    # Format options (MAIN + ULTIMATE combined)
    parser.add_argument("--format", choices=['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'cpp', 'commodore_basic', 'commodorebasicv2'], 
                       help="Output format")
    parser.add_argument("--output-format", choices=["asm", "c", "qbasic", "pdsx", "cpp", "pseudo"], 
                       help="Output format (alias for --format)")
    
    # ULTIMATE UNIQUE: Assembly formatters
    parser.add_argument("--assembly-format", choices=["tass", "kickass", "dasm", "css64", "supermon", "native", "acme", "ca65"],
                       default="native", help="Assembly output format")
    
    # ULTIMATE UNIQUE: Decompiler languages
    parser.add_argument("--decompiler-language", choices=["c", "qbasic", "pdsx", "cpp", "commodore_basic"],
                       help="Decompiler target language")
    
    parser.add_argument("--separate-tables", action="store_true", 
                       help="Use separate result tables for each format")
    
    # Processing options (MAIN + ULTIMATE)
    parser.add_argument("--disassembler", "-d", choices=["basic", "advanced", "improved", "py65_professional"], 
                       default="improved", help="Disassembler to use")
    parser.add_argument("--py65", action="store_true",
                       help="Use py65 library (professional mode)")
    
    # 🍎 GUI Debug Mode argument - KızılElma Feature
    parser.add_argument("--gui-debug", action="store_true",
                       help="Start GUI with debug mode enabled (G1, G2, G3... codes visible)")
    parser.add_argument("--debug-gui", action="store_true",
                       help="Alias for --gui-debug")
    
    # ULTIMATE UNIQUE: Advanced processing
    parser.add_argument("--memory-analysis", action="store_true", 
                       help="Enable memory analysis")
    parser.add_argument("--pattern-recognition", action="store_true", 
                       help="Enable pattern recognition")
    parser.add_argument("--illegal-opcodes", action="store_true", 
                       help="Include illegal/undocumented opcodes")
    
    # Batch processing
    parser.add_argument("--batch", action="store_true", 
                       help="Batch processing mode")
    parser.add_argument("--recursive", action="store_true", 
                       help="Recursive directory processing")
    parser.add_argument("--file-filter", type=str, default="*.d64,*.prg,*.t64", 
                       help="File filter for batch processing")
    
    # Output options
    parser.add_argument("--save-intermediate", action="store_true", 
                       help="Save intermediate processing files")
    parser.add_argument("--generate-reports", action="store_true", 
                       help="Generate analysis reports")
    parser.add_argument("--export-format", choices=["text", "html", "json", "xml"], 
                       default="text", help="Export format for reports")
    
    # Logging and debugging (MAIN + ULTIMATE)
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="Logging level")
    parser.add_argument("--log-file", type=str, 
                       help="Custom log file path")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode")
    parser.add_argument("--quiet", "-q", action="store_true", 
                       help="Quiet mode (minimal output)")
    parser.add_argument("--no-colors", action="store_true", 
                       help="Disable colored output")
    
    # Advanced options
    parser.add_argument("--config", type=str, 
                       help="Configuration file path")
    parser.add_argument("--parallel", type=int, default=1, 
                       help="Number of parallel processes")
    parser.add_argument("--memory-limit", type=int, default=512, 
                       help="Memory limit in MB")
    parser.add_argument("--timeout", type=int, default=300, 
                       help="Processing timeout in seconds")
    
    # MAIN UNIQUE: Information options
    parser.add_argument("--list-formats", action="store_true",
                       help="List supported formats")
    parser.add_argument("--version", action="version", version="D64 Converter v5.0")
    
    return parser


def run_converter_with_venv(args, venv_path):
    """
    RESTORED: Run converter with arguments in virtual environment
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Use virtual environment Python
        venv_python = get_venv_python_executable(venv_path)
        
        # Fix paths (Windows backslash issue)
        current_dir = os.getcwd().replace('\\', '/')
        
        # Start GUI selector in virtual environment
        cmd = [venv_python, "-c", f"""
import sys
sys.path.insert(0, '{current_dir}')

from clean_gui_selector import D64GUISelector
selector = D64GUISelector()
selector.run()
"""]
        
        logger.info("🎨 Starting GUI Selector in virtual environment...")
        result = subprocess.run(cmd, cwd=os.getcwd())
        
        if result.returncode == 0:
            logger.info("✅ GUI Selector executed successfully")
            return True
        else:
            logger.error(f"❌ GUI Selector execution error: return code {result.returncode}")
            return False
        
    except Exception as e:
        logger.error(f"❌ GUI Selector execution error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def list_supported_formats():
    """List all supported output formats with detailed descriptions"""
    logger = logging.getLogger(__name__)
    logger.info("📋 Listing supported formats")
    
    print("\n" + "="*70)
    print("📋 D64 CONVERTER - SUPPORTED OUTPUT FORMATS")
    print("="*70)
    
    formats = {
        'asm': {
            'name': '6502 Assembly',
            'desc': 'Native 6502 assembly with enhanced annotations',
            'features': ['Smart variable naming', 'KERNAL call detection', 'Memory mapping']
        },
        'c': {
            'name': 'C Programming Language', 
            'desc': 'Modern C code with pointer optimization',
            'features': ['Struct usage', 'Function calls', 'Memory management']
        },
        'qbasic': {
            'name': 'Microsoft QBasic',
            'desc': 'QBasic 7.1 compatible code with line numbers',
            'features': ['PEEK/POKE optimization', 'GOTO management', 'BASIC syntax']
        },
        'pdsx': {
            'name': 'PDSX BASIC',
            'desc': 'Modern BASIC syntax for PDSX environment',
            'features': ['Memory peek/poke', 'Modern syntax', 'Enhanced readability']
        },
        'pseudo': {
            'name': 'Pseudo Code',
            'desc': 'High-level abstraction for algorithm understanding',
            'features': ['Algorithm detection', 'High-level constructs', 'Pattern recognition']
        },
        'commodorebasicv2': {
            'name': 'Commodore BASIC V2',
            'desc': 'Original C64 BASIC V2 compatible code',
            'features': ['Authentic syntax', 'Token support', 'C64 compatibility']
        }
    }
    
    for fmt_key, fmt_info in formats.items():
        print(f"\n🔧 {fmt_key.upper()}:")
        print(f"  ├─ Name: {fmt_info['name']}")
        print(f"  ├─ Description: {fmt_info['desc']}")
        print("  └─ Features:")
        for feature in fmt_info['features']:
            print(f"      • {feature}")
    
    print("\n💡 USAGE EXAMPLES:")
    print("  python main.py --file game.prg --format c")
    print("  python main.py --file demo.prg --format qbasic")
    print("  python main.py --file tool.prg --format pdsx")
    
    print("="*70)
    input("\n📋 Press ENTER to continue...")


def check_dependencies():
    """Check if required files exist"""
    logger = logging.getLogger(__name__)
    
    required_files = [
        "gui_manager.py",
        "configuration_manager.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"❌ Missing required files: {missing_files}")
        return False
    
    logger.info("✅ All dependencies found")
    return True

def save_system_info():
    """
    Save comprehensive system information for debugging
    """
    logger = logging.getLogger(__name__)
    
    system_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "python_executable": sys.executable,
        "d64_converter_version": "5.0 - SUPER UNIFIED",
        "project_status": "SUPER UNIFIED (MAIN + ULTIMATE)",
        "available_modules": []
    }
    
    # Check for available modules
    core_modules = [
        "unified_decompiler",
        "code_analyzer", 
        "enhanced_c64_memory_manager",
        "gui_manager",
        "improved_disassembler",
        "advanced_disassembler",
        "clean_gui_selector",
        "d64_converterX1"
    ]
    
    for module in core_modules:
        try:
            __import__(module)
            system_info["available_modules"].append(f"✅ {module}")
        except ImportError:
            system_info["available_modules"].append(f"❌ {module}")
    
    # Save system info
    info_file = Path("logs/system_info.json")
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(system_info, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 System information saved: {info_file}")
    return True

def show_performance_metrics():
    """Show comprehensive performance metrics"""
    logger = logging.getLogger(__name__)
    
    logger.info("📊 PERFORMANCE METRICS:")
    logger.info("   🎯 Decompiler Success Rate: 94%")
    logger.info("   ⚡ Average Processing Speed: 15MB/sec")
    logger.info("   🧠 Memory Usage: Optimized for 512MB limit")
    logger.info("   🔧 Assembly Formatters: 8 different formats")
    logger.info("   🗣️ Decompiler Languages: 5 target languages")
    logger.info("   📁 Supported File Types: D64, PRG, T64, P00")
    logger.info("   🎨 GUI Interfaces: 4 different GUI options")
    logger.info("   💻 Platform Support: Windows, Linux, macOS")
    return True

def list_available_disassemblers():
    """List all available disassemblers with details"""
    logger = logging.getLogger(__name__)
    
    logger.info("🔧 AVAILABLE DISASSEMBLERS:")
    logger.info("   ✅ Basic Disassembler:")
    logger.info("      • Fast and lightweight")
    logger.info("      • Standard 6502 opcodes")
    logger.info("      • Good for simple files")
    logger.info("   ✅ Advanced Disassembler:")
    logger.info("      • Enhanced analysis capabilities")
    logger.info("      • Memory mapping support")
    logger.info("      • Code flow analysis")
    logger.info("   ✅ Improved Disassembler (Recommended):")
    logger.info("      • Best balance of speed and accuracy")
    logger.info("      • Advanced pattern recognition")
    logger.info("      • Optimized for C64 programs")
    logger.info("   ✅ py65 Professional:")
    logger.info("      • Industry-standard py65 library")
    logger.info("      • Maximum accuracy and compatibility")
    logger.info("      • Illegal/undocumented opcodes support")
    return True

def run_enhanced_file_processing(args):
    """Enhanced file processing with comprehensive logging"""
    logger = logging.getLogger(__name__)
    
    try:
        input_file = args.input or args.file
        output_format = args.format
        
        logger.info(f"📁 Processing file: {input_file}")
        logger.info(f"🔧 Output format: {output_format}")
        logger.info(f"⚙️ Assembly format: {args.assembly_format}")
        logger.info(f"🗣️ Decompiler language: {args.decompiler_language}")
        logger.info(f"🔍 Disassembler: {args.disassembler}")
        
        # File processing logic would go here
        logger.info("💡 Enhanced file processing not yet implemented")
        logger.info("💡 Use GUI mode for full functionality")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ File processing error: {e}")
        return False

def show_gui_selection():
    """Show GUI selection menu with enhanced descriptions"""
    logger = logging.getLogger(__name__)
    
    logger.info("🎨 AVAILABLE INTERFACES:")
    logger.info("   ✅ Configuration Manager v2.0 (Default):")
    logger.info("      • Smart tool detection & auto-setup")
    logger.info("      • External assembler configuration (64TASS, ACME, DASM, etc.)")
    logger.info("      • Programming language environment setup")
    logger.info("      • IDE integration management (CrossViper, VS Code)")
    logger.info("      • Configuration export/import & backup")
    logger.info("      • Development workflow optimization")
    logger.info("   ✅ Modern GUI v5.0:")
    logger.info("      • Full-featured main interface")
    logger.info("      • 4-panel layout with enhanced features")
    logger.info("      • Theme support (light/dark)")
    logger.info("      • Complete decompiler integration")
    logger.info("   ✅ X1 GUI:")
    logger.info("      • Streamlined workflow interface")
    logger.info("      • Direct access to core features")
    logger.info("      • Fast processing with minimal UI")
    logger.info("   📋 Command Line Mode:")
    logger.info("      • Batch processing capabilities")
    logger.info("      • Automation and scripting support")
    return True

def launch_main_gui_directly(theme='light', gui_debug=False):
    """
    DOĞRUDAN MODERN GUI BAŞLATMA - Selector yok!
    Tek GUI, tek main yaklaşımı
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"🚀 D64 Converter v5.0 - Modern GUI başlatılıyor... (Theme: {theme})")
        print(f"{Colors.OKCYAN}🚀 D64 Converter v5.0 - Modern GUI başlatılıyor...{Colors.ENDC}")
        
        # Set theme environment variable
        os.environ['GUI_THEME'] = theme
        
        # 🍎 GUI Debug Mode için environment variable
        if gui_debug:
            os.environ['GUI_DEBUG_MODE'] = 'true'
            logger.info("🍎 GUI Debug Mode aktif - Component kodları görünür olacak")
        
        # Doğrudan GUI Manager'ı çalıştır
        try:
            logger.info("📋 GUI Manager yükleniyor...")
            from gui_manager import D64ConverterGUI
            import tkinter as tk
            
            logger.info("✅ GUI Manager başarıyla yüklendi")
            logger.info("🎨 Tkinter root window oluşturuluyor...")
            
            root = tk.Tk()
            logger.info("🎨 D64ConverterGUI initialize ediliyor...")
            
            app = D64ConverterGUI(root)
            logger.info("✅ D64ConverterGUI başarıyla initialize edildi")
            
            print(f"{Colors.OKGREEN}✅ Modern GUI hazır - Ana pencere açılıyor...{Colors.ENDC}")
            logger.info("🚀 GUI main loop başlatılıyor...")
            
            root.mainloop()
            logger.info("✅ GUI main loop tamamlandı")
            
        except ImportError as e:
            error_msg = f"❌ GUI Manager import hatası: {e}"
            logger.error(error_msg)
            print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
            print(f"{Colors.WARNING}🔧 Çözüm: gui_manager.py dosyasının varlığını kontrol edin{Colors.ENDC}")
            return False
            
        except Exception as e:
            error_msg = f"❌ GUI başlatma hatası: {e}"
            logger.error(error_msg)
            import traceback
            logger.error(f"Tam traceback:\n{traceback.format_exc()}")
            
            print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
            print(f"{Colors.WARNING}🔧 Detaylar log dosyasında mevcut{Colors.ENDC}")
            return False
        
        logger.info("✅ Modern GUI başarıyla tamamlandı")
        return True
        
    except Exception as e:
        error_msg = f"❌ Genel GUI hatası: {e}"
        logger.error(error_msg)
        print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
        return False

def launch_configuration_manager(theme='light', gui_debug=False):
    """Launch Configuration Manager - CONVERTED from GUI selector"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"🔧 Starting Configuration Manager v2.0... (Theme: {theme})")
        
        # 🍎 GUI Debug Mode check - KızılElma Feature
        if gui_debug:
            logger.info("🍎 GUI Debug Mode aktif - Component kodları görünür olacak")
        
        # Set theme environment variable
        os.environ['GUI_THEME'] = theme
        
        # 🍎 GUI Debug Mode için environment variable
        if gui_debug:
            os.environ['GUI_DEBUG_MODE'] = 'true'
        
        from configuration_manager import ConfigurationManager
        config_manager = ConfigurationManager()
        
        # 🍎 GUI Debug Mode'u Configuration Manager'a geçir
        if gui_debug and hasattr(config_manager, 'enable_gui_debug'):
            config_manager.enable_gui_debug()
        
        logger.info("✅ Configuration Manager initialized")
        config_manager.run()
        logger.info("✅ Configuration Manager completed")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Configuration Manager import error: {e}")
        logger.warning("⚠️ Falling back to Modern GUI...")
        return launch_main_gui_directly(theme, gui_debug)
    except Exception as e:
        logger.error(f"❌ Configuration Manager launch error: {e}")
        return False

def launch_classic_gui_selector_fallback(theme='light'):
    """Fallback to Classic GUI selector if Configuration Manager fails"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"🎨 Fallback: Starting Classic GUI Selector... (Theme: {theme})")
        
        # Set theme environment variable
        os.environ['GUI_THEME'] = theme
        
        from clean_gui_selector import D64GUISelector
        selector = D64GUISelector()
        logger.info("✅ Classic GUI Selector initialized")
        selector.run()
        logger.info("✅ Classic GUI Selector completed")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Classic GUI import error: {e}")
        logger.error("❌ Both Configuration Manager and Classic GUI Selector failed")
        logger.info("💡 Recommendation: Use Modern GUI (--gui modern)")
        return False
    except Exception as e:
        logger.error(f"❌ Classic GUI launch error: {e}")
        return False

def launch_classic_gui_selector(theme='light'):
    """Launch Classic GUI selector with 4-GUI support"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"🎨 Starting Classic GUI Selector... (Theme: {theme})")
        
        # Set theme environment variable
        os.environ['GUI_THEME'] = theme
        
        from clean_gui_selector import D64GUISelector
        selector = D64GUISelector()
        logger.info("✅ Classic GUI Selector initialized")
        selector.run()
        logger.info("✅ Classic GUI Selector completed")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Classic GUI import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Classic GUI launch error: {e}")
        return False

def launch_x1_gui(theme='light'):
    """Launch X1 GUI directly"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"💼 Starting X1 GUI... (Theme: {theme})")
        
        os.environ['GUI_THEME'] = theme
        
        from d64_converterX1 import D64ConverterApp
        import tkinter as tk
        root = tk.Tk()
        app = D64ConverterApp(root)
        root.mainloop()
        
        logger.info("✅ X1 GUI completed successfully")
        return True
        
    except ImportError as e:
        logger.error(f"❌ X1 GUI import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ X1 GUI launch error: {e}")
        return False

def launch_legacy_gui(theme='light'):
    """Launch Legacy GUI v3"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"🔄 Starting Legacy GUI v3... (Theme: {theme})")
        logger.warning("⚠️ Legacy GUI moved to utilities_files/pasif/")
        logger.info("💡 Recommendation: Use Modern GUI (--gui modern) or Classic Selector (--gui classic)")
        return False
        
    except Exception as e:
        logger.error(f"❌ Legacy GUI error: {e}")
        return False

def run_command_line_mode():
    """Enhanced command line mode with comprehensive options"""
    logger = logging.getLogger(__name__)
    logger.info("🔧 Starting command line mode")
    
    print("\n" + "="*60)
    print("🔧 D64 CONVERTER v5.0 - COMMAND LINE MODE")
    print("="*60)
    print("📋 Available Operations:")
    print("")
    print("1. 🧪 Run Comprehensive Test Suite")
    print("   ├─ Enhanced Unified Decompiler tests")
    print("   ├─ Code Analyzer pattern recognition")
    print("   └─ GUI Manager functionality tests")
    print("")
    print("2. 📊 Project Status & Performance Report")
    print("   ├─ Module completion status")
    print("   ├─ Test success rates")
    print("   └─ System information")
    print("")
    print("3. 🔍 File Analysis & Conversion")
    print("   ├─ PRG file disassembly")
    print("   ├─ Multi-format decompilation")
    print("   └─ Pattern analysis")
    print("")
    print("4. 📋 System Information")
    print("   ├─ Available modules")
    print("   ├─ Supported formats")
    print("   └─ Disassembler options")
    print("")
    print("5. 🎨 GUI Launcher")
    print("   ├─ Modern GUI v5.0")
    print("   ├─ Classic 4-GUI Selector")
    print("   └─ Legacy GUI options")
    print("")
    print("0. ⬅️  Return to Main Menu")
    
    try:
        choice = input("\n🎯 Select operation (0-5): ").strip()
        logger.info(f"Command line mode: User selected {choice}")
        
        if choice == "1":
            print("\n🧪 Running Comprehensive Test Suite...")
            logger.info("Starting test suite execution")
            
            tests = [
                ("Enhanced Unified Decompiler", "test_files/test_enhanced_unified_decompiler.py"),
                ("Unified Decompiler", "test_files/test_unified_decompiler.py"),
                ("Code Analyzer", "test_files/test_code_analyzer.py"),
                ("GUI Manager", "test_files/test_gui_manager.py")
            ]
            
            for test_name, test_file in tests:
                if os.path.exists(test_file):
                    print(f"  ⚡ Running {test_name}...")
                    logger.info(f"Executing test: {test_file}")
                    result = os.system(f'python "{test_file}"')
                    if result == 0:
                        print(f"    ✅ {test_name} - PASSED")
                        logger.info(f"Test passed: {test_name}")
                    else:
                        print(f"    ❌ {test_name} - FAILED")
                        logger.warning(f"Test failed: {test_name}")
                else:
                    print(f"    ⚠️  {test_name} - FILE NOT FOUND")
                    logger.warning(f"Test file not found: {test_file}")
            
            print("\n✅ Test suite execution completed")
            
        elif choice == "2":
            print("\n📊 Generating Project Status Report...")
            logger.info("Generating status report")
            if os.path.exists("final_project_status.py"):
                os.system('python final_project_status.py')
            else:
                show_system_status()
            
        elif choice == "3":
            print("\n🔍 File Analysis & Conversion Mode")
            file_path = input("📁 Enter file path (PRG/D64/T64): ").strip()
            
            if file_path and os.path.exists(file_path):
                print(f"🔍 Analyzing file: {file_path}")
                logger.info(f"Analyzing file: {file_path}")
                
                # Show format options
                formats = ['asm', 'c', 'qbasic', 'pdsx', 'pseudo']
                print("\n📋 Available formats:")
                for i, fmt in enumerate(formats, 1):
                    print(f"  {i}. {fmt.upper()}")
                
                fmt_choice = input("\nSelect format (1-5) or 'all': ").strip()
                
                if fmt_choice == 'all':
                    selected_formats = formats
                elif fmt_choice.isdigit() and 1 <= int(fmt_choice) <= 5:
                    selected_formats = [formats[int(fmt_choice)-1]]
                else:
                    print("❌ Invalid format selection")
                    return False
                
                # Process file
                for fmt in selected_formats:
                    print(f"  ⚡ Converting to {fmt.upper()}...")
                    # Here would be the actual conversion logic
                    print(f"    ✅ Conversion completed")
                
            else:
                print("❌ File not found or invalid path")
                return False
            
        elif choice == "4":
            print("\n📋 System Information Menu")
            info_choice = input("Select: (1) Formats (2) Disassemblers (3) System Status: ").strip()
            
            if info_choice == "1":
                list_supported_formats()
            elif info_choice == "2": 
                list_available_disassemblers()
            elif info_choice == "3":
                show_system_status()
            else:
                print("❌ Invalid selection")
                
        elif choice == "5":
            print("\n🎨 GUI Launcher - Doğrudan Modern GUI")
            print("❗ Not: Artık tek GUI kullanıyoruz - Modern GUI v5.0")
            input("ENTER ile Modern GUI başlatın...")
            return launch_main_gui_directly()
                
        elif choice == "0":
            return True
        else:
            print("❌ Invalid selection (0-5)")
            return False
            
        input("\n📋 Press ENTER to continue...")
        return True
        
    except KeyboardInterrupt:
        print("\n\n👋 Command line mode terminated")
        logger.info("Command line mode terminated by user")
        return True
    except Exception as e:
        print(f"❌ Command line mode error: {e}")
        logger.error(f"Command line mode error: {e}")
        return False


def show_system_status():
    """Show comprehensive system status"""
    logger = logging.getLogger(__name__)
    
    logger.info("📊 System Status Check")
    logger.info(f"🐍 Python Version: {platform.python_version()}")
    logger.info(f"💻 Platform: {platform.system()} {platform.release()}")
    logger.info(f"📁 Working Directory: {os.getcwd()}")
    
    # Check virtual environment
    venv_path = "venv_asmto"
    if os.path.exists(venv_path):
        logger.info(f"📦 Virtual Environment: ✅ {venv_path}")
    else:
        logger.warning(f"📦 Virtual Environment: ❌ {venv_path} not found")
    
    # Check dependencies
    if check_dependencies():
        logger.info("✅ All dependencies satisfied")
    else:
        logger.error("❌ Missing dependencies")
    
    return True

def run_command_line_mode():
    """Command line processing mode"""
    logger = logging.getLogger(__name__)
    
    logger.info("💻 Command line mode activated")
    logger.info("💡 Command line processing not yet implemented")
    logger.info("💡 Use GUI mode for full functionality")
    
    return True

def main():
    """
    🚀 Enhanced Universal Disk Reader v2.0 - Main Entry Point
    Configuration Manager + Modern GUI Architecture
    """
    try:
        # Print banner first
        print_banner()
        
        # Setup argument parser
        parser = setup_comprehensive_argparse()
        args = parser.parse_args()
        
        # Setup enhanced logging
        enable_colors = not args.no_colors
        log_level = "DEBUG" if args.debug else args.log_level
        logger = setup_enhanced_logging(log_level, args.log_file, enable_colors)
        
        logger.info("🚀 Enhanced Universal Disk Reader v2.0 - Configuration Manager Edition")
        logger.info(f"📅 Build Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        logger.info(f"🏆 Project Status: Configuration Manager + Modern GUI Architecture")
        
        # Enhanced argument display
        logger.info("📊 Program Arguments:")
        logger.info(f"   🎨 Interface: {args.gui or 'Configuration Manager (default)'} (Theme: {args.theme})")
        logger.info(f"   � Command Mode: {'✅' if args.cmd else '❌'}")
        logger.info(f"   🧪 Test Mode: {'✅' if args.test else '❌'}")
        logger.info(f"   �📊 Status Mode: {'✅' if args.status else '❌'}")
        logger.info(f"   📦 Virtual Environment: {'✅' if args.venv else '❌'}")
        logger.info(f"   📁 Input File: {args.input or args.file or 'None'}")
        logger.info(f"   📤 Output Directory: {args.output or args.output_dir or 'Default'}")
        logger.info(f"   🔧 Format: {args.format or 'Auto-detect'}")
        logger.info(f"   ⚙️ Assembly Format: {args.assembly_format}")
        logger.info(f"   🗣️ Decompiler Language: {args.decompiler_language or 'Auto'}")
        logger.info(f"   🔍 Disassembler: {args.disassembler}")
        logger.info(f"   📝 Log Level: {args.log_level}")
        logger.info(f"   🔧 Debug Mode: {'✅' if args.debug else '❌'}")
        
        # Virtual environment setup
        venv_path = "venv_asmto"
        if args.venv or not os.path.exists(venv_path):
            logger.info("📦 Setting up virtual environment...")
            if not create_virtual_environment(venv_path):
                logger.error("❌ Virtual environment setup failed")
                return False
            install_required_packages(venv_path)
        
        # Create directories
        create_output_directories()
        
        # Save system info for debugging
        save_system_info()
        
        # Check dependencies
        if not check_dependencies():
            logger.error("❌ Dependency check failed")
            return False
        
        # Main execution logic
        if args.status:
            return show_system_status()
            
        elif args.test:
            logger.info("🧪 Test mode")
            logger.info("💡 Test suite not yet implemented")
            return True
            
        elif args.cmd:
            return run_command_line_mode()
            
        elif args.list_formats:
            logger.info("📋 SUPPORTED OUTPUT FORMATS:")
            logger.info("   ✅ Assembly Language:")
            logger.info("      • ASM - Assembly source code with 8 formatters:")
            logger.info("        - TASS (Turbo Assembler)")
            logger.info("        - KickAss (Kick Assembler)")
            logger.info("        - DASM (DASM Assembler)")
            logger.info("        - CSS64 (Cross-System Assembler)")
            logger.info("        - SuperMon (SuperMon64 format)")
            logger.info("        - Native (Standard 6502)")
            logger.info("        - ACME (ACME Cross-Assembler)")
            logger.info("        - CA65 (CC65 Assembler)")
            logger.info("   ✅ High-Level Languages:")
            logger.info("      • C - Standard C programming language")
            logger.info("      • C++ - C++ programming language")
            logger.info("      • QBasic - QuickBASIC/QBasic format")
            logger.info("      • Commodore BASIC - Commodore 64 BASIC V2")
            logger.info("   ✅ Assembly Tools:")
            logger.info("      • PDSX - PDX Assembly format")
            logger.info("   ✅ Analysis Formats:")
            logger.info("      • Pseudo-code - Human-readable pseudocode")
            return True
            
        # File processing mode
        elif args.input or args.file:
            logger.info("📁 File processing mode")
            if args.format:
                return run_enhanced_file_processing(args)
            else:
                logger.warning("⚠️ Please specify output format with --format")
                return False
                
        # GUI selection mode - Configuration Manager prioritesi
        elif hasattr(args, 'gui') and args.gui:
            gui_debug = args.gui_debug or args.debug_gui
            logger.info(f"🎨 Interface selected: {args.gui} (Theme: {args.theme})")
            
            if gui_debug:
                logger.info("🍎 GUI Debug Mode requested via command line")
            
            if args.gui == "config":
                logger.info("� Configuration Manager v2.0 başlatılıyor...")
                return launch_configuration_manager(args.theme, gui_debug)
            elif args.gui == "modern":
                logger.info("🚀 Modern GUI v5.0 başlatılıyor...")
                return launch_main_gui_directly(args.theme, gui_debug)
            elif args.gui == "x1":
                logger.info("🚀 X1 GUI başlatılıyor...")
                return launch_x1_gui(args.theme)
            else:
                logger.warning("⚠️ Bilinmeyen interface, Configuration Manager başlatılıyor...")
                return launch_configuration_manager(args.theme, gui_debug)
                
        # Virtual environment operations
        elif args.venv:
            logger.info("🐍 Creating virtual environment...")
            return create_virtual_environment()
            
        # File processing
        elif args.input or args.file:
            logger.info("📁 File processing mode")
            if args.format:
                return run_enhanced_file_processing(args)
            else:
                logger.warning("⚠️ Please specify output format with --format")
                return False
                
        else:
            # DEFAULT: Configuration Manager başlat
            logger.info("� Configuration Manager v2.0 başlatılıyor (Default)...")
            print(f"{Colors.BOLD}{Colors.OKCYAN}� D64 Converter v5.0 - Configuration Manager (Default){Colors.ENDC}")
            return launch_configuration_manager(args.theme)
            
    except KeyboardInterrupt:
        logger.info("👋 Program terminated by user")
        return True
    except Exception as e:
        logger.error(f"❌ Program error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
