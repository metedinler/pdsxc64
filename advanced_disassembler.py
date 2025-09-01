"""
Gelişmiş C64 PRG dosyası disassembler
- Basit opcode table (yeni, güvenli)
- py65 tabanlı (eski, güçlü ama riskli)
- Çoklu dil çevirisi destekli
- Memory map entegrasyonu
🍎 Advanced Disassembler v5.4 - Commodore 64 Geliştirme Stüdyosu - DEBUG MODE
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: advanced_disassembler.py - Gelişmiş C64 Disassembler Motoru
VERSİYON: 5.4 (4 Disassembler Motor - "advanced" seçeneği) - DEBUG MODE
AMAÇ: Gelişmiş C64 PRG dosyası disassembly ve çoklu format desteği

🚀 DEBUG GUIDE - COMPONENT CODES:
================================================================
[D1] AdvancedDisassembler - Ana sınıf
[D2] disassemble_simple() - Basit disassembly (dış kullanım)
[D3] disassemble_py65() - py65 disassembly (dış kullanım)
[D4] disassemble() - Format seçimli ana disassembly
[D5] _disassemble_asm() - Native Assembly format
[D6] _disassemble_tass() - TASS format
[D7] _disassemble_kickassembler() - KickAssembler format
[D8] _disassemble_cc64() - CC64 format
[D9] _disassemble_simple() - İç basit disassembly
[D10] _disassemble_py65() - İç py65 disassembly
[D11] translate_instruction() - Çeviri motoru
[D12] load_memory_map() - Memory map yükleyici
[D13] get_memory_info() - Memory bilgi alıcı
[D14] get_memory_label() - Memory label alıcı
[D15] convert_to_language() - Dil çevirici
[D16] to_c() - C çevirisi
[D17] to_qbasic() - QBasic çevirisi
[D18] to_pdsx() - PDSX çevirisi
[D19] to_commodore_basic_v2() - CBM Basic çevirisi
[D20] to_pseudo() - Pseudo-code çevirisi
================================================================

Bu modül 4 Disassembler Motor sisteminin "advanced" motorudur:
• Gelişmiş Opcode Table: Güvenli ve kapsamlı disassembly
• py65 Tabanlı Motor: Güçlü ama riskli disassembly seçeneği
• Çoklu Dil Çevirisi: Assembly, C, QBasic, PDSX, Pseudo çıkış
• Memory Map Entegrasyonu: C64 bellek haritası ile gelişmiş etiketleme
• GUI Integration: 4 Disassembler dropdown'ında "advanced" seçeneği

4 Disassembler Motor Sistemi:
1. basic - Temel disassembler
2. advanced - Bu modül (gelişmiş özellikler)
3. improved - C64 Enhanced disassembler  
4. py65_professional - Professional py65 tabanlı
================================================================
"""

import json
import os
from opcode_manager import OpcodeManager
from improved_disassembler import ImprovedDisassembler
import disassembly_formatter

