"""
🔌 Professional Plugin Architecture for D64 Converter
====================================================

Faz 3.3: Professional Plugin Architecture Implementation
Author: Enhanced AI System
Created: 28 Temmuz 2025
Purpose: Genişletilebilir plugin sistemi ile modüler mimari

📋 PLUGIN TÜRLERİ:
- 🎨 Format Plugins: Yeni disassembly formatları
- 🔄 Transpiler Plugins: Yeni hedef diller
- 🔍 Analyzer Plugins: Özel analiz araçları  
- 📤 Export Plugins: Farklı çıktı formatları
- 🛠️ Tool Plugins: Özel araçlar ve yardımcılar

🏗️ Plugin Interface Requirements:
1. Plugin metadata (name, version, author, description)
2. Plugin type classification
3. Dependency management
4. Plugin lifecycle (load, init, execute, cleanup)
5. Error handling and logging
6. Plugin discovery and auto-loading
"""

import os
import sys
import json
import importlib
import importlib.util
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Type, Callable
from dataclasses import dataclass
from pathlib import Path
import logging
from enum import Enum

# Plugin Types Enum
class PluginType(Enum):
    FORMAT = "format"
    TRANSPILER = "transpiler"
    ANALYZER = "analyzer"
    EXPORT = "export"
    TOOL = "tool"

@dataclass
class PluginMetadata:
    """Plugin metadata structure"""
    name: str
    version: str
    author: str
    description: str
    plugin_type: PluginType
    dependencies: List[str]
    entry_point: str
    config_schema: Optional[Dict] = None
    min_api_version: str = "1.0.0"
    
class IPlugin(ABC):
    """Base Plugin Interface - Tüm pluginler bu interface'i implement etmeli"""
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Plugin metadata döndür"""
        pass
    
    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Plugin'i başlat - True: başarılı, False: başarısız"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevini çalıştır"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Plugin cleanup işlemleri"""
        pass
    
    def get_config(self) -> Dict[str, Any]:
        """Plugin config döndür (optional)"""
        return {}

class IFormatPlugin(IPlugin):
    """Format Plugin Interface"""
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Format adını döndür (örn: "KickAssembler", "TASS", "DASM")"""
        pass
    
    @abstractmethod
    def format_assembly(self, assembly_code: str, options: Dict[str, Any] = None) -> str:
        """Assembly kodunu belirli formata çevir"""
        pass
    
    @abstractmethod
    def parse_assembly(self, formatted_code: str) -> Dict[str, Any]:
        """Formatlanmış assembly'yi parse et"""
        pass

class ITranspilerPlugin(IPlugin):
    """Transpiler Plugin Interface"""
    
    @abstractmethod
    def get_target_language(self) -> str:
        """Hedef dil adını döndür (örn: "C++", "Rust", "C#")"""
        pass
    
    @abstractmethod
    def transpile(self, assembly_code: str, options: Dict[str, Any] = None) -> str:
        """Assembly'yi hedef dile çevir"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Çıktı dosya uzantısı (örn: ".cpp", ".rs", ".cs")"""
        pass

class IAnalyzerPlugin(IPlugin):
    """Analyzer Plugin Interface"""
    
    @abstractmethod
    def get_analysis_type(self) -> str:
        """Analiz türünü döndür (örn: "Performance", "Security", "Optimization")"""
        pass
    
    @abstractmethod
    def analyze(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Kod analizi yap ve sonuçları döndür"""
        pass

class IExportPlugin(IPlugin):
    """Export Plugin Interface"""
    
    @abstractmethod
    def get_export_format(self) -> str:
        """Export format adını döndür (örn: "PDF", "HTML", "XML")"""
        pass
    
    @abstractmethod
    def export(self, data: Any, output_path: str, options: Dict[str, Any] = None) -> bool:
        """Veriyi belirtilen formatta export et"""
        pass

class IToolPlugin(IPlugin):
    """Tool Plugin Interface"""
    
    @abstractmethod
    def get_tool_name(self) -> str:
        """Tool adını döndür"""
        pass
    
    @abstractmethod
    def run_tool(self, input_data: Any, options: Dict[str, Any] = None) -> Any:
        """Tool'u çalıştır"""
        pass

class PluginManager:
    """🔌 Professional Plugin Manager"""
    
    def __init__(self, plugins_dir: str = "plugins", config_file: str = "plugin_config.json"):
        self.plugins_dir = Path(plugins_dir)
        self.config_file = config_file
        self.loaded_plugins: Dict[str, IPlugin] = {}
        self.plugin_registry: Dict[PluginType, List[str]] = {
            PluginType.FORMAT: [],
            PluginType.TRANSPILER: [],
            PluginType.ANALYZER: [],
            PluginType.EXPORT: [],
            PluginType.TOOL: []
        }
        
        # Logging setup
        self.logger = logging.getLogger("PluginManager")
        self.logger.setLevel(logging.INFO)
        
        # Plugin discovery cache
        self.discovery_cache: Dict[str, PluginMetadata] = {}
        
        # Create plugins directory if not exists
        self.plugins_dir.mkdir(exist_ok=True)
        
        # Initialize plugin manager
        self._initialize()
    
    def _initialize(self):
        """Plugin Manager'ı başlat"""
        self.logger.info("🔌 Plugin Manager başlatılıyor...")
        
        # Load configuration
        self._load_config()
        
        # Discover plugins
        self._discover_plugins()
        
        # Auto-load enabled plugins
        self._auto_load_plugins()
        
        self.logger.info(f"✅ Plugin Manager hazır - {len(self.loaded_plugins)} plugin yüklendi")
    
    def _load_config(self):
        """Plugin configuration yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "auto_load": True,
                    "enabled_plugins": [],
                    "disabled_plugins": [],
                    "plugin_settings": {}
                }
                self._save_config()
        except Exception as e:
            self.logger.error(f"❌ Config yükleme hatası: {e}")
            self.config = {}
    
    def _save_config(self):
        """Plugin configuration kaydet"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"❌ Config kaydetme hatası: {e}")
    
    def _discover_plugins(self):
        """Plugin'leri keşfet ve metadata'larını oku"""
        self.logger.info("🔍 Plugin keşfi başlatılıyor...")
        
        for plugin_file in self.plugins_dir.rglob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            try:
                metadata = self._read_plugin_metadata(plugin_file)
                if metadata:
                    self.discovery_cache[metadata.name] = metadata
                    self.logger.info(f"✅ Plugin keşfedildi: {metadata.name} v{metadata.version}")
            except Exception as e:
                self.logger.error(f"❌ Plugin keşif hatası ({plugin_file}): {e}")
    
    def _read_plugin_metadata(self, plugin_file: Path) -> Optional[PluginMetadata]:
        """Plugin dosyasından metadata oku"""
        try:
            spec = importlib.util.spec_from_file_location("temp_plugin", plugin_file)
            if not spec or not spec.loader:
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Plugin class'ını bul
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, IPlugin) and 
                    attr != IPlugin):
                    
                    # Temporary instance oluştur ve metadata al
                    try:
                        temp_instance = attr()
                        metadata = temp_instance.get_metadata()
                        temp_instance.cleanup()
                        return metadata
                    except Exception as e:
                        self.logger.warning(f"⚠️ Plugin metadata okuma hatası: {e}")
                        continue
                        
            return None
        except Exception as e:
            self.logger.error(f"❌ Plugin dosya okuma hatası: {e}")
            return None
    
    def _auto_load_plugins(self):
        """Enabled plugin'leri otomatik yükle"""
        if not self.config.get("auto_load", True):
            return
            
        for plugin_name, metadata in self.discovery_cache.items():
            if (plugin_name not in self.config.get("disabled_plugins", []) and
                (not self.config.get("enabled_plugins") or 
                 plugin_name in self.config.get("enabled_plugins", []))):
                
                try:
                    self.load_plugin(plugin_name)
                except Exception as e:
                    self.logger.error(f"❌ Auto-load hatası ({plugin_name}): {e}")
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Plugin'i yükle"""
        if plugin_name in self.loaded_plugins:
            self.logger.warning(f"⚠️ Plugin zaten yüklü: {plugin_name}")
            return True
            
        if plugin_name not in self.discovery_cache:
            self.logger.error(f"❌ Plugin bulunamadı: {plugin_name}")
            return False
            
        try:
            metadata = self.discovery_cache[plugin_name]
            
            # Plugin dosyasını bul
            plugin_file = None
            for pfile in self.plugins_dir.rglob("*.py"):
                if self._get_plugin_name_from_file(pfile) == plugin_name:
                    plugin_file = pfile
                    break
                    
            if not plugin_file:
                self.logger.error(f"❌ Plugin dosyası bulunamadı: {plugin_name}")
                return False
            
            # Plugin'i yükle
            spec = importlib.util.spec_from_file_location(f"plugin_{plugin_name}", plugin_file)
            if not spec or not spec.loader:
                self.logger.error(f"❌ Plugin spec oluşturulamadı: {plugin_name}")
                return False
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Plugin class'ını bul ve instance oluştur
            plugin_instance = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, IPlugin) and 
                    attr != IPlugin):
                    
                    plugin_instance = attr()
                    break
            
            if not plugin_instance:
                self.logger.error(f"❌ Plugin class bulunamadı: {plugin_name}")
                return False
            
            # Plugin'i initialize et
            context = {
                "plugin_manager": self,
                "config": self.config.get("plugin_settings", {}).get(plugin_name, {}),
                "workspace_dir": os.getcwd()
            }
            
            if not plugin_instance.initialize(context):
                self.logger.error(f"❌ Plugin initialize hatası: {plugin_name}")
                return False
            
            # Plugin'i kaydet
            self.loaded_plugins[plugin_name] = plugin_instance
            self.plugin_registry[metadata.plugin_type].append(plugin_name)
            
            self.logger.info(f"✅ Plugin yüklendi: {plugin_name} ({metadata.plugin_type.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Plugin yükleme hatası ({plugin_name}): {e}")
            return False
    
    def _get_plugin_name_from_file(self, plugin_file: Path) -> Optional[str]:
        """Plugin dosyasından plugin adını al"""
        try:
            metadata = self._read_plugin_metadata(plugin_file)
            return metadata.name if metadata else None
        except:
            return None
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Plugin'i kaldır"""
        if plugin_name not in self.loaded_plugins:
            self.logger.warning(f"⚠️ Plugin yüklü değil: {plugin_name}")
            return False
            
        try:
            plugin = self.loaded_plugins[plugin_name]
            plugin.cleanup()
            
            # Registry'den kaldır
            metadata = self.discovery_cache.get(plugin_name)
            if metadata:
                if plugin_name in self.plugin_registry[metadata.plugin_type]:
                    self.plugin_registry[metadata.plugin_type].remove(plugin_name)
            
            # Loaded plugins'den kaldır
            del self.loaded_plugins[plugin_name]
            
            self.logger.info(f"✅ Plugin kaldırıldı: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Plugin kaldırma hatası ({plugin_name}): {e}")
            return False
    
    def get_plugins_by_type(self, plugin_type: PluginType) -> List[IPlugin]:
        """Belirli türdeki plugin'leri döndür"""
        plugins = []
        for plugin_name in self.plugin_registry[plugin_type]:
            if plugin_name in self.loaded_plugins:
                plugins.append(self.loaded_plugins[plugin_name])
        return plugins
    
    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        """Plugin instance'ını döndür"""
        return self.loaded_plugins.get(plugin_name)
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Tüm plugin'leri listele"""
        result = {}
        
        for plugin_name, metadata in self.discovery_cache.items():
            is_loaded = plugin_name in self.loaded_plugins
            result[plugin_name] = {
                "metadata": metadata,
                "loaded": is_loaded,
                "status": "LOADED" if is_loaded else "DISCOVERED"
            }
            
        return result
    
    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        """Plugin'i çalıştır"""
        if plugin_name not in self.loaded_plugins:
            raise ValueError(f"Plugin yüklü değil: {plugin_name}")
            
        plugin = self.loaded_plugins[plugin_name]
        return plugin.execute(*args, **kwargs)
    
    def create_plugin_template(self, plugin_name: str, plugin_type: PluginType, 
                             author: str = "Unknown") -> str:
        """Yeni plugin template'i oluştur"""
        template_map = {
            PluginType.FORMAT: self._create_format_plugin_template,
            PluginType.TRANSPILER: self._create_transpiler_plugin_template,
            PluginType.ANALYZER: self._create_analyzer_plugin_template,
            PluginType.EXPORT: self._create_export_plugin_template,
            PluginType.TOOL: self._create_tool_plugin_template
        }
        
        template_func = template_map.get(plugin_type)
        if not template_func:
            raise ValueError(f"Desteklenmeyen plugin türü: {plugin_type}")
            
        return template_func(plugin_name, author)
    
    def _create_format_plugin_template(self, plugin_name: str, author: str) -> str:
        """Format Plugin template'i oluştur"""
        template = '''"""
{plugin_name} Format Plugin
========================

Author: {author}
Plugin Type: Format
Description: {plugin_name} format desteği
"""

from typing import Dict, Any
from plugin_manager import IFormatPlugin, PluginMetadata, PluginType

class {plugin_name}FormatPlugin(IFormatPlugin):
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name}_format",
            version="1.0.0",
            author="{author}",
            description="{plugin_name} format plugin",
            plugin_type=PluginType.FORMAT,
            dependencies=[],
            entry_point="{plugin_name}FormatPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        # Plugin initialization code here
        return True
    
    def cleanup(self) -> None:
        # Cleanup code here
        pass
    
    def get_format_name(self) -> str:
        return "{plugin_name}"
    
    def format_assembly(self, assembly_code: str, options: Dict[str, Any] = None) -> str:
        """Assembly kodunu {plugin_name} formatına çevir"""
        # Format implementation here
        return assembly_code
    
    def parse_assembly(self, formatted_code: str) -> Dict[str, Any]:
        """Formatlanmış assembly'yi parse et"""
        # Parse implementation here
        return {{"success": True, "parsed_data": {{}}}}
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        return self.format_assembly(*args, **kwargs)
'''
        return template.format(plugin_name=plugin_name, author=author)
    
    def _create_transpiler_plugin_template(self, plugin_name: str, author: str) -> str:
        """Transpiler Plugin template'i oluştur"""
        template = '''"""
{plugin_name} Transpiler Plugin
============================

Author: {author}
Plugin Type: Transpiler
Description: Assembly → {plugin_name} transpiler
"""

from typing import Dict, Any
from plugin_manager import ITranspilerPlugin, PluginMetadata, PluginType

class {plugin_name}TranspilerPlugin(ITranspilerPlugin):
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name}_transpiler",
            version="1.0.0",
            author="{author}",
            description="Assembly to {plugin_name} transpiler",
            plugin_type=PluginType.TRANSPILER,
            dependencies=[],
            entry_point="{plugin_name}TranspilerPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        # Plugin initialization code here
        return True
    
    def cleanup(self) -> None:
        # Cleanup code here
        pass
    
    def get_target_language(self) -> str:
        return "{plugin_name}"
    
    def get_file_extension(self) -> str:
        return ".{plugin_name_lower}"
    
    def transpile(self, assembly_code: str, options: Dict[str, Any] = None) -> str:
        """Assembly'yi {plugin_name}'e çevir"""
        # Transpiler implementation here
        return "// Generated {plugin_name} code\\n// Original assembly:\\n/* " + str(assembly_code) + " */"
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        return self.transpile(*args, **kwargs)
'''
        return template.format(plugin_name=plugin_name, author=author, plugin_name_lower=plugin_name.lower())
    
    def _create_analyzer_plugin_template(self, plugin_name: str, author: str) -> str:
        """Analyzer Plugin template'i oluştur"""
        template = '''"""
{plugin_name} Analyzer Plugin
==========================

Author: {author}
Plugin Type: Analyzer
Description: {plugin_name} kod analizi
"""

from typing import Dict, Any
from plugin_manager import IAnalyzerPlugin, PluginMetadata, PluginType

class {plugin_name}AnalyzerPlugin(IAnalyzerPlugin):
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name}_analyzer",
            version="1.0.0",
            author="{author}",
            description="{plugin_name} code analyzer",
            plugin_type=PluginType.ANALYZER,
            dependencies=[],
            entry_point="{plugin_name}AnalyzerPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        # Plugin initialization code here
        return True
    
    def cleanup(self) -> None:
        # Cleanup code here
        pass
    
    def get_analysis_type(self) -> str:
        return "{plugin_name}"
    
    def analyze(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """{plugin_name} analizi yap"""
        # Analysis implementation here
        return {{
            "analysis_type": "{plugin_name}",
            "results": [],
            "summary": "Analysis completed",
            "success": True
        }}
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        return self.analyze(*args, **kwargs)
'''
        return template.format(plugin_name=plugin_name, author=author)
    
    def _create_export_plugin_template(self, plugin_name: str, author: str) -> str:
        """Export Plugin template'i oluştur"""
        template = '''"""
{plugin_name} Export Plugin
========================

Author: {author}
Plugin Type: Export
Description: {plugin_name} format export
"""

from typing import Dict, Any
from plugin_manager import IExportPlugin, PluginMetadata, PluginType

class {plugin_name}ExportPlugin(IExportPlugin):
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name}_export",
            version="1.0.0",
            author="{author}",
            description="{plugin_name} format exporter",
            plugin_type=PluginType.EXPORT,
            dependencies=[],
            entry_point="{plugin_name}ExportPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        # Plugin initialization code here
        return True
    
    def cleanup(self) -> None:
        # Cleanup code here
        pass
    
    def get_export_format(self) -> str:
        return "{plugin_name}"
    
    def export(self, data: Any, output_path: str, options: Dict[str, Any] = None) -> bool:
        """Veriyi {plugin_name} formatında export et"""
        try:
            # Export implementation here
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("Exported to {plugin_name} format\\n")
                f.write(str(data))
            return True
        except Exception as e:
            print("Export error: " + str(e))
            return False
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        return self.export(*args, **kwargs)
'''
        return template.format(plugin_name=plugin_name, author=author)
    
    def _create_tool_plugin_template(self, plugin_name: str, author: str) -> str:
        """Tool Plugin template'i oluştur"""
        template = '''"""
{plugin_name} Tool Plugin
=====================

Author: {author}
Plugin Type: Tool
Description: {plugin_name} tool
"""

from typing import Dict, Any
from plugin_manager import IToolPlugin, PluginMetadata, PluginType

class {plugin_name}ToolPlugin(IToolPlugin):
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name}_tool",
            version="1.0.0",
            author="{author}",
            description="{plugin_name} tool plugin",
            plugin_type=PluginType.TOOL,
            dependencies=[],
            entry_point="{plugin_name}ToolPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        # Plugin initialization code here
        return True
    
    def cleanup(self) -> None:
        # Cleanup code here
        pass
    
    def get_tool_name(self) -> str:
        return "{plugin_name}"
    
    def run_tool(self, input_data: Any, options: Dict[str, Any] = None) -> Any:
        """{plugin_name} tool'unu çalıştır"""
        # Tool implementation here
        return {{
            "tool_name": "{plugin_name}",
            "input_data": input_data,
            "result": "Tool executed successfully",
            "success": True
        }}
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        return self.run_tool(*args, **kwargs)
'''
        return template.format(plugin_name=plugin_name, author=author)

# Plugin Manager Singleton Instance
_plugin_manager_instance = None

def get_plugin_manager() -> PluginManager:
    """Global Plugin Manager instance'ını döndür"""
    global _plugin_manager_instance
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
    return _plugin_manager_instance

# Example Usage & Demo
if __name__ == "__main__":
    print("🔌 Professional Plugin Architecture Demo")
    print("=" * 50)
    
    # Plugin Manager oluştur
    pm = PluginManager()
    
    # Plugin'leri listele
    plugins = pm.list_plugins()
    print(f"\n📋 Keşfedilen Plugin'ler ({len(plugins)} adet):")
    for name, info in plugins.items():
        status = "🟢 LOADED" if info["loaded"] else "🔵 DISCOVERED"
        print(f"  {status} {name} v{info['metadata'].version} ({info['metadata'].plugin_type.value})")
    
    # Plugin türlerine göre göster
    print(f"\n📊 Plugin Türleri:")
    for plugin_type in PluginType:
        count = len(pm.plugin_registry[plugin_type])
        print(f"  {plugin_type.value.title()}: {count} adet")
    
    print(f"\n✅ Plugin Manager hazır - {len(pm.loaded_plugins)} plugin aktif")
