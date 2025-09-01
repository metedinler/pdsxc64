#!/usr/bin/env python3
"""
D64 Converter v6.0 - COMPREHENSIVE COMMAND LINE INTERFACE
Advanced Commodore 64 Decompiler Suite with Full Feature Access
🚀 COMPLETE SYSTEM ACCESS VIA COMMAND LINE
✨ Features: All system features, Plugin support, Comprehensive testing
📝 Comprehensive Logging: Tüm kullanıcı etkileşimleri, hatalar, uyarılar loglanır
"""

import os
import sys
import argparse
import logging
import datetime
import json
import subprocess
import platform
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# Comprehensive logging sistemi başlat
try:
    from comprehensive_logger import init_logger, log_info, log_error, log_warning, log_user_action, log_performance
    # Logger'ı hemen başlat
    logger = init_logger()
    log_info("D64 Converter v6.0 Comprehensive başlatıldı", "MAIN_COMPREHENSIVE_STARTUP")
except Exception as e:
    print(f"⚠️ Logging sistemi başlatılamadı: {e}")
    # Fallback olarak basit print fonksiyonları
    def log_info(msg, context=None): print(f"ℹ️ {msg}")
    def log_error(msg, exc=None, context=None): print(f"🔴 {msg}")  
    def log_warning(msg, context=None): print(f"⚠️ {msg}")
    def log_user_action(*args, **kwargs): pass
    def log_performance(*args, **kwargs): pass

# ==========================================
# SANAL ORTAM KONTROLÜ (venv_asmto)
# ==========================================

def ensure_venv_asmto():
    """venv_asmto sanal ortamının aktif olduğundan emin ol - Auto activation ile"""
    script_dir = Path(__file__).parent
    venv_path = script_dir / "venv_asmto"
    
    # Sanal ortam var mı kontrol et
    if not venv_path.exists():
        print(f"🔴 HATA: venv_asmto sanal ortamı bulunamadı: {venv_path}")
        print(f"🔧 Sanal ortam oluşturuluyor...")
        try:
            # Sanal ortamı otomatik oluştur
            import venv
            venv.create(venv_path, with_pip=True)
            print(f"✅ venv_asmto sanal ortamı oluşturuldu")
        except Exception as e:
            print(f"🔴 Sanal ortam oluşturma hatası: {e}")
            print(f"🔧 Manuel olarak oluşturun:")
            print(f"   python -m venv venv_asmto")
            sys.exit(1)
    
    # Mevcut Python'un sanal ortamda olup olmadığını kontrol et
    current_python = sys.executable
    if platform.system() == "Windows":
        expected_python = venv_path / "Scripts" / "python.exe"
    else:
        expected_python = venv_path / "bin" / "python"
    
    if not str(current_python).startswith(str(venv_path)):
        print(f"� Program sanal ortam dışında çalışıyor, otomatik geçiş yapılıyor...")
        print(f"📍 Mevcut Python: {current_python}")
        print(f"📍 Hedef Python: {expected_python}")
        
        # Sanal ortamda program yeniden başlat
        try:
            venv_python = str(expected_python)
            current_script = str(Path(__file__).resolve())
            
            # Mevcut argümanları al
            args = sys.argv[1:]  # İlk argüman script adı, o yüzden atla
            
            print(f"🚀 Sanal ortamda yeniden başlatılıyor...")
            print(f"📄 Script: {current_script}")
            print(f"🔧 Argümanlar: {args}")
            
            # Yeni process'i sanal ortamda başlat
            cmd = [venv_python, current_script] + args
            subprocess.run(cmd, cwd=script_dir)
            
            # Mevcut process'i kapat
            print(f"✅ Sanal ortam process'i başlatıldı, ana process kapatılıyor")
            sys.exit(0)
            
        except Exception as e:
            print(f"🔴 Otomatik geçiş hatası: {e}")
            print(f"🔧 Manuel olarak aktif edin:")
            if platform.system() == "Windows":
                print(f"   venv_asmto\\Scripts\\activate")
            else:
                print(f"   source venv_asmto/bin/activate")
            sys.exit(1)
    
    print(f"✅ venv_asmto sanal ortamı aktif: {current_python}")

# Sanal ortam kontrolünü hemen yap
ensure_venv_asmto()

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
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

def print_colored(text: str, color: str = Colors.ENDC):
    """Renkli metin yazdırma"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header():
    """Program başlık bilgilerini yazdır"""
    print_colored("=" * 80, Colors.HEADER)
    print_colored("🚀 D64 CONVERTER v6.0 - COMPREHENSIVE COMMAND LINE INTERFACE", Colors.HEADER + Colors.BOLD)
    print_colored("Advanced Commodore 64 Decompiler Suite", Colors.OKBLUE)
    print_colored("Author: Enhanced AI System | Date: 28 Temmuz 2025", Colors.GRAY)
    print_colored("=" * 80, Colors.HEADER)

def create_comprehensive_parser():
    """Comprehensive argument parser oluştur"""
    parser = argparse.ArgumentParser(
        description="🚀 D64 Converter v6.0 - Complete C64 Development Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📋 USAGE EXAMPLES:
  
🔍 Basic Operations:
  python main.py --analyze-d64 "demo.d64" --format kickassembler
  python main.py --disassemble-prg "program.prg" --output "output.asm"
  python main.py --transpile "code.asm" --target python --quality enhanced
  
📊 Analysis & Testing:
  python main.py --test-all-systems
  python main.py --analyze-performance "code.asm"
  python main.py --knowledge-report
  
🔌 Plugin Operations:
  python main.py --list-plugins
  python main.py --plugin-demo
  python main.py --generate-plugin --type transpiler --name "Go" --author "Developer"
  
🌉 Bridge Systems:
  python main.py --bridge-demo
  python main.py --format-convert "code.asm" --from "native" --to "kickassembler"
  
🎯 Complete System Test:
  python main.py --full-system-test --verbose
  
📚 Documentation:
  python main.py --help-all
  python main.py --version
        """
    )
    
    # === BASIC OPERATIONS ===
    basic_group = parser.add_argument_group('📁 Basic File Operations')
    basic_group.add_argument('--analyze-d64', metavar='FILE', 
                            help='Analyze D64 disk image file')
    basic_group.add_argument('--disassemble-prg', metavar='FILE',
                            help='Disassemble PRG file to assembly')
    basic_group.add_argument('--analyze-basic', metavar='FILE',
                            help='Analyze BASIC program file')
    basic_group.add_argument('--output', '-o', metavar='FILE',
                            help='Output file path')
    basic_group.add_argument('--format', choices=['native', 'kickassembler', 'tass', 'dasm', 'css64', 'supermon', 'acme', 'ca65'],
                            default='native', help='Assembly output format')
    
    # === TRANSPILATION ===
    transpile_group = parser.add_argument_group('🔄 Multi-Language Transpilation')
    transpile_group.add_argument('--transpile', metavar='FILE',
                                help='Transpile assembly file to target language')
    transpile_group.add_argument('--target', choices=['c', 'qbasic', 'python', 'javascript', 'pascal'],
                                help='Target language for transpilation')
    transpile_group.add_argument('--quality', choices=['basic', 'enhanced', 'optimized', 'production'],
                                default='enhanced', help='Transpilation quality level')
    transpile_group.add_argument('--hardware-aware', action='store_true',
                                help='Enable hardware-aware transpilation with register info')
    
    # === ANALYSIS ===
    analysis_group = parser.add_argument_group('🔍 Analysis & Performance')
    analysis_group.add_argument('--analyze-performance', metavar='FILE',
                               help='Perform performance analysis on assembly file')
    analysis_group.add_argument('--memory-analysis', metavar='FILE',
                               help='Analyze memory usage patterns')
    analysis_group.add_argument('--hardware-detection', metavar='FILE',
                               help='Detect hardware register usage')
    analysis_group.add_argument('--knowledge-report', action='store_true',
                               help='Generate comprehensive knowledge database report')
    
    # === PLUGIN SYSTEM ===
    plugin_group = parser.add_argument_group('🔌 Plugin System')
    plugin_group.add_argument('--list-plugins', action='store_true',
                             help='List all available plugins')
    plugin_group.add_argument('--plugin-demo', action='store_true',
                             help='Run comprehensive plugin system demo')
    plugin_group.add_argument('--load-plugin', metavar='NAME',
                             help='Load specific plugin by name')
    plugin_group.add_argument('--execute-plugin', metavar='NAME',
                             help='Execute specific plugin')
    plugin_group.add_argument('--generate-plugin', action='store_true',
                             help='Generate new plugin template')
    plugin_group.add_argument('--plugin-type', choices=['format', 'transpiler', 'analyzer', 'export', 'tool'],
                             help='Plugin type for generation')
    plugin_group.add_argument('--plugin-name', metavar='NAME',
                             help='Plugin name for generation')
    plugin_group.add_argument('--plugin-author', metavar='AUTHOR', default='Unknown',
                             help='Plugin author for generation')
    
    # === BRIDGE SYSTEMS ===
    bridge_group = parser.add_argument_group('🌉 Bridge Systems')
    bridge_group.add_argument('--bridge-demo', action='store_true',
                             help='Run Bridge Systems demonstration')
    bridge_group.add_argument('--format-convert', metavar='FILE',
                             help='Convert assembly format using bridge system')
    bridge_group.add_argument('--from-format', metavar='FORMAT',
                             help='Source format for conversion')
    bridge_group.add_argument('--to-format', metavar='FORMAT',
                             help='Target format for conversion')
    bridge_group.add_argument('--transpile-bridge', metavar='FILE',
                             help='Use transpiler bridge for multi-language conversion')
    
    # === TESTING ===
    test_group = parser.add_argument_group('🧪 Testing & Quality Assurance')
    test_group.add_argument('--test-all-systems', action='store_true',
                           help='Run comprehensive system tests')
    test_group.add_argument('--test-disassembler', action='store_true',
                           help='Test disassembler with sample files')
    test_group.add_argument('--test-transpiler', action='store_true',
                           help='Test transpiler engine with all languages')
    test_group.add_argument('--test-plugins', action='store_true',
                           help='Test all loaded plugins')
    test_group.add_argument('--test-bridges', action='store_true',
                           help='Test bridge systems')
    test_group.add_argument('--benchmark', action='store_true',
                           help='Run performance benchmarks')
    test_group.add_argument('--full-system-test', action='store_true',
                           help='Complete system validation (all tests)')
    
    # === OUTPUT & BEHAVIOR ===
    output_group = parser.add_argument_group('📄 Output & Behavior')
    output_group.add_argument('--verbose', '-v', action='store_true',
                             help='Enable verbose output')
    output_group.add_argument('--quiet', '-q', action='store_true',
                             help='Suppress non-essential output')
    output_group.add_argument('--debug', action='store_true',
                             help='Enable debug mode with detailed logging')
    output_group.add_argument('--log-file', metavar='FILE',
                             help='Log output to file')
    output_group.add_argument('--json-output', action='store_true',
                             help='Output results in JSON format')
    output_group.add_argument('--no-color', action='store_true',
                             help='Disable colored output')
    
    # === INFORMATION ===
    info_group = parser.add_argument_group('📚 Information & Help')
    info_group.add_argument('--version', action='version', version='D64 Converter v6.0')
    info_group.add_argument('--help-all', action='store_true',
                           help='Show comprehensive help with all features')
    info_group.add_argument('--list-formats', action='store_true',
                           help='List all supported assembly formats')
    info_group.add_argument('--list-targets', action='store_true',
                           help='List all supported transpilation targets')
    info_group.add_argument('--system-info', action='store_true',
                           help='Show detailed system information')
    
    return parser

def setup_logging(args):
    """Logging sistemini ayarla"""
    log_level = logging.DEBUG if args.debug else (logging.WARNING if args.quiet else logging.INFO)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if args.log_file:
        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=args.log_file,
            filemode='w'
        )
    else:
        logging.basicConfig(
            level=log_level,
            format=log_format
        )
    
    logger = logging.getLogger('D64Converter')
    return logger

def load_core_modules():
    """Core modülleri yükle"""
    try:
        global d64_reader, improved_disassembler, c64_memory_manager
        global enhanced_c64_knowledge_manager, transpiler_engine, plugin_manager
        global bridge_systems
        
        print_colored("🔄 Loading core modules...", Colors.OKCYAN)
        
        # Core modules
        import d64_reader
        import improved_disassembler
        import c64_memory_manager
        
        # Enhanced modules
        import enhanced_c64_knowledge_manager
        import transpiler_engine
        import plugin_manager
        import bridge_systems
        
        print_colored("✅ All core modules loaded successfully", Colors.OKGREEN)
        return True
        
    except ImportError as e:
        print_colored(f"❌ Failed to load core modules: {e}", Colors.FAIL)
        return False

def handle_basic_operations(args, logger):
    """Basic file operations handler"""
    
    if args.analyze_d64:
        print_colored(f"🔍 Analyzing D64 file: {args.analyze_d64}", Colors.OKCYAN)
        try:
            reader = d64_reader.D64Reader(args.analyze_d64)
            files = reader.list_files()
            
            if args.json_output:
                print(json.dumps({"d64_analysis": files}, indent=2))
            else:
                print_colored(f"📁 Found {len(files)} files in D64:", Colors.OKGREEN)
                for file_info in files:
                    print(f"  - {file_info}")
                    
        except Exception as e:
            print_colored(f"❌ Error analyzing D64: {e}", Colors.FAIL)
            
    if args.disassemble_prg:
        print_colored(f"🔧 Disassembling PRG file: {args.disassemble_prg}", Colors.OKCYAN)
        try:
            with open(args.disassemble_prg, 'rb') as f:
                prg_data = f.read()
                
            disasm = improved_disassembler.ImprovedDisassembler()
            assembly_code = disasm.disassemble_data(prg_data, assembly_format=args.format)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(assembly_code)
                print_colored(f"✅ Assembly saved to: {args.output}", Colors.OKGREEN)
            else:
                print(assembly_code)
                
        except Exception as e:
            print_colored(f"❌ Error disassembling PRG: {e}", Colors.FAIL)
            
    if args.analyze_basic:
        print_colored(f"📝 Analyzing BASIC file: {args.analyze_basic}", Colors.OKCYAN)
        try:
            # BASIC analysis implementation
            import c64_basic_parser
            parser = c64_basic_parser.C64BasicParser()
            result = parser.analyze_file(args.analyze_basic)
            
            if args.json_output:
                print(json.dumps(result, indent=2))
            else:
                print_colored("📊 BASIC Analysis Results:", Colors.OKGREEN)
                print(f"Lines: {result.get('line_count', 0)}")
                print(f"Variables: {result.get('variable_count', 0)}")
                
        except Exception as e:
            print_colored(f"❌ Error analyzing BASIC: {e}", Colors.FAIL)

def handle_transpilation(args, logger):
    """Transpilation operations handler"""
    
    if args.transpile and args.target:
        print_colored(f"🔄 Transpiling {args.transpile} to {args.target}", Colors.OKCYAN)
        try:
            with open(args.transpile, 'r', encoding='utf-8') as f:
                assembly_code = f.read()
                
            # Load Enhanced Transpiler Engine
            engine = transpiler_engine.EnhancedTranspilerEngine()
            
            # Transpile
            transpiled_code = engine.transpile_to_language(
                assembly_code=assembly_code,
                target_language=args.target,
                quality_level=args.quality,
                hardware_aware=args.hardware_aware
            )
            
            # Output
            if args.output:
                output_file = args.output
            else:
                base_name = os.path.splitext(args.transpile)[0]
                extensions = {'c': '.c', 'qbasic': '.bas', 'python': '.py', 'javascript': '.js', 'pascal': '.pas'}
                output_file = f"{base_name}{extensions.get(args.target, '.txt')}"
                
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(transpiled_code)
                
            print_colored(f"✅ {args.target.title()} code saved to: {output_file}", Colors.OKGREEN)
            
        except Exception as e:
            print_colored(f"❌ Error during transpilation: {e}", Colors.FAIL)

def handle_analysis(args, logger):
    """Analysis operations handler"""
    
    if args.analyze_performance:
        print_colored(f"📊 Analyzing performance: {args.analyze_performance}", Colors.OKCYAN)
        try:
            with open(args.analyze_performance, 'r', encoding='utf-8') as f:
                assembly_code = f.read()
                
            # Load Performance Analyzer Plugin
            pm = plugin_manager.get_plugin_manager()
            analyzer_plugins = pm.get_plugins_by_type(plugin_manager.PluginType.ANALYZER)
            
            if analyzer_plugins:
                perf_plugin = analyzer_plugins[0]  # Use first analyzer
                analysis_result = perf_plugin.execute(assembly_code)
                
                if args.json_output:
                    print(json.dumps(analysis_result, indent=2))
                else:
                    print_colored("📊 Performance Analysis Results:", Colors.OKGREEN)
                    print(f"Total Instructions: {analysis_result.get('instruction_count', 0)}")
                    print(f"Total Cycles: {analysis_result.get('total_cycles', 0)}")
                    print(f"Performance Issues: {len(analysis_result.get('performance_issues', []))}")
                    print(analysis_result.get('summary', ''))
            else:
                print_colored("❌ No performance analyzer plugin available", Colors.FAIL)
                
        except Exception as e:
            print_colored(f"❌ Error during performance analysis: {e}", Colors.FAIL)
            
    if args.knowledge_report:
        print_colored("📚 Generating knowledge database report...", Colors.OKCYAN)
        try:
            km = enhanced_c64_knowledge_manager.EnhancedC64KnowledgeManager()
            report = km.generate_knowledge_report()
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(report)
                print_colored(f"✅ Knowledge report saved to: {args.output}", Colors.OKGREEN)
            else:
                print(report)
                
        except Exception as e:
            print_colored(f"❌ Error generating knowledge report: {e}", Colors.FAIL)

def handle_plugins(args, logger):
    """Plugin system handler"""
    
    if args.list_plugins:
        print_colored("🔌 Available Plugins:", Colors.OKCYAN)
        try:
            pm = plugin_manager.get_plugin_manager()
            plugins = pm.list_plugins()
            
            if args.json_output:
                print(json.dumps(plugins, indent=2, default=str))
            else:
                for name, info in plugins.items():
                    status = "🟢 LOADED" if info["loaded"] else "🔵 DISCOVERED"
                    metadata = info["metadata"]
                    print(f"  {status} {name} v{metadata.version}")
                    print(f"      Type: {metadata.plugin_type.value}")
                    print(f"      Author: {metadata.author}")
                    print(f"      Description: {metadata.description}")
                    print()
                    
        except Exception as e:
            print_colored(f"❌ Error listing plugins: {e}", Colors.FAIL)
            
    if args.plugin_demo:
        print_colored("🎮 Running Plugin Demo...", Colors.OKCYAN)
        try:
            import plugin_demo
            plugin_demo.main()
        except Exception as e:
            print_colored(f"❌ Error running plugin demo: {e}", Colors.FAIL)
            
    if args.generate_plugin and args.plugin_type and args.plugin_name:
        print_colored(f"🛠️ Generating {args.plugin_type} plugin: {args.plugin_name}", Colors.OKCYAN)
        try:
            pm = plugin_manager.get_plugin_manager()
            plugin_type = plugin_manager.PluginType(args.plugin_type)
            
            template_code = pm.create_plugin_template(
                plugin_name=args.plugin_name,
                plugin_type=plugin_type,
                author=args.plugin_author
            )
            
            output_file = f"plugins/{args.plugin_name.lower()}_{args.plugin_type}_plugin.py"
            os.makedirs('plugins', exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template_code)
                
            print_colored(f"✅ Plugin template saved to: {output_file}", Colors.OKGREEN)
            
        except Exception as e:
            print_colored(f"❌ Error generating plugin: {e}", Colors.FAIL)

def handle_bridges(args, logger):
    """Bridge systems handler"""
    
    if args.bridge_demo:
        print_colored("🌉 Running Bridge Systems Demo...", Colors.OKCYAN)
        try:
            bs = bridge_systems.BridgeSystemsManager()
            bs.run_comprehensive_demo()
        except Exception as e:
            print_colored(f"❌ Error running bridge demo: {e}", Colors.FAIL)
            
    if args.format_convert and args.from_format and args.to_format:
        print_colored(f"🔄 Converting format: {args.from_format} → {args.to_format}", Colors.OKCYAN)
        try:
            with open(args.format_convert, 'r', encoding='utf-8') as f:
                assembly_code = f.read()
                
            bs = bridge_systems.BridgeSystemsManager()
            converted_code = bs.convert_assembly_format(
                assembly_code=assembly_code,
                source_format=args.from_format,
                target_format=args.to_format
            )
            
            if args.output:
                output_file = args.output
            else:
                base_name = os.path.splitext(args.format_convert)[0]
                output_file = f"{base_name}_{args.to_format}.asm"
                
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted_code)
                
            print_colored(f"✅ Converted assembly saved to: {output_file}", Colors.OKGREEN)
            
        except Exception as e:
            print_colored(f"❌ Error during format conversion: {e}", Colors.FAIL)

