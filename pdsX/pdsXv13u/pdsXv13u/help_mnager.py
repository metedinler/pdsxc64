import json
import os

class PdsXException(Exception):
    pass

class HelpManager:
    def __init__(self, help_file="help_data.json"):
        self.help_file = help_file
        self.help_data = self._load_help_data()

    def _load_help_data(self):
        """help_data.json dosyasını yükler"""
        if not os.path.exists(self.help_file):
            raise PdsXException(f"Yardım dosyası bulunamadı: {self.help_file}")
        with open(self.help_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def show_help(self, name=None):
        """Belirtilen komut veya fonksiyon için yardım bilgisi gösterir"""
        if name is None:
            return self._show_general_help()
        
        name = name.upper()
        for cmd in self.help_data.get("commands", []):
            if cmd["name"].upper() == name:
                return self._format_help(cmd)
        for func in self.help_data.get("functions", []):
            if func["name"].upper() == name:
                return self._format_help(func)
        return f"Yardım bilgisi bulunamadı: {name}"

    def _show_general_help(self):
        """Genel yardım bilgisi gösterir"""
        return (
            "Kullanım: HELP [komut_adı | fonksiyon_adı]\n"
            "Örnek: HELP PRINT\n"
            "Mevcut komutlar ve fonksiyonlar için HELP dosyasına bakın."
        )

    def _format_help(self, item):
        """Yardım bilgisini formatlar"""
        return (
            f"Ad: {item['name']}\n"
            f"Kullanım: {item['usage']}\n"
            f"Amaç: {item['purpose']}\n"
            f"Örnek: {item['example']}\n"
            f"{'-' * 50}"
        )