# c64_basic_parser.py
import subprocess
import logging
from basic_detokenizer import BasicDetokenizer

try:
    from pdsXv12_minimal import pdsXv12Final
except ImportError:
    print("Uyarı: pdsXv12_minimal modülü bulunamadı. Bazı özellikler çalışmayabilir.")
    pdsXv12Final = None

# Logging yapılandırması
logging.basicConfig(filename='logs/d64_converter.log', level=logging.ERROR)

class C64BasicParser:
    def __init__(self):
        if pdsXv12Final:
            self.interpreter = pdsXv12Final()
        else:
            self.interpreter = None
        
        # Yeni BASIC detokenizer
        self.detokenizer = BasicDetokenizer()
        
        # Eski token map - backwards compatibility
        self.token_map = {
            0x99: "PRINT", 0x8F: "INPUT", 0x8A: "GOTO", 0x89: "GOSUB",
            0xA2: "RETURN", 0x9B: "IF", 0x8D: "FOR", 0x8E: "NEXT",
            0xA7: "DATA", 0xA8: "READ", 0xA9: "RESTORE"
        }

    def detokenize(self, prg_data):
        """PRG dosyasını detokenize eder - yeni BasicDetokenizer kullanır"""
        try:
            # Yeni detokenizer ile işle
            lines = self.detokenizer.detokenize_prg(prg_data)
            return lines
            
        except Exception as e:
            logging.error(f"Detokenize hatası: {e}")
            
            # Fallback: petcat kullanmaya çalış
            try:
                with open("temp.prg", "wb") as f:
                    f.write(prg_data)
                result = subprocess.run(["petcat", "-w2", "-o", "temp.txt", "--", "temp.prg"],
                                       capture_output=True, text=True)
                with open("temp.txt", "r") as f:
                    lines = f.readlines()
                return lines
            except Exception as e2:
                logging.error(f"Petcat fallback hatası: {e2}")
                return [f"ERROR: Detokenization failed: {e}"]

    def transpile(self, basic_lines, output_type="pdsx"):
        """C64 BASIC kodunu farklı formatlara çevirir"""
        try:
            # Yeni detokenizer'ın transpile fonksiyonunu kullan
            return self.detokenizer.transpile_to_format(basic_lines, output_type)
            
        except Exception as e:
            logging.error(f"Transpile hatası: {e}")
            return f"ERROR: Transpilation failed: {e}"
