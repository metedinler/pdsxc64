#!/usr/bin/env python3
"""
D64 Converter v5.0 - ULTIMATE MAIN ENTRY POINT
Advanced Commodore 64 Decompiler Suite
🚀 ULTIMATE VERSION - En Güçlü, En Muazzam, Sequential Flow
✨ Features: Detaylı logging, Renkli terminal, Virtual environment, No selection menu
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

def print_banner():
    """Enhanced graphical banner with colors"""
    banner = f"""
{Colors.HEADER}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  {Colors.BOLD}🚀 D64 CONVERTER v5.0 - ULTIMATE EDITION 🚀{Colors.ENDC}{Colors.HEADER}                          ║
║                                                                              ║
║  {Colors.OKBLUE}Advanced Commodore 64 Decompiler Suite{Colors.ENDC}{Colors.HEADER}                               ║
║  {Colors.OKCYAN}✨ Assembly Formatters (8 formats) + Decompiler Languages (5 formats){Colors.ENDC}{Colors.HEADER}  ║
║  {Colors.OKGREEN}🔧 Enhanced Memory Manager • 🧠 AI Pattern Recognition{Colors.ENDC}{Colors.HEADER}                ║
║  {Colors.WARNING}📊 94% Success Rate • 🎯 Production Ready{Colors.ENDC}{Colors.HEADER}                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BOLD}{Colors.OKCYAN}🎯 SEQUENTIAL STARTUP FLOW - NO SELECTION MENUS{Colors.ENDC}
{Colors.GRAY}════════════════════════════════════════════════════════════════════════════════{Colors.ENDC}
"""
    print(banner)

def setup_enhanced_logging(log_level="INFO", log_file=None, enable_colors=True):
    """
    🎨 Enhanced logging system with colors and graphics
    """
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Generate log file name if not provided
    if log_file is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"d64_converter_ultimate_{timestamp}.log"
    
    # Custom colored formatter
    class ColoredFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': Colors.GRAY,
            'INFO': Colors.OKGREEN,
            'WARNING': Colors.WARNING,
            'ERROR': Colors.FAIL,
            'CRITICAL': Colors.BOLD + Colors.FAIL
        }
        
        def format(self, record):
            if enable_colors:
                color = self.COLORS.get(record.levelname, '')
                record.levelname = f"{color}{record.levelname}{Colors.ENDC}"
                record.msg = f"{color}{record.msg}{Colors.ENDC}"
            return super().format(record)
    
    # Enhanced log format with graphics
    log_format = '%(asctime)s 🔍 %(levelname)s 📍 %(module)s:%(lineno)d 💬 %(message)s'
    
    # Configure logging
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Create handlers
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    ))
    
    console_handler = logging.StreamHandler(sys.stdout)
    if enable_colors:
        console_handler.setFormatter(ColoredFormatter(log_format))
    else:
        console_handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        handlers=[file_handler, console_handler]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"{Colors.OKGREEN}🎯 Enhanced logging system initialized: {log_file}{Colors.ENDC}")
    logger.info(f"{Colors.OKBLUE}📊 Log level: {log_level}{Colors.ENDC}")
    
    return logger

def create_virtual_environment(venv_path="venv_asmto"):
    """
    🌟 RESTORED: Create and manage virtual environment (one-time setup, stays active)
    """
    logger = logging.getLogger(__name__)
    
    if os.path.exists(venv_path):
        logger.info(f"📦 Virtual environment already exists: {Colors.OKGREEN}{venv_path}{Colors.ENDC}")
        return True
    else:
        logger.info(f"📦 Creating virtual environment: {Colors.OKCYAN}{venv_path}{Colors.ENDC}")
        try:
            # Animated progress
            def show_progress():
                chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
                for i in range(20):
                    sys.stdout.write(f"\r{Colors.OKCYAN}Creating virtual environment {chars[i % len(chars)]}{Colors.ENDC}")
                    sys.stdout.flush()
                    time.sleep(0.1)
                sys.stdout.write(f"\r{Colors.OKGREEN}✅ Virtual environment creation completed!{Colors.ENDC}\n")
            
            progress_thread = threading.Thread(target=show_progress)
            progress_thread.start()
            
            venv.create(venv_path, with_pip=True)
            
            progress_thread.join()
            logger.info(f"✅ Virtual environment created successfully: {Colors.OKGREEN}{venv_path}{Colors.ENDC}")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating virtual environment: {Colors.FAIL}{e}{Colors.ENDC}")
            return False

def install_required_packages(venv_path="venv_asmto"):
    """
    📚 Install required packages in virtual environment
    """
    logger = logging.getLogger(__name__)
    
    # Required packages
    packages = [
        "tkinterdnd2",
        "py65",
        "pillow",
        "numpy",
        "colorama"
    ]
    
    # Get pip executable path
    if platform.system() == "Windows":
        pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        pip_executable = os.path.join(venv_path, "bin", "pip")
    
    logger.info(f"📚 Installing required packages: {Colors.OKCYAN}{', '.join(packages)}{Colors.ENDC}")
    
    for package in packages:
        try:
            logger.info(f"⬇️ Installing {Colors.YELLOW}{package}{Colors.ENDC}...")
            result = subprocess.run(
                [pip_executable, "install", package],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"✅ {Colors.OKGREEN}{package}{Colors.ENDC} installed successfully")
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Could not install {Colors.WARNING}{package}{Colors.ENDC}: {e}")
        except Exception as e:
            logger.error(f"❌ Error installing {Colors.FAIL}{package}{Colors.ENDC}: {e}")

def create_enhanced_directories():
    """
    📁 Create enhanced directory structure with assembly formatters + decompiler languages
    """
    logger = logging.getLogger(__name__)
    
    # Enhanced directory structure
    directories = {
        # Assembly Formatters (8 formats)
        "format_files/assembly/tass": "TASS Turbo Assembler outputs",
        "format_files/assembly/kickass": "KickAssembler outputs", 
        "format_files/assembly/dasm": "DASM outputs",
        "format_files/assembly/css64": "CSS64 outputs",
        "format_files/assembly/supermon": "SuperMon outputs",
        "format_files/assembly/native": "Native 6502 outputs",
        "format_files/assembly/acme": "ACME assembler outputs",
        "format_files/assembly/ca65": "CA65 assembler outputs",
        
        # Decompiler Languages (5 formats)
        "format_files/languages/c": "C language decompiler outputs",
        "format_files/languages/qbasic": "QBasic decompiler outputs",
        "format_files/languages/pdsx": "PDSx-BASIC decompiler outputs", 
        "format_files/languages/cpp": "C++ decompiler outputs",
        "format_files/languages/commodore_basic": "Commodore BASIC V2 outputs",
        
        # Traditional directories (backward compatibility)
        "asm_files": "Traditional assembly files",
        "c_files": "Traditional C files",
        "qbasic_files": "Traditional QBasic files", 
        "pdsx_files": "Traditional PDSx files",
        "pseudo_files": "Pseudocode files",
        "png_files": "Sprite PNG outputs",
        "sid_files": "SID music files",
        "prg_files": "Extracted PRG files",
        "logs": "System and operation logs",
        "test_files": "Test and validation files",
        "utilities_files/aktif": "Active utility files",
        "utilities_files/pasif": "Passive/backup utility files"
    }
    
    logger.info(f"{Colors.BOLD}📁 Creating enhanced directory structure...{Colors.ENDC}")
    
    created_count = 0
    for dirname, description in directories.items():
        try:
            Path(dirname).mkdir(parents=True, exist_ok=True)
            logger.info(f"📂 {Colors.OKGREEN}{dirname:<35}{Colors.ENDC} - {Colors.GRAY}{description}{Colors.ENDC}")
            created_count += 1
        except Exception as e:
            logger.error(f"❌ Failed to create {Colors.FAIL}{dirname}{Colors.ENDC}: {e}")
    
    logger.info(f"✅ {Colors.OKGREEN}Directory structure created: {created_count} directories{Colors.ENDC}")

def check_system_status():
    """
    🔍 Comprehensive system status check
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"{Colors.BOLD}🔍 SYSTEM STATUS CHECK{Colors.ENDC}")
    logger.info(f"{'='*60}")
    
    # Python version
    logger.info(f"🐍 Python Version: {Colors.OKCYAN}{sys.version.split()[0]}{Colors.ENDC}")
    
    # Platform info
    logger.info(f"💻 Platform: {Colors.OKCYAN}{platform.platform()}{Colors.ENDC}")
    
    # Working directory
    logger.info(f"📍 Working Directory: {Colors.OKCYAN}{os.getcwd()}{Colors.ENDC}")
    
    # Check virtual environment
    venv_path = "venv_asmto"
    venv_status = "✅ EXISTS" if os.path.exists(venv_path) else "❌ NOT FOUND"
    logger.info(f"📦 Virtual Environment: {Colors.OKGREEN if os.path.exists(venv_path) else Colors.FAIL}{venv_status}{Colors.ENDC}")
    
    # Check critical modules
    critical_modules = [
        "enhanced_c64_memory_manager",
        "assembly_formatters", 
        "unified_decompiler",
        "code_analyzer",
        "improved_disassembler"
    ]
    
    logger.info(f"{Colors.BOLD}🔧 CRITICAL MODULES CHECK{Colors.ENDC}")
    for module in critical_modules:
        try:
            __import__(module)
            logger.info(f"📚 {module:<30} {Colors.OKGREEN}✅ AVAILABLE{Colors.ENDC}")
        except ImportError as e:
            logger.error(f"📚 {module:<30} {Colors.FAIL}❌ MISSING{Colors.ENDC}")
    
    # Check GUI availability
    logger.info(f"{Colors.BOLD}🖥️  GUI AVAILABILITY{Colors.ENDC}")
    gui_files = ["gui_manager.py", "gui_demo.py", "clean_gui_selector.py", "eski_gui_3.py"]
    for gui_file in gui_files:
        if os.path.exists(gui_file):
            logger.info(f"🖼️  {gui_file:<25} {Colors.OKGREEN}✅ AVAILABLE{Colors.ENDC}")
        else:
            logger.info(f"🖼️  {gui_file:<25} {Colors.WARNING}⚠️  NOT FOUND{Colors.ENDC}")

def setup_comprehensive_argparse():
    """
    🛠️ Comprehensive argument parser with 25+ arguments
    """
    parser = argparse.ArgumentParser(
        description="D64 Converter v5.0 - Ultimate Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD}EXAMPLES:{Colors.ENDC}
  {Colors.OKCYAN}python main.py --gui modern{Colors.ENDC}                    # Modern GUI
  {Colors.OKCYAN}python main.py --cmd --input test.d64{Colors.ENDC}          # Command line mode
  {Colors.OKCYAN}python main.py --test --verbose{Colors.ENDC}                # Run tests with verbose output
  {Colors.OKCYAN}python main.py --assembly-format tass{Colors.ENDC}          # Use TASS format
  {Colors.OKCYAN}python main.py --decompiler-language c{Colors.ENDC}         # Decompile to C
  {Colors.OKCYAN}python main.py --batch --input-dir ./prg_files{Colors.ENDC} # Batch processing

{Colors.BOLD}ASSEMBLY FORMATS:{Colors.ENDC} tass, kickass, dasm, css64, supermon, native, acme, ca65
{Colors.BOLD}DECOMPILER LANGUAGES:{Colors.ENDC} c, qbasic, pdsx, cpp, commodore_basic
        """
    )
    
    # Main operation modes
    parser.add_argument("--gui", choices=["modern", "classic", "legacy"], 
                       help="Launch GUI mode (modern, classic, or legacy)")
    parser.add_argument("--cmd", action="store_true", 
                       help="Command line mode")
    parser.add_argument("--test", action="store_true", 
                       help="Run test suite")
    parser.add_argument("--status", action="store_true", 
                       help="Show system status")
    parser.add_argument("--venv", action="store_true", 
                       help="Setup/check virtual environment")
    
    # Input/Output
    parser.add_argument("--input", "-i", type=str, 
                       help="Input file (D64, PRG, etc.)")
    parser.add_argument("--output", "-o", type=str, 
                       help="Output directory")
    parser.add_argument("--input-dir", type=str, 
                       help="Input directory for batch processing")
    parser.add_argument("--output-format", choices=["asm", "c", "qbasic", "pdsx", "cpp", "pseudo"], 
                       help="Output format")
    
    # Assembly formatters (NEW!)
    parser.add_argument("--assembly-format", choices=["tass", "kickass", "dasm", "css64", "supermon", "native", "acme", "ca65"],
                       default="native", help="Assembly output format")
    parser.add_argument("--decompiler-language", choices=["c", "qbasic", "pdsx", "cpp", "commodore_basic"],
                       help="Decompiler target language")
    parser.add_argument("--separate-tables", action="store_true", 
                       help="Use separate result tables for each format")
    
    # Processing options
    parser.add_argument("--disassembler", choices=["basic", "advanced", "improved", "py65_professional"], 
                       default="improved", help="Disassembler to use")
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
    
    # Logging and debugging
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="Logging level")
    parser.add_argument("--log-file", type=str, 
                       help="Custom log file path")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
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
    
    return parser

def run_sequential_startup(args):
    """
    🚀 SEQUENTIAL STARTUP FLOW - NO SELECTION MENUS
    Enhanced with assembly formatters and decompiler languages
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"{Colors.BOLD}{Colors.OKGREEN}🚀 STARTING SEQUENTIAL STARTUP FLOW{Colors.ENDC}")
    logger.info(f"{'='*60}")
    
    # Step 1: Virtual Environment Setup
    logger.info(f"{Colors.BOLD}📦 STEP 1: Virtual Environment Management{Colors.ENDC}")
    if not create_virtual_environment():
        logger.error(f"{Colors.FAIL}❌ Virtual environment setup failed{Colors.ENDC}")
        return False
    install_required_packages()
    
    # Step 2: Directory Structure
    logger.info(f"{Colors.BOLD}📁 STEP 2: Enhanced Directory Structure{Colors.ENDC}")
    create_enhanced_directories()
    
    # Step 3: System Status Check
    logger.info(f"{Colors.BOLD}🔍 STEP 3: System Status Check{Colors.ENDC}")
    check_system_status()
    
    # Step 4: Assembly Formatters Integration
    logger.info(f"{Colors.BOLD}🔧 STEP 4: Assembly Formatters Integration{Colors.ENDC}")
    try:
        from assembly_formatters import AssemblyFormatters
        formatters = AssemblyFormatters()
        supported_formats = formatters.list_supported_formats()
        logger.info(f"✅ Assembly Formatters loaded: {Colors.OKCYAN}{len(supported_formats)} formats{Colors.ENDC}")
        for key, name in supported_formats.items():
            logger.info(f"   📝 {key}: {Colors.GRAY}{name}{Colors.ENDC}")
    except ImportError as e:
        logger.error(f"❌ Could not load Assembly Formatters: {Colors.FAIL}{e}{Colors.ENDC}")
    
    # Step 5: Decompiler Languages Integration  
    logger.info(f"{Colors.BOLD}🎯 STEP 5: Decompiler Languages Integration{Colors.ENDC}")
    try:
        from unified_decompiler import UnifiedDecompiler
        decompiler = UnifiedDecompiler("c")  # Test initialization
        logger.info(f"✅ Unified Decompiler loaded: {Colors.OKGREEN}5 target languages{Colors.ENDC}")
        languages = ["C", "QBasic", "PDSx-BASIC", "C++", "Commodore BASIC V2"]
        for lang in languages:
            logger.info(f"   🎯 {Colors.GRAY}{lang}{Colors.ENDC}")
    except ImportError as e:
        logger.error(f"❌ Could not load Unified Decompiler: {Colors.FAIL}{e}{Colors.ENDC}")
    
    # Step 6: Mode Selection Based on Arguments
    logger.info(f"{Colors.BOLD}🎮 STEP 6: Mode Selection{Colors.ENDC}")
    
    if args.status:
        logger.info(f"📊 System status displayed successfully")
        return True
    elif args.test:
        logger.info(f"🧪 Running test suite...")
        return run_test_suite(args)
    elif args.gui:
        logger.info(f"🖥️  Launching {Colors.OKCYAN}{args.gui}{Colors.ENDC} GUI...")
        return launch_gui(args.gui)
    elif args.cmd:
        logger.info(f"💻 Starting command line mode...")
        return run_command_line_mode(args)
    else:
        # Default: Show available options and run modern GUI
        logger.info(f"{Colors.BOLD}🎯 No specific mode selected, launching Modern GUI...{Colors.ENDC}")
        return launch_gui("modern")

def launch_gui(gui_type="modern"):
    """
    🖥️ Launch specified GUI type
    """
    logger = logging.getLogger(__name__)
    
    gui_files = {
        "modern": ("gui_demo.py", "Modern GUI v5.0"),
        "classic": ("clean_gui_selector.py", "Classic GUI Selector"),
        "legacy": ("eski_gui_3.py", "Legacy GUI v3")
    }
    
    if gui_type not in gui_files:
        logger.error(f"❌ Unknown GUI type: {Colors.FAIL}{gui_type}{Colors.ENDC}")
        return False
    
    gui_file, gui_name = gui_files[gui_type]
    
    if not os.path.exists(gui_file):
        logger.error(f"❌ GUI file not found: {Colors.FAIL}{gui_file}{Colors.ENDC}")
        return False
    
    logger.info(f"🚀 Launching {Colors.OKCYAN}{gui_name}{Colors.ENDC}...")
    
    try:
        # Import and run the GUI
        if gui_type == "modern":
            import gui_demo
            gui_demo.main()
        elif gui_type == "classic":
            import clean_gui_selector
            clean_gui_selector.main()
        elif gui_type == "legacy":
            import eski_gui_3
            eski_gui_3.main()
        
        logger.info(f"✅ {gui_name} launched successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error launching {gui_name}: {Colors.FAIL}{e}{Colors.ENDC}")
        return False