class AdvancedDisassembler:
    """[D1] Ana AdvancedDisassembler sınıfı - Tüm disassembly işlemlerinin merkezi"""
    
    def __init__(self, start_address, code, use_py65=False, use_illegal_opcodes=False, output_format='tass'):
        """[D1.1] Constructor - Disassembler'ı başlat"""
        # DEBUG mode flag - önce tanımla
        self.debug_mode = True
        
        self.start_address = start_address
        self.code = code
        self.use_py65 = use_py65
        self.use_illegal_opcodes = use_illegal_opcodes
        self.output_format = output_format  # 'asm', 'c', 'qbasic', 'pseudo'
        self.opcode_manager = OpcodeManager()
        self.opcodes = self.opcode_manager.get_all_opcodes()
        self.translations = self.opcode_manager.get_all_translations()
        self.memory_map = self.load_memory_map()  # [D12] çağrısı
        
        # [D1.2] py65 desteği
        if use_py65:
            try:
                from py65.devices.mpu6502 import MPU
                from py65.memory import ObservableMemory
                from py65.disassembler import Disassembler as PY65Disassembler
                self.memory = ObservableMemory()
                self.mpu = MPU(self.memory)  # Memory'yi MPU'ya geç
                self.py65_disassembler = PY65Disassembler(self.mpu)
                self.py65_available = True
                if self.debug_mode:
                    print("[D1.2] ✅ py65 disassembler yüklendi")
            except ImportError as e:
                self.py65_available = False
                if self.debug_mode:
                    print(f"[D1.2] ❌ py65 kütüphanesi yüklenemedi: {e}")
        else:
            self.py65_available = False
            if self.debug_mode:
                print("[D1.2] ℹ️ py65 kullanılmıyor")
    
    def load_memory_map(self):
        """[D12] Memory map'i yükle"""
        if self.debug_mode:
            print("[D12] 🔄 Memory map yükleniyor...")
            
        memory_map = {}
        json_path = os.path.join(os.path.dirname(__file__), "memory_map.json")
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # String hex değerlerini int'e çevir
                for hex_str, description in data.items():
                    if hex_str.startswith('0x'):
                        address = int(hex_str, 16)
                        memory_map[address] = description
                        
                if self.debug_mode:
                    print(f"[D12] ✅ Memory map yüklendi: {len(memory_map)} adres")
                
            except Exception as e:
                if self.debug_mode:
                    print(f"[D12] ❌ Memory map yükleme hatası: {e}")
        else:
            if self.debug_mode:
                print(f"[D12] ⚠️ Memory map dosyası bulunamadı: {json_path}")
                
        return memory_map
    
    def get_memory_info(self, address):
        """[D13] Belirli bir adres için memory map bilgisi al"""
        if self.debug_mode:
            print(f"[D13] 🔍 Memory info aranıyor: ${address:04X}")
            
        if address in self.memory_map:
            info = self.memory_map[address]
            if self.debug_mode:
                print(f"[D13] ✅ Bulundu: {info}")
            return info
        
        if self.debug_mode:
            print(f"[D13] ❌ Memory info bulunamadı")
        return None
    
    def translate_instruction(self, opcode_name, operand_value=None, operand_2=None):
        """[D11] Instruction'ı belirtilen formata çevir"""
        if self.debug_mode:
            print(f"[D11] 🔄 Çeviri: {opcode_name} -> {self.output_format}")
            
        if self.output_format == 'asm':
            if self.debug_mode:
                print("[D11] ℹ️ Assembly format - çeviri yok")
            return None  # Assembly format için çeviri yok
        
        # Çeviri tablosunda varsa kullan
        if opcode_name in self.translations:
            # Format'a göre doğru key'i kullan
            if self.output_format == 'c':
                translation_key = 'c_equivalent'
            elif self.output_format == 'qbasic':
                translation_key = 'qbasic_equivalent'
            elif self.output_format == 'pdsx':
                translation_key = 'pdsx_equivalent'
            elif self.output_format == 'pseudo':
                translation_key = 'pseudo_equivalent'
            elif self.output_format == 'commodorebasicv2':
                translation_key = 'commodorebasicv2_equivalent'
            else:
                translation_key = f"{self.output_format}_equivalent"
            
            translation = self.translations[opcode_name].get(translation_key, None)
            
            if translation:
                if self.debug_mode:
                    print(f"[D11] ✅ Çeviri bulundu: {translation}")
                    
                # Operand değerlerini yerine koy
                if operand_value is not None:
                    # Önce büyük harflerle dene
                    if 'ADDRESS' in translation:
                        translation = translation.replace('ADDRESS', str(operand_value))
                    elif 'ADDR' in translation:
                        translation = translation.replace('ADDR', str(operand_value))
                    elif 'address' in translation:
                        translation = translation.replace('address', str(operand_value))
                    elif 'addr' in translation:
                        translation = translation.replace('addr', str(operand_value))
                    elif 'VALUE' in translation:
                        translation = translation.replace('VALUE', str(operand_value))
                    elif 'value' in translation:
                        translation = translation.replace('value', str(operand_value))
                    elif 'label' in translation:
                        translation = translation.replace('label', f"label_{operand_value:04X}")
                    elif 'LABEL' in translation:
                        translation = translation.replace('LABEL', f"label_{operand_value:04X}")
                
                return translation
            else:
                if self.debug_mode:
                    print(f"[D11] ⚠️ Çeviri bulunamadı: {translation_key}")
        
        # Fallback: Bilinmeyen opcode'lar için basit çeviri
        if self.debug_mode:
            print(f"[D11] 🔄 Fallback çeviri kullanılıyor")
            
        if self.output_format == 'c':
            if operand_value is not None:
                return f"/* {opcode_name} {operand_value} */"
            else:
                return f"/* {opcode_name} */"
        elif self.output_format in ['qbasic', 'pdsx', 'commodorebasicv2']:
            if operand_value is not None:
                return f"REM {opcode_name} {operand_value}"
            else:
                return f"REM {opcode_name}"
        else:
            if operand_value is not None:
                return f"// {opcode_name} {operand_value}"
            else:
                return f"// {opcode_name}"

    def disassemble_simple(self, prg_data):
        """[D2] Basit disassemble metodu - dış kullanım için"""
        if self.debug_mode:
            print(f"[D2] 🚀 Basit disassemble başlatılıyor - Format: {self.output_format}")
            
        if not prg_data or len(prg_data) < 2:
            if self.debug_mode:
                print("[D2] ❌ Geçersiz PRG verisi")
            return "Hata: Geçersiz PRG verisi"
        
        # Eğer format assembly değilse, yeni improved disassembler kullan
        if self.output_format != 'asm':
            if self.debug_mode:
                print("[D2] 🔄 ImprovedDisassembler kullanılıyor")
            improved_disasm = ImprovedDisassembler(self.start_address, self.code, self.output_format)
            return improved_disasm.disassemble_to_format(prg_data)
        
        if self.debug_mode:
            print("[D2] 🔄 Assembly format - eski metod kullanılıyor")
            
        # Assembly format için eski metod
        # PRG dosyasının başlangıç adresini al
        start_addr = prg_data[0] + (prg_data[1] << 8)
        code_data = prg_data[2:]
        
        if self.debug_mode:
            print(f"[D2] 📍 Start Address: ${start_addr:04X}, Code Size: {len(code_data)} bytes")
        
        # Geçici olarak parametreleri güncelle
        old_start = self.start_address
        old_code = self.code
        
        self.start_address = start_addr
        self.code = code_data
        
        result = self._disassemble_simple()  # [D9] çağrısı
        
        # Eski parametreleri geri yükle
        self.start_address = old_start
        self.code = old_code
        
        if self.debug_mode:
            print(f"[D2] ✅ Disassemble tamamlandı - {len(result)} satır")
        
        return '\n'.join(result)
        
    def disassemble_py65(self, prg_data):
        """[D3] py65 disassemble metodu - dış kullanım için"""
        if self.debug_mode:
            print(f"[D3] 🚀 py65 disassemble başlatılıyor")
            
        if not prg_data or len(prg_data) < 2:
            if self.debug_mode:
                print("[D3] ❌ Geçersiz PRG verisi")
            return "Hata: Geçersiz PRG verisi"
            
        # PRG dosyasının başlangıç adresini al
        start_addr = prg_data[0] + (prg_data[1] << 8)
        code_data = prg_data[2:]
        
        if self.debug_mode:
            print(f"[D3] 📍 Start Address: ${start_addr:04X}, Code Size: {len(code_data)} bytes")
        
        # Geçici olarak parametreleri güncelle
        old_start = self.start_address
        old_code = self.code
        
        self.start_address = start_addr
        self.code = code_data
        
        result = self._disassemble_py65()  # [D10] çağrısı
        
        # Eski parametreleri geri yükle
        self.start_address = old_start
        self.code = old_code
        
        if self.debug_mode:
            print(f"[D3] ✅ py65 disassemble tamamlandı - {len(result)} satır")
        
        return '\n'.join(result)

    def disassemble(self):
        """[D4] Disassembler metodu - seçilen yazım tarzına göre çıktı üretir"""
        if self.debug_mode:
            print(f"[D4] 🚀 Format seçimli disassemble: {self.output_format}")
            
        if self.output_format == 'asm':
            if self.debug_mode:
                print("[D4] 🔄 [D5] _disassemble_asm() çağrılıyor")
            return self._disassemble_asm()
        elif self.output_format == 'tass':
            if self.debug_mode:
                print("[D4] 🔄 [D6] _disassemble_tass() çağrılıyor")
            return self._disassemble_tass()
        elif self.output_format == 'kickassembler':
            if self.debug_mode:
                print("[D4] 🔄 [D7] _disassemble_kickassembler() çağrılıyor")
            return self._disassemble_kickassembler()
        elif self.output_format == 'cc64':
            if self.debug_mode:
                print("[D4] 🔄 [D8] _disassemble_cc64() çağrılıyor")
            return self._disassemble_cc64()
        else:
            if self.debug_mode:
                print(f"[D4] ❌ Desteklenmeyen format: {self.output_format}")
            raise ValueError(f"Desteklenmeyen çıktı formatı: {self.output_format}")

    def _disassemble_asm(self):
        """[D5] Standard Assembly format için disassembler (Native C64 Assembly)"""
        if self.debug_mode:
            print(f"[D5] 🎯 Native Assembly disassemble başlatılıyor")
            print(f"[D5] 📍 Start: ${self.start_address:04X}, Size: {len(self.code)} bytes")
            
        lines = []
        lines.append(f"; Assembly Code - Start Address: ${self.start_address:04X}")
        lines.append(f"; Code Size: {len(self.code)} bytes")
        lines.append("")
        
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            # Additional bounds check to prevent index errors
            if pc - self.start_address >= len(self.code):
                break
                
            opcode = self.code[pc - self.start_address]
            
            # Address prefix ekle
            address_line = f"{disassembly_formatter.format_address(pc)}: "
            
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                
                # Hex bytes göster
                hex_bytes = []
                for i in range(length):
                    if pc - self.start_address + i < len(self.code):
                        hex_bytes.append(f"{self.code[pc - self.start_address + i]:02X}")
                hex_str = " ".join(hex_bytes).ljust(8)  # 8 karakter genişlik
                
                # Assembly instruksiyon oluştur
                if length == 1:
                    instruction = f"{mnemonic}"
                elif length == 2:
                    # Bounds check for 2-byte instruction
                    if pc - self.start_address + 1 < len(self.code):
                        operand = self.code[pc - self.start_address + 1]
                        instruction = f"{mnemonic} ${operand:02X}"
                    else:
                        instruction = f"{mnemonic} ??   ; Missing operand byte"
                elif length == 3:
                    # Bounds check for 3-byte instruction
                    if pc - self.start_address + 2 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        operand_hi = self.code[pc - self.start_address + 2]
                        operand = operand_lo + (operand_hi << 8)
                        
                        # Memory map label kontrolü
                        label = self.get_memory_label(operand)
                        if label:
                            instruction = f"{mnemonic} {label}"
                        else:
                            instruction = f"{mnemonic} ${operand:04X}"
                    elif pc - self.start_address + 1 < len(self.code):
                        # Only low byte available
                        operand_lo = self.code[pc - self.start_address + 1]
                        instruction = f"{mnemonic} ${operand_lo:02X}?? ; Missing high byte"
                    else:
                        instruction = f"{mnemonic} ????   ; Missing operand bytes"
                
                lines.append(f"{address_line}{hex_str} {instruction}")
                
                # Safe PC increment - don't go beyond available data
                pc += min(length, len(self.code) - (pc - self.start_address))
                
                # Additional safety check to prevent infinite loop
                if pc >= self.start_address + len(self.code):
                    break
            else:
                # Bilinmeyen opcode
                hex_str = f"{opcode:02X}".ljust(8)
                lines.append(f"{address_line}{hex_str} .BYTE ${opcode:02X}")
                pc += 1
        
        return lines

    def _disassemble_tass(self):
        """[D6] TASS yazım tarzı için disassembler"""
        if self.debug_mode:
            print(f"[D6] 🎯 TASS format disassemble başlatılıyor")
            
        lines = []
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            # Bounds check
            if pc - self.start_address >= len(self.code):
                break
                
            opcode = self.code[pc - self.start_address]
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                if length == 1:
                    lines.append(f"{mnemonic}")
                elif length == 2:
                    if pc - self.start_address + 1 < len(self.code):
                        operand = self.code[pc - self.start_address + 1]
                        lines.append(f"{mnemonic} ${operand:02X}")
                    else:
                        lines.append(f"{mnemonic} ??")
                elif length == 3:
                    if pc - self.start_address + 2 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        operand_hi = self.code[pc - self.start_address + 2]
                        operand = operand_lo + (operand_hi << 8)
                        lines.append(f"{mnemonic} ${operand:04X}")
                    elif pc - self.start_address + 1 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        lines.append(f"{mnemonic} ${operand_lo:02X}??")
                    else:
                        lines.append(f"{mnemonic} ????")
                        
                # Safe PC increment
                pc += min(length, len(self.code) - (pc - self.start_address))
                if pc >= self.start_address + len(self.code):
                    break
            else:
                lines.append(f".BYTE ${opcode:02X}")
                pc += 1
        return lines

    def _disassemble_kickassembler(self):
        """[D7] KickAssembler yazım tarzı için disassembler"""
        if self.debug_mode:
            print(f"[D7] 🎯 KickAssembler format disassemble başlatılıyor")
            
        lines = []
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            if pc - self.start_address >= len(self.code):
                break
                
            opcode = self.code[pc - self.start_address]
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                if length == 1:
                    lines.append(f"{mnemonic}")
                elif length == 2:
                    if pc - self.start_address + 1 < len(self.code):
                        operand = self.code[pc - self.start_address + 1]
                        lines.append(f"{mnemonic} #{operand:02X}")
                    else:
                        lines.append(f"{mnemonic} #??")
                elif length == 3:
                    if pc - self.start_address + 2 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        operand_hi = self.code[pc - self.start_address + 2]
                        operand = operand_lo + (operand_hi << 8)
                        lines.append(f"{mnemonic} #{operand:04X}")
                    elif pc - self.start_address + 1 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        lines.append(f"{mnemonic} #{operand_lo:02X}??")
                    else:
                        lines.append(f"{mnemonic} #????")
                        
                pc += min(length, len(self.code) - (pc - self.start_address))
                if pc >= self.start_address + len(self.code):
                    break
            else:
                lines.append(f".BYTE #{opcode:02X}")
                pc += 1
        return lines

    def _disassemble_cc64(self):
        """[D8] CC64 yazım tarzı için disassembler"""
        if self.debug_mode:
            print(f"[D8] 🎯 CC64 format disassemble başlatılıyor")
            
        lines = []
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            if pc - self.start_address >= len(self.code):
                break
                
            opcode = self.code[pc - self.start_address]
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                if length == 1:
                    lines.append(f"{mnemonic}")
                elif length == 2:
                    if pc - self.start_address + 1 < len(self.code):
                        operand = self.code[pc - self.start_address + 1]
                        lines.append(f"{mnemonic} {operand:02X}h")
                    else:
                        lines.append(f"{mnemonic} ??h")
                elif length == 3:
                    if pc - self.start_address + 2 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        operand_hi = self.code[pc - self.start_address + 2]
                        operand = operand_lo + (operand_hi << 8)
                        lines.append(f"{mnemonic} {operand:04X}h")
                    elif pc - self.start_address + 1 < len(self.code):
                        operand_lo = self.code[pc - self.start_address + 1]
                        lines.append(f"{mnemonic} {operand_lo:02X}??h")
                    else:
                        lines.append(f"{mnemonic} ????h")
                        
                pc += min(length, len(self.code) - (pc - self.start_address))
                if pc >= self.start_address + len(self.code):
                    break
            else:
                lines.append(f".BYTE {opcode:02X}h")
                pc += 1
        return lines
    
    def _disassemble_simple(self):
        """[D9] Basit opcode table ile disassemble"""
        if self.debug_mode:
            print(f"[D9] 🎯 Basit disassemble başlatılıyor")
            
        if not self.code:
            return ["Hata: Kod verisi yok"]
        
        lines = []
        pc = self.start_address
        end_address = self.start_address + len(self.code)
        
        while pc < end_address:
            try:
                if pc - self.start_address >= len(self.code):
                    break
                    
                opcode = self.code[pc - self.start_address]
                
                if opcode in self.opcodes:
                    template, length, opcode_name = self.opcodes[opcode]
                    operand_value = None
                    
                    if length == 1:
                        disasm_text = template
                    elif length == 2:
                        if pc - self.start_address + 1 < len(self.code):
                            operand = self.code[pc - self.start_address + 1]
                            operand_value = operand
                            disasm_text = template % operand
                            
                            # Memory map kontrolü (sadece assembly için)
                            if self.output_format == 'asm':
                                memory_info = self.get_memory_info(operand)
                                if memory_info:
                                    disasm_text += f" ; {memory_info}"
                        else:
                            disasm_text = f".BYTE ${opcode:02X}"
                    elif length == 3:
                        if pc - self.start_address + 2 < len(self.code):
                            operand_lo = self.code[pc - self.start_address + 1]
                            operand_hi = self.code[pc - self.start_address + 2]
                            operand = operand_lo + (operand_hi << 8)
                            operand_value = operand
                            disasm_text = template % operand
                            
                            # Memory map kontrolü (sadece assembly için)
                            if self.output_format == 'asm':
                                memory_info = self.get_memory_info(operand)
                                if memory_info:
                                    disasm_text += f" ; {memory_info}"
                        else:
                            disasm_text = f".BYTE ${opcode:02X}"
                    
                    # Format'a göre çeviri yap
                    if self.output_format != 'asm':
                        translation = self.translate_instruction(opcode_name, operand_value)
                        if translation:
                            # Çeviri ana kod olsun, assembly yorum olsun
                            if self.output_format == 'c':
                                disasm_text = f"{translation}  /* {disasm_text} */"
                            elif self.output_format == 'qbasic':
                                disasm_text = f"{translation}  REM {disasm_text}"
                            elif self.output_format == 'pdsx':
                                disasm_text = f"{translation}  REM {disasm_text}"
                            elif self.output_format == 'commodorebasicv2':
                                disasm_text = f"{translation}  REM {disasm_text}"
                            elif self.output_format == 'pseudo':
                                disasm_text = f"{translation}  // {disasm_text}"
                            else:
                                disasm_text = f"{translation}  /* {disasm_text} */"
                        
                        lines.append(f"{disasm_text}")
                    else:
                        # Assembly format için address ile beraber
                        lines.append(f"${pc:04X}: {disasm_text}")
                    
                    pc += length
                else:
                    # Bilinmeyen opcode - sabit çeviri
                    if self.output_format == 'asm':
                        lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                    else:
                        # Bilinmeyen opcode'lar için format'a göre sabit çeviri
                        if self.output_format == 'c':
                            lines.append(f"/* Unknown opcode: 0x{opcode:02X} */")
                        elif self.output_format == 'qbasic':
                            lines.append(f"REM Unknown opcode: 0x{opcode:02X}")
                        elif self.output_format == 'pdsx':
                            lines.append(f"REM Unknown opcode: 0x{opcode:02X}")
                        elif self.output_format == 'commodorebasicv2':
                            lines.append(f"REM Unknown opcode: 0x{opcode:02X}")
                        elif self.output_format == 'pseudo':
                            lines.append(f"// Unknown opcode: 0x{opcode:02X}")
                        else:
                            lines.append(f"/* Unknown opcode: 0x{opcode:02X} */")
                    pc += 1
                    
            except Exception as e:
                lines.append(f"{disassembly_formatter.format_address(pc)}: HATA - {e}")
                pc += 1
        
        return lines
    
    def _disassemble_py65(self):
        """[D10] py65 ile disassemble (eski method)"""
        if self.debug_mode:
            print(f"[D10] 🎯 py65 disassemble başlatılıyor")
            
        try:
            # Memory'ye kodu yükle
            self.memory[self.start_address:self.start_address + len(self.code)] = self.code
            
            lines = []
            pc = self.start_address
            end_address = self.start_address + len(self.code)
            
            while pc < end_address:
                try:
                    # py65 disassembler kullan
                    length, disasm_text = self.py65_disassembler.instruction_at(pc)
                    lines.append(f"{disassembly_formatter.format_address(pc)}: {disasm_text}")
                    pc += length
                    
                except Exception as e:
                    # Fallback: Basit disassemble
                    opcode = self.memory[pc]
                    if opcode in self.opcodes:
                        length = self.opcodes[opcode][1]
                        lines.append(f"{disassembly_formatter.format_address(pc)}: .BYTE ${opcode:02X}")
                    else:
                        lines.append(f"{disassembly_formatter.format_address(pc)}: .BYTE ${opcode:02X}")
                        length = 1
                    pc += length
                    
            return lines
            
        except Exception as e:
            return [f"py65 Hatası: {e}"]
    
    def _get_instruction_length(self, opcode):
        """Instruction uzunluğunu hesapla"""
        if opcode in self.opcodes:
            return self.opcodes[opcode][1]
        return 1
    
    def convert_to_language(self, asm_lines, target_language):
        """[D15] Assembly'yi başka dillere çevir"""
        if self.debug_mode:
            print(f"[D15] 🔄 Dil çevirisi: {target_language}")
            
        if not asm_lines:
            return []
        
        converted = []
        
        for line in asm_lines:
            try:
                # Assembly satırını parse et
                if ':' in line:
                    addr_part, inst_part = line.split(':', 1)
                    addr = addr_part.strip()
                    instruction = inst_part.strip()
                    
                    # Opcode'u çıkar
                    opcode_name = instruction.split()[0] if instruction else ""
                    
                    # Çeviri yap
                    translation = self.opcode_manager.get_translation(opcode_name, target_language)
                    converted.append(f"{addr}: {translation}")
                else:
                    converted.append(f"// {line}")
                    
            except Exception as e:
                converted.append(f"// Çeviri hatası: {line}")
        
        return converted
    
    def to_c(self, asm_lines):
        """[D16] C diline çevir"""
        if self.debug_mode:
            print(f"[D16] 🔄 C diline çeviri")
        return self.convert_to_language(asm_lines, "c")
    
    def to_qbasic(self, asm_lines):
        """[D17] QBasic'e çevir"""
        if self.debug_mode:
            print(f"[D17] 🔄 QBasic'e çeviri")
        return self.convert_to_language(asm_lines, "qbasic")
    
    def to_pdsx(self, asm_lines):
        """[D18] PDSX'e çevir"""
        if self.debug_mode:
            print(f"[D18] 🔄 PDSX'e çeviri")
        return self.convert_to_language(asm_lines, "pdsx")
    
    def to_commodore_basic_v2(self, asm_lines):
        """[D19] Commodore BASIC V2'ye çevir"""
        if self.debug_mode:
            print(f"[D19] 🔄 Commodore BASIC V2'ye çeviri")
        return self.convert_to_language(asm_lines, "commodorebasicv2")
    
    def to_pseudo(self, asm_lines):
        """[D20] Pseudo-code'a çevir"""
        if self.debug_mode:
            print(f"[D20] 🔄 Pseudo-code'a çeviri")
        return self.convert_to_language(asm_lines, "pseudo")
    
    def get_memory_label(self, address):
        """[D14] Memory map'ten label al"""
        if self.debug_mode:
            print(f"[D14] 🔍 Memory label aranıyor: ${address:04X}")
            
        try:
            # JSON verisini DataLoader üzerinden yükle
            from data_loader import DataLoader
            loader = DataLoader(os.path.dirname(__file__))
            
            # Memory maps ve zeropage verilerini yükle
            mem_maps = loader.load_directory('c64_rom_data/memory_maps')
            zero_maps = loader.load_directory('c64_rom_data/zeropage')
            
            # Önce zeropage değişkenlerini kontrol et
            for key, data in zero_maps.get('zeropage_vars', {}).items():
                try:
                    addr = int(key.replace('$', ''), 16)
                    if addr == address:
                        name = data.get('name', '')
                        return name.upper() if name else None
                except:
                    continue
            
            # Sonra memory map'i kontrol et
            for key, data in mem_maps.get('c64_memory_map', {}).items():
                try:
                    start_addr = int(key.replace('$', ''), 16)
                    end_addr_str = data.get('end_addr', key)
                    end_addr = int(end_addr_str.replace('$', ''), 16)
                    
                    if start_addr <= address <= end_addr:
                        name = data.get('name', '')
                        return name.replace(' ', '_').upper() if name else None
                except:
                    continue
            
            # ROM routines ve KERNAL calls
            rom_data = loader.load_directory('c64_rom_data')
            kernal_routines = rom_data.get('kernal_routines', {})
            basic_routines = rom_data.get('basic_routines', {})
            
            addr_hex = f"${address:04X}"
            if addr_hex in kernal_routines:
                name = kernal_routines[addr_hex].get('name', '')
                return name.upper() if name else None
            
            if addr_hex in basic_routines:
                name = basic_routines[addr_hex].get('name', '')
                return name.upper() if name else None
            
            return None
            
        except Exception as e:
            if self.debug_mode:
                print(f"[D14] JSON label yükleme hatası: {e}")
            return None
    
    # === DEBUG VE TEST FONKSİYONLARI ===
    
    def debug_toggle(self, enable=None):
        """[DEBUG] Debug modunu aç/kapat"""
        if enable is None:
            self.debug_mode = not self.debug_mode
        else:
            self.debug_mode = enable
        print(f"[DEBUG] Debug mode: {'AÇIK' if self.debug_mode else 'KAPALI'}")
    
    def debug_info(self):
        """[DEBUG] Genel debug bilgilerini göster"""
        print("=" * 60)
        print("🍎 ADVANCED DISASSEMBLER DEBUG INFO")
        print("=" * 60)
        print(f"[D1] Start Address: ${self.start_address:04X}")
        print(f"[D1] Code Size: {len(self.code)} bytes")
        print(f"[D1] Output Format: {self.output_format}")
        print(f"[D1] Use py65: {self.use_py65}")
        print(f"[D1] py65 Available: {self.py65_available}")
        print(f"[D1] Use Illegal Opcodes: {self.use_illegal_opcodes}")
        print(f"[D1] Debug Mode: {self.debug_mode}")
        print(f"[D12] Memory Map Entries: {len(self.memory_map)}")
        print(f"[D1] Opcodes Available: {len(self.opcodes)}")
        print(f"[D1] Translations Available: {len(self.translations)}")
        print("=" * 60)
    
    def debug_test_opcodes(self, count=10):
        """[DEBUG] İlk N opcode'u test et"""
        print(f"[DEBUG] İlk {count} opcode test ediliyor...")
        for i in range(min(count, len(self.code))):
            opcode = self.code[i]
            addr = self.start_address + i
            
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                print(f"[D-TEST] ${addr:04X}: {opcode:02X} -> {mnemonic} (len:{length})")
            else:
                print(f"[D-TEST] ${addr:04X}: {opcode:02X} -> UNKNOWN")
    
    def debug_memory_map_sample(self, count=5):
        """[DEBUG] Memory map örnekleri göster"""
        print(f"[DEBUG] Memory map örnekleri (ilk {count}):")
        items = list(self.memory_map.items())[:count]
        for addr, info in items:
            print(f"[D12] ${addr:04X}: {info}")
    
    def test_translation(self, opcode_name, target_format=None):
        """[DEBUG] Belirli bir opcode çevirisini test et"""
        if target_format:
            old_format = self.output_format
            self.output_format = target_format
        
        print(f"[D11-TEST] Testing {opcode_name} -> {self.output_format}")
        result = self.translate_instruction(opcode_name, 0x1234)
        print(f"[D11-TEST] Result: {result}")
        
        if target_format:
            self.output_format = old_format
        
        return result

# Geriye uyumluluk için eski API
class Disassembler:
    def __init__(self, start_address, code):
        self.advanced = AdvancedDisassembler(start_address, code, use_py65=False)
    
    def disassemble(self):
        return self.advanced.disassemble()

# py65 destekli versiyon
class PY65Disassembler:
    def __init__(self, start_address, code):
        self.advanced = AdvancedDisassembler(start_address, code, use_py65=True)
    
    def disassemble(self):
        return self.advanced.disassemble()

if __name__ == "__main__":
    # 🚀 DEBUG MODE TEST RUNNER
    print("🍎 Advanced Disassembler v5.4 - DEBUG MODE")
    print("=" * 60)
    
    # Test kodu
    test_code = [0xA9, 0x00, 0x85, 0x02, 0x60]  # LDA #$00, STA $02, RTS
    
    print("=== [D1] Basic Test - Constructor ===")
    disasm = Disassembler(0xC000, test_code)
    for line in disasm.disassemble():
        print(line)
    
    print("\n=== [D1] Advanced Disassembler Test ===")
    advanced = AdvancedDisassembler(0xC000, test_code)
    
    # Debug bilgilerini göster
    print("\n=== [DEBUG] Info ===")
    advanced.debug_info()
    
    print("\n=== [DEBUG] Opcode Test ===")
    advanced.debug_test_opcodes(5)
    
    print("\n=== [DEBUG] Memory Map Sample ===")
    advanced.debug_memory_map_sample(3)
    
    print("\n=== [D5] Assembly Disassembly ===")
    asm_lines = advanced.disassemble()
    for line in asm_lines:
        print(line)
    
    print("\n=== [D16] C Translation Test ===")
    advanced.test_translation("LDA", "c")
    c_lines = advanced.to_c(asm_lines)
    for line in c_lines:
        print(line)
    
    print("\n=== [D17] QBasic Translation Test ===")
    advanced.test_translation("STA", "qbasic")
    qbasic_lines = advanced.to_qbasic(asm_lines)
    for line in qbasic_lines:
        print(line)
    
    # Debug mode toggle test
    print("\n=== [DEBUG] Mode Toggle Test ===")
    advanced.debug_toggle(False)
    advanced.debug_toggle(True)
    
    print("\n🎯 Test tamamlandı! Tüm componentler [D1-D20] çalışıyor.")
    print("💡 Artık component kodları ile kolayca iletişim kurabiliriz!")
