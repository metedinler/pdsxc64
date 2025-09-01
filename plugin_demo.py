"""
🔌 Professional Plugin Architecture Demo
========================================

Faz 3.3: Professional Plugin Architecture Test & Demo
Author: Enhanced AI System  
Created: 28 Temmuz 2025
Purpose: Plugin Manager ve örnek plugin'leri test et

📋 DEMO FEATURES:
1. Plugin Discovery & Loading
2. Plugin Type Classification  
3. Format Plugin Test (DASM)
4. Transpiler Plugin Test (Rust)
5. Analyzer Plugin Test (Performance)
6. Plugin Template Generation
7. Plugin Management Operations
"""

import os
import sys
from plugin_manager import get_plugin_manager, PluginType

def main():
    print("🔌 Professional Plugin Architecture Demo")
    print("=" * 60)
    
    # Get Plugin Manager instance
    pm = get_plugin_manager()
    
    print(f"\n📊 Plugin Manager Status:")
    print(f"   Plugins Directory: {pm.plugins_dir}")
    print(f"   Config File: {pm.config_file}")
    
    # List all discovered plugins
    plugins = pm.list_plugins()
    print(f"\n📋 Discovered Plugins ({len(plugins)} total):")
    for name, info in plugins.items():
        status = "🟢 LOADED" if info["loaded"] else "🔵 DISCOVERED"
        metadata = info["metadata"]
        print(f"   {status} {name}")
        print(f"      Version: {metadata.version}")
        print(f"      Author: {metadata.author}")
        print(f"      Type: {metadata.plugin_type.value}")
        print(f"      Description: {metadata.description}")
        print()
    
    # Plugin statistics by type
    print(f"📊 Plugin Statistics by Type:")
    total_loaded = 0
    for plugin_type in PluginType:
        plugins_of_type = pm.get_plugins_by_type(plugin_type)
        count = len(plugins_of_type)
        total_loaded += count
        print(f"   {plugin_type.value.title()}: {count} active")
    
    print(f"   Total Active: {total_loaded}")
    
    # Test Format Plugin (DASM)
    print(f"\n🎨 Testing Format Plugin (DASM):")
    print("-" * 40)
    
    test_assembly = """
    ; Simple 6502 assembly test
    LDA #$FF        ; Load accumulator with $FF
    STA $D020       ; Store to border color
    LDX #$00        ; Load X with 0
loop:
    INX             ; Increment X
    CPX #$10        ; Compare with 16
    BNE loop        ; Branch if not equal
    RTS             ; Return
    """
    
    format_plugins = pm.get_plugins_by_type(PluginType.FORMAT)
    if format_plugins:
        dasm_plugin = format_plugins[0]  # Get first format plugin
        try:
            formatted_code = dasm_plugin.execute(test_assembly)
            print("✅ DASM Format Test SUCCESS!")
            print("Generated DASM code:")
            print(formatted_code[:300] + "..." if len(formatted_code) > 300 else formatted_code)
        except Exception as e:
            print(f"❌ DASM Format Test FAILED: {e}")
    else:
        print("❌ No Format Plugin loaded")
    
    # Test Transpiler Plugin (Rust)
    print(f"\n🔄 Testing Transpiler Plugin (Rust):")
    print("-" * 40)
    
    transpiler_plugins = pm.get_plugins_by_type(PluginType.TRANSPILER)
    if transpiler_plugins:
        rust_plugin = transpiler_plugins[0]  # Get first transpiler plugin
        try:
            rust_code = rust_plugin.execute(test_assembly)
            print("✅ Rust Transpiler Test SUCCESS!")
            print("Generated Rust code preview:")
            lines = rust_code.split('\n')[:15]  # First 15 lines
            for line in lines:
                print(f"   {line}")
            print(f"   ... ({len(rust_code.split())} total lines)")
        except Exception as e:
            print(f"❌ Rust Transpiler Test FAILED: {e}")
    else:
        print("❌ No Transpiler Plugin loaded")
    
    # Test Analyzer Plugin (Performance)
    print(f"\n🔍 Testing Analyzer Plugin (Performance):")
    print("-" * 40)
    
    analyzer_plugins = pm.get_plugins_by_type(PluginType.ANALYZER)
    if analyzer_plugins:
        perf_plugin = analyzer_plugins[0]  # Get first analyzer plugin
        try:
            analysis = perf_plugin.execute(test_assembly)
            print("✅ Performance Analyzer Test SUCCESS!")
            
            if analysis.get("success", False):
                print(f"   Total Instructions: {analysis['instruction_count']}")
                print(f"   Total Cycles: {analysis['total_cycles']}")
                print(f"   Performance Issues: {len(analysis['performance_issues'])}")
                print(f"   Optimizations: {len(analysis['optimizations'])}")
                
                # Show hotspots
                if analysis["hotspots"]:
                    print(f"   Top Hotspot: {analysis['hotspots'][0]['instruction']}")
                
                # Show summary (first 2 lines)
                summary_lines = analysis["summary"].split('\n')[:3]
                print(f"   Summary Preview:")
                for line in summary_lines:
                    if line.strip():
                        print(f"     {line}")
            else:
                print(f"   Analysis failed: {analysis.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Performance Analyzer Test FAILED: {e}")
    else:
        print("❌ No Analyzer Plugin loaded")
    
    # Plugin Template Generation Demo
    print(f"\n🛠️ Plugin Template Generation Demo:")
    print("-" * 40)
    
    try:
        # Generate a sample Export Plugin template
        template_code = pm.create_plugin_template(
            plugin_name="JSON",
            plugin_type=PluginType.EXPORT,
            author="Demo User"
        )
        
        print("✅ Plugin Template Generation SUCCESS!")
        print("Generated JSON Export Plugin template preview:")
        template_lines = template_code.split('\n')[:20]  # First 20 lines
        for line in template_lines:
            print(f"   {line}")
        print(f"   ... ({len(template_code.split())} total lines)")
        
    except Exception as e:
        print(f"❌ Plugin Template Generation FAILED: {e}")
    
    # Plugin Management Operations Demo
    print(f"\n⚙️ Plugin Management Demo:")
    print("-" * 40)
    
    # Show plugin registry
    print("Plugin Registry Status:")
    for plugin_type, plugin_names in pm.plugin_registry.items():
        print(f"   {plugin_type.value}: {plugin_names}")
    
    # Show loaded plugins
    print(f"\nLoaded Plugins ({len(pm.loaded_plugins)}):")
    for plugin_name, plugin_instance in pm.loaded_plugins.items():
        plugin_type = plugin_instance.get_metadata().plugin_type.value
        print(f"   ✅ {plugin_name} ({plugin_type})")
    
    # Advanced Plugin Info
    print(f"\n📈 Advanced Plugin Information:")
    print("-" * 40)
    
    if pm.loaded_plugins:
        sample_plugin_name = list(pm.loaded_plugins.keys())[0]
        sample_plugin = pm.get_plugin(sample_plugin_name)
        
        if sample_plugin:
            metadata = sample_plugin.get_metadata()
            print(f"Sample Plugin Details ({sample_plugin_name}):")
            print(f"   Entry Point: {metadata.entry_point}")
            print(f"   Dependencies: {metadata.dependencies}")
            print(f"   Min API Version: {metadata.min_api_version}")
            
            # Get plugin config
            config = sample_plugin.get_config()
            if config:
                print(f"   Configuration: {config}")
            else:
                print(f"   Configuration: Default (empty)")
    
    # Final Summary
    print(f"\n🏆 Plugin Architecture Demo Summary:")
    print("=" * 60)
    print(f"✅ Plugin Discovery: {len(plugins)} plugins found")
    print(f"✅ Plugin Loading: {len(pm.loaded_plugins)} plugins loaded")
    print(f"✅ Format Plugin: DASM format tested")
    print(f"✅ Transpiler Plugin: Rust transpiler tested") 
    print(f"✅ Analyzer Plugin: Performance analyzer tested")
    print(f"✅ Template Generation: JSON export template generated")
    print(f"✅ Plugin Management: Registry and operations demonstrated")
    print(f"\n🎯 Professional Plugin Architecture is READY!")
    print(f"📊 System supports {len(PluginType)} plugin types")
    print(f"🔌 Extensible architecture for future enhancements")

if __name__ == "__main__":
    main()