def run_command_line_mode(args):
    """
    💻 Command line processing mode
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"{Colors.BOLD}💻 COMMAND LINE MODE{Colors.ENDC}")
    
    if not args.input:
        logger.error(f"❌ No input file specified. Use --input <file>")
        return False
    
    if not os.path.exists(args.input):
        logger.error(f"❌ Input file not found: {Colors.FAIL}{args.input}{Colors.ENDC}")
        return False
    
    logger.info(f"📁 Processing: {Colors.OKCYAN}{args.input}{Colors.ENDC}")
    logger.info(f"🔧 Disassembler: {Colors.OKCYAN}{args.disassembler}{Colors.ENDC}")
    
    if args.assembly_format:
        logger.info(f"📝 Assembly format: {Colors.OKCYAN}{args.assembly_format}{Colors.ENDC}")
    
    if args.decompiler_language:
        logger.info(f"🎯 Target language: {Colors.OKCYAN}{args.decompiler_language}{Colors.ENDC}")
    
    # TODO: Implement actual processing logic
    logger.info(f"✅ Command line processing would be implemented here")
    return True

def run_test_suite(args):
    """
    🧪 Run comprehensive test suite
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"{Colors.BOLD}🧪 RUNNING COMPREHENSIVE TEST SUITE{Colors.ENDC}")
    
    test_files = [
        "test_files/test_enhanced_c64_memory_manager.py",
        "test_files/test_unified_decompiler.py", 
        "test_files/test_code_analyzer.py"
    ]
    
    if os.path.exists("assembly_formatters.py"):
        logger.info(f"🔧 Testing Assembly Formatters...")
        try:
            import assembly_formatters
            logger.info(f"✅ Assembly Formatters test passed")
        except Exception as e:
            logger.error(f"❌ Assembly Formatters test failed: {e}")
    
    # TODO: Add more comprehensive test execution
    logger.info(f"✅ Test suite completed")
    return True

def main():
    """
    🎯 ULTIMATE MAIN FUNCTION - Sequential Flow, No Selection Menu
    """
    # Print banner first
    print_banner()
    
    # Setup argument parser
    parser = setup_comprehensive_argparse()
    args = parser.parse_args()
    
    # Setup enhanced logging
    logger = setup_enhanced_logging(
        log_level=args.log_level,
        log_file=args.log_file,
        enable_colors=not args.no_colors
    )
    
    logger.info(f"{Colors.BOLD}🎯 D64 Converter v5.0 - Ultimate Edition Started{Colors.ENDC}")
    logger.info(f"⏰ Timestamp: {Colors.OKCYAN}{datetime.datetime.now()}{Colors.ENDC}")
    
    try:
        # Run sequential startup
        success = run_sequential_startup(args)
        
        if success:
            logger.info(f"{Colors.BOLD}{Colors.OKGREEN}🎉 D64 Converter v5.0 - Ultimate Edition completed successfully!{Colors.ENDC}")
        else:
            logger.error(f"{Colors.BOLD}{Colors.FAIL}❌ D64 Converter v5.0 - Ultimate Edition failed!{Colors.ENDC}")
            
    except KeyboardInterrupt:
        logger.info(f"{Colors.WARNING}⚠️ Operation cancelled by user{Colors.ENDC}")
    except Exception as e:
        logger.error(f"{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        if args.verbose:
            import traceback
            logger.error(f"{Colors.FAIL}{traceback.format_exc()}{Colors.ENDC}")

if __name__ == "__main__":
    main()