def handle_testing(args, logger):
    """Testing operations handler"""
    
    if args.test_all_systems or args.full_system_test:
        print_colored("🧪 Running Comprehensive System Tests...", Colors.OKCYAN)
        
        test_results = {
            "disassembler_test": False,
            "transpiler_test": False,
            "plugin_test": False,
            "bridge_test": False,
            "knowledge_manager_test": False
        }
        
        # Test Disassembler
        try:
            print_colored("  🔧 Testing Disassembler...", Colors.YELLOW)
            disasm = improved_disassembler.ImprovedDisassembler()
            test_data = bytes([0xA9, 0xFF, 0x8D, 0x20, 0xD0])  # LDA #$FF; STA $D020
            result = disasm.disassemble_data(test_data)
            test_results["disassembler_test"] = "LDA" in result and "STA" in result
            print_colored(f"    ✅ Disassembler: {'PASS' if test_results['disassembler_test'] else 'FAIL'}", Colors.OKGREEN if test_results["disassembler_test"] else Colors.FAIL)
        except Exception as e:
            print_colored(f"    ❌ Disassembler test failed: {e}", Colors.FAIL)
            
        # Test Transpiler
        try:
            print_colored("  🔄 Testing Transpiler Engine...", Colors.YELLOW)
            engine = transpiler_engine.EnhancedTranspilerEngine()
            test_asm = "LDA #$FF\\nSTA $D020"
            result = engine.transpile_to_language(test_asm, "python", "basic")
            test_results["transpiler_test"] = "def" in result or "cpu" in result
            print_colored(f"    ✅ Transpiler: {'PASS' if test_results['transpiler_test'] else 'FAIL'}", Colors.OKGREEN if test_results["transpiler_test"] else Colors.FAIL)
        except Exception as e:
            print_colored(f"    ❌ Transpiler test failed: {e}", Colors.FAIL)
            
        # Test Plugins
        try:
            print_colored("  🔌 Testing Plugin System...", Colors.YELLOW)
            pm = plugin_manager.get_plugin_manager()
            plugins = pm.list_plugins()
            test_results["plugin_test"] = len(plugins) > 0
            print_colored(f"    ✅ Plugins: {'PASS' if test_results['plugin_test'] else 'FAIL'} ({len(plugins)} plugins)", Colors.OKGREEN if test_results["plugin_test"] else Colors.FAIL)
        except Exception as e:
            print_colored(f"    ❌ Plugin test failed: {e}", Colors.FAIL)
            
        # Test Bridges
        try:
            print_colored("  🌉 Testing Bridge Systems...", Colors.YELLOW)
            bs = bridge_systems.BridgeSystemsManager()
            test_asm = "LDA #$FF"
            result = bs.convert_assembly_format(test_asm, "native", "kickassembler")
            test_results["bridge_test"] = len(result) > 0
            print_colored(f"    ✅ Bridges: {'PASS' if test_results['bridge_test'] else 'FAIL'}", Colors.OKGREEN if test_results["bridge_test"] else Colors.FAIL)
        except Exception as e:
            print_colored(f"    ❌ Bridge test failed: {e}", Colors.FAIL)
            
        # Test Knowledge Manager
        try:
            print_colored("  📚 Testing Knowledge Manager...", Colors.YELLOW)
            km = enhanced_c64_knowledge_manager.EnhancedC64KnowledgeManager()
            total_entries = km.get_total_entries()
            test_results["knowledge_manager_test"] = total_entries > 500
            print_colored(f"    ✅ Knowledge Manager: {'PASS' if test_results['knowledge_manager_test'] else 'FAIL'} ({total_entries} entries)", Colors.OKGREEN if test_results["knowledge_manager_test"] else Colors.FAIL)
        except Exception as e:
            print_colored(f"    ❌ Knowledge Manager test failed: {e}", Colors.FAIL)
            
        # Summary
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        print_colored(f"\n🏆 Test Summary: {passed_tests}/{total_tests} tests passed", Colors.OKGREEN if passed_tests == total_tests else Colors.WARNING)
        
        if args.json_output:
            test_results["summary"] = {"passed": passed_tests, "total": total_tests, "success_rate": passed_tests/total_tests}
            print(json.dumps(test_results, indent=2))

def handle_information(args, logger):
    """Information operations handler"""
    
    if args.help_all:
        print_colored("📚 D64 Converter v6.0 - Comprehensive Help", Colors.HEADER + Colors.BOLD)
        print_colored("=" * 60, Colors.HEADER)
        
        help_sections = {
            "🔍 Analysis Features": [
                "• D64 disk image analysis and file extraction",
                "• PRG file disassembly with 8 format support",
                "• BASIC program analysis and tokenization",
                "• Performance analysis with cycle counting",
                "• Hardware register usage detection"
            ],
            "🔄 Transpilation Features": [
                "• Assembly → C/QBasic/Python/JavaScript/Pascal",
                "• Hardware-aware transpilation with register info",
                "• Multiple quality levels (Basic to Production)",
                "• Enhanced C64 Knowledge Manager integration",
                "• Format-specific optimizations"
            ],
            "🔌 Plugin System": [
                "• 5 plugin types: Format, Transpiler, Analyzer, Export, Tool",
                "• Plugin discovery and auto-loading",
                "• Template generation for new plugins",
                "• Comprehensive plugin management",
                "• Example plugins included"
            ],
            "🌉 Bridge Systems": [
                "• Assembly format conversion (8 formats)",
                "• Multi-language transpilation bridge",
                "• Decompiler integration pipeline",
                "• Format-specific optimization rules"
            ]
        }
        
        for section, features in help_sections.items():
            print_colored(f"\n{section}:", Colors.OKCYAN + Colors.BOLD)
            for feature in features:
                print_colored(f"  {feature}", Colors.OKGREEN)
                
    if args.list_formats:
        formats = ['native', 'kickassembler', 'tass', 'dasm', 'css64', 'supermon', 'acme', 'ca65']
        print_colored("🎨 Supported Assembly Formats:", Colors.OKCYAN)
        for fmt in formats:
            print_colored(f"  • {fmt}", Colors.OKGREEN)
            
    if args.list_targets:
        targets = ['c', 'qbasic', 'python', 'javascript', 'pascal']
        print_colored("🎯 Supported Transpilation Targets:", Colors.OKCYAN)
        for target in targets:
            print_colored(f"  • {target}", Colors.OKGREEN)
            
    if args.system_info:
        print_colored("💻 System Information:", Colors.OKCYAN)
        print(f"  Platform: {platform.platform()}")
        print(f"  Python: {sys.version}")
        print(f"  Working Directory: {os.getcwd()}")
        print(f"  D64 Converter: v6.0")

def main():
    """Ana program giriş noktası"""
    
    # Argument parsing
    parser = create_comprehensive_parser()
    args = parser.parse_args()
    
    # Color handling
    if args.no_color:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')
    
    # Header
    if not args.quiet:
        print_header()
    
    # Logging setup
    logger = setup_logging(args)
    
    # Load core modules
    if not load_core_modules():
        print_colored("❌ Failed to initialize system", Colors.FAIL)
        sys.exit(1)
    
    # Handle operations based on arguments
    try:
        # Basic operations
        handle_basic_operations(args, logger)
        
        # Transpilation
        handle_transpilation(args, logger)
        
        # Analysis
        handle_analysis(args, logger)
        
        # Plugins
        handle_plugins(args, logger)
        
        # Bridges
        handle_bridges(args, logger)
        
        # Testing
        handle_testing(args, logger)
        
        # Information
        handle_information(args, logger)
        
        # If no specific operation was requested, show help
        if len(sys.argv) == 1:
            parser.print_help()
            
    except KeyboardInterrupt:
        print_colored("\n⏹️ Operation cancelled by user", Colors.WARNING)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print_colored(f"❌ Unexpected error: {e}", Colors.FAIL)
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
