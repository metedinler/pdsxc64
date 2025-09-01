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
            result = subprocess.run(["petcat", "-w2", "-o", "temp.txt", "--", "temp.prg"],
                                   capture_output=True, text=True)
            with open("temp.txt", "r") as f:
                lines = f.readlines()
            return lines
        except Exception as e:
            logging.error(f"Detokenize hatası: {e}")
            return None

    def transpile(self, basic_lines, output_type="pdsx"):
        """C64 BASIC kodunu pdsX, QBasic64 veya C’ye çevirir."""
        try:
            output = []
            for line in basic_lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 1)
                if len(parts) < 2:
                    continue
                line_num, code = parts
                tokens = code.split(":")
                for token in tokens:
                    token = token.strip()
                    if token.startswith("PRINT"):
                        if output_type == "pdsx":
                            output.append(f"PRINT {token[5:].strip()}")
                        elif output_type == "qbasic":
                            output.append(f"PRINT {token[5:].strip()}")
                        else:
                            output.append(f'printf({token[5:].strip()});')
                    elif token.startswith("INPUT"):
                        if output_type == "pdsx":
                            output.append(f"INPUT {token[5:].strip()}")
                        elif output_type == "qbasic":
                            output.append(f"INPUT {token[5:].strip()}")
                        else:
                            output.append(f'scanf("%d", &{token[5:].strip()});')
                    elif token.startswith("GOTO"):
                        if output_type == "pdsx":
                            output.append(f"GOTO label_{token[4:].strip()}")
                        elif output_type == "qbasic":
                            output.append(f"GOTO label_{token[4:].strip()}")
                        else:
                            output.append(f'goto label_{token[4:].strip()};')
                    elif token.startswith("GOSUB"):
                        if output_type == "pdsx":
                            output.append(f"GOSUB label_{token[5:].strip()}")
                        elif output_type == "qbasic":
                            output.append(f"GOSUB label_{token[5:].strip()}")
                        else:
                            output.append(f'func_{token[5:].strip()}();')
                    elif token.startswith("RETURN"):
                        if output_type == "pdsx":
                            output.append("RETURN")
                        elif output_type == "qbasic":
                            output.append("RETURN")
                        else:
                            output.append("return;")
                    elif token.startswith("IF"):
                        condition = token[2:].split("THEN")[0].strip()
                        action = token.split("THEN")[1].strip()
                        if output_type == "pdsx":
                            output.append(f"IF {condition} THEN {action}")
                        elif output_type == "qbasic":
                            output.append(f"IF {condition} THEN {action}")
                        else:
                            output.append(f'if ({condition}) {{ {action}; }}')
                    elif token.startswith("FOR"):
                        parts = token[3:].split("TO")
                        var, range_end = parts[0].strip(), parts[1].strip()
                        if output_type == "pdsx":
                            output.append(f"FOR {var} = 0 TO {range_end}")
                        elif output_type == "qbasic":
                            output.append(f"FOR {var} = 0 TO {range_end}")
                        else:
                            output.append(f'for (int {var} = 0; {var} <= {range_end}; {var}++) {{')
                    elif token.startswith("NEXT"):
                        if output_type == "pdsx":
                            output.append("NEXT")
                        elif output_type == "qbasic":
                            output.append("NEXT")
                        else:
                            output.append("}")
                    elif token.startswith("DATA"):
                        if output_type == "pdsx":
                            output.append(f"DATA {token[4:].strip()}")
                        elif output_type == "qbasic":
                            output.append(f"DATA {token[4:].strip()}")
                        else:
                            output.append(f'int data[] = {{{token[4:].strip()}}};')
                    elif token.startswith("READ"):
                        if output_type == "pdsx":
                            output.append(f"READ {token[4:].strip()}")
                        elif output_type == "qbasic":
                            output.append(f"READ {token[4:].strip()}")
                        else:
                            output.append(f'read_data(&{token[4:].strip()});')
                    elif token.startswith("RESTORE"):
                        if output_type == "pdsx":
                            output.append("RESTORE")
                        elif output_type == "qbasic":
                            output.append("RESTORE")
                        else:
                            output.append("reset_data_pointer();")
            return "\n".join(output)
        except Exception as e:
            logging.error(f"Transpile hatası: {e}")
            return None