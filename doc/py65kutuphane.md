# py65 Kütüphanesi Derinlemesine Analiz

## Genel Bakış

py65, Mike Naberezny tarafından geliştirilmiş profesyonel 6502 mikroişlemci simülatörü ve disassembler kütüphanesidir. Bu kütüphane C64, Apple II, NES gibi retro bilgisayarların temelini oluşturan 6502 ailesi mikroişlemcileri için tam özellikli bir emülatör sunar.

**Konum**: `C:\Users\dell\Documents\projeler\d64_converter\venv_asmto\Lib\site-packages\py65\`
**Versiyon**: 1.2.0
**Geliştirici**: Mike Naberezny
**Lisans**: BSD

## Modül Yapısı

### 1. Ana Modüller (`py65/`)

#### 1.1 `mpu6502.py` - Ana İşlemci Modülü
- **Amaç**: 6502 mikroişlemcinin tam simülasyonu
- **Ana Sınıf**: `MPU`
- **Temel Özellikler**:
  - 65536 byte (64KB) bellek alanı
  - 16-bit adres sistemi
  - 8-bit veri sistemi
  - Tam opcode desteği (256 tüm opcode)
  - Interrupt sistemi (IRQ, NMI, RESET)
  - Processor flags (NEGATIVE, OVERFLOW, BREAK, DECIMAL, INTERRUPT, ZERO, CARRY)

```python
# MPU temel kullanım
from py65.devices.mpu6502 import MPU
from py65.memory import ObservableMemory

# Bellek oluştur
memory = ObservableMemory()
# MPU başlat
mpu = MPU(memory=memory, pc=0x1000)
# Tek adım çalıştır
mpu.step()
```

#### 1.2 `disassembler.py` - Disassembler Modülü
- **Amaç**: Makine kodunu assembly koduna çevirme
- **Ana Sınıf**: `Disassembler`
- **Desteklenen Adreslemeler**:
  - `acc` - Accumulator
  - `abs` - Absolute
  - `abx` - Absolute,X
  - `aby` - Absolute,Y
  - `imm` - Immediate
  - `imp` - Implied
  - `ind` - Indirect
  - `iny` - Indirect,Y
  - `inx` - Indirect,X
  - `iax` - Indirect Absolute,X
  - `rel` - Relative
  - `zpi` - Zero Page Indirect
  - `zpg` - Zero Page
  - `zpx` - Zero Page,X
  - `zpy` - Zero Page,Y

```python
# Disassembler kullanım
from py65.disassembler import Disassembler

disasm = Disassembler(mpu)
length, instruction = disasm.instruction_at(0x1000)
print(f"Length: {length}, Instruction: {instruction}")
```

#### 1.3 `assembler.py` - Assembler Modülü
- **Amaç**: Assembly kodunu makine koduna çevirme
- **Ana Sınıf**: `Assembler`
- **Özellikler**:
  - Tam 6502 assembly syntax desteği
  - Label desteği
  - Macro desteği
  - Hata raporlama

```python
# Assembler kullanım
from py65.assembler import Assembler

assembler = Assembler(mpu)
assembled = assembler.assemble("LDA #$FF")
```

#### 1.4 `memory.py` - Bellek Modülü
- **Amaç**: Gözlemlenebilir bellek sistemi
- **Ana Sınıf**: `ObservableMemory`
- **Özellikler**:
  - Read/Write callback sistemi
  - Memory mapping
  - I/O port simülasyonu

```python
# Memory callback örneği
def read_callback(address, value):
    print(f"Read from ${address:04X}: ${value:02X}")

memory = ObservableMemory()
memory.subscribe_to_read([0x1000, 0x1001], read_callback)
```

#### 1.5 `monitor.py` - Monitör Modülü
- **Amaç**: Interaktif debugging ve monitoring
- **Ana Sınıf**: `Monitor`
- **Komutlar**:
  - `assemble` - Assembly kod yazma
  - `disassemble` - Disassembly görüntüleme
  - `mem` - Bellek görüntüleme/düzenleme
  - `registers` - Register görüntüleme
  - `step` - Tek adım çalıştırma
  - `breakpoint` - Breakpoint yönetimi
  - `load/save` - Dosya işlemleri

### 2. Cihaz Modülleri (`py65/devices/`)

#### 2.1 `mpu6502.py` - Orijinal 6502
- **Özellikler**:
  - 256 opcode desteği
  - Decimal mode
  - Interrupt sistem
  - BCD aritmetik

#### 2.2 `mpu65c02.py` - CMOS 65C02
- **Ek Özellikler**:
  - Yeni opcodes (BRA, PHX, PLX, PHY, PLY)
  - Gelişmiş addressing modes
  - Düşük güç tüketimi simülasyonu

#### 2.3 `mpu65org16.py` - 16-bit Genişleme
- **Özellikler**:
  - 16-bit addressing
  - Genişletilmiş register set

### 3. Yardımcı Modüller (`py65/utils/`)

#### 3.1 `addressing.py` - Adres Çözümleme
- Label yönetimi
- Adres formatları
- Symbol table

#### 3.2 `conversions.py` - Veri Dönüşümleri
- Binary/Hex/Decimal dönüşümler
- String formatları

#### 3.3 `devices.py` - Cihaz Yardımcıları
- Instruction decorator
- Device utilities

## Profesyonel Disassembler İçin Kritik Sınıflar

### 1. MPU Sınıfı Detayları

```python
class MPU:
    # Temel özellikler
    BYTE_WIDTH = 8      # 8-bit veri
    ADDR_WIDTH = 16     # 16-bit adres
    BYTE_FORMAT = "%02x" # Hex format
    ADDR_FORMAT = "%04x" # Hex format
    
    # Processor flags
    NEGATIVE = 128      # N flag
    OVERFLOW = 64       # V flag
    UNUSED = 32         # Unused flag
    BREAK = 16          # B flag
    DECIMAL = 8         # D flag
    INTERRUPT = 4       # I flag
    ZERO = 2            # Z flag
    CARRY = 1           # C flag
    
    # Vektörler
    RESET = 0xfffc      # Reset vector
    NMI = 0xfffa        # NMI vector
    IRQ = 0xfffe        # IRQ vector
```

### 2. Disassembler Sınıfı Detayları

```python
class Disassembler:
    def __init__(self, mpu, address_parser=None):
        self._mpu = mpu
        self._address_parser = address_parser or AddressParser()
        
    def instruction_at(self, pc):
        """PC adresindeki instruction'ı çözümle"""
        instruction = self._mpu.ByteAt(pc)
        disasm, addressing = self._mpu.disassemble[instruction]
        
        # Addressing mode'a göre format
        if addressing == 'abs':
            address = self._mpu.WordAt(pc + 1)
            disasm += ' $' + self.addrFmt % address
            length = 3
        elif addressing == 'imm':
            byte = self._mpu.ByteAt(pc + 1)
            disasm += ' #$' + self.byteFmt % byte
            length = 2
        # ... diğer addressing modes
        
        return (length, disasm)
```

### 3. ObservableMemory Sınıfı Detayları

```python
class ObservableMemory:
    def subscribe_to_read(self, addresses, callback):
        """Bellek okuma callback'i ekle"""
        pass
        
    def subscribe_to_write(self, addresses, callback):
        """Bellek yazma callback'i ekle"""
        pass
        
    def write(self, address, value):
        """Bellek yazma işlemi"""
        pass
```

## Profesyonel Disassembler Tasarımı

### 1. Gelişmiş Özellikler

```python
class Py65ProfessionalDisassembler:
    def __init__(self):
        self.memory = ObservableMemory()
        self.mpu = MPU(memory=self.memory)
        self.disassembler = Disassembler(self.mpu)
        self.symbol_table = {}
        self.code_blocks = []
        self.data_blocks = []
        
    def advanced_disassemble(self, start_addr, end_addr):
        """Gelişmiş disassembly fonksiyonu"""
        results = []
        pc = start_addr
        
        while pc <= end_addr:
            # Instruction analizi
            length, instruction = self.disassembler.instruction_at(pc)
            
            # Code flow analizi
            flow_info = self.analyze_code_flow(pc, instruction)
            
            # Symbol çözümlemesi
            symbol = self.resolve_symbol(pc)
            
            # Yorum oluşturma
            comment = self.generate_comment(pc, instruction)
            
            result = {
                'address': pc,
                'bytes': [self.mpu.ByteAt(pc + i) for i in range(length)],
                'instruction': instruction,
                'symbol': symbol,
                'comment': comment,
                'flow_info': flow_info
            }
            
            results.append(result)
            pc += length
            
        return results
```

### 2. Code Flow Analizi

```python
def analyze_code_flow(self, address, instruction):
    """Kod akış analizi"""
    flow_info = {
        'type': 'sequential',
        'targets': [],
        'is_branch': False,
        'is_jump': False,
        'is_call': False,
        'is_return': False
    }
    
    # Branch instructions
    if instruction.startswith(('BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BVC', 'BVS')):
        flow_info['type'] = 'branch'
        flow_info['is_branch'] = True
        # Branch target hesapla
        
    # Jump instructions
    elif instruction.startswith('JMP'):
        flow_info['type'] = 'jump'
        flow_info['is_jump'] = True
        
    # Subroutine calls
    elif instruction.startswith('JSR'):
        flow_info['type'] = 'call'
        flow_info['is_call'] = True
        
    # Returns
    elif instruction.startswith('RTS'):
        flow_info['type'] = 'return'
        flow_info['is_return'] = True
        
    return flow_info
```

### 3. Symbol Management

```python
def add_symbol(self, address, name, symbol_type='label'):
    """Symbol tablosuna symbol ekle"""
    self.symbol_table[address] = {
        'name': name,
        'type': symbol_type,
        'references': []
    }
    
def resolve_symbol(self, address):
    """Adres için symbol çözümle"""
    if address in self.symbol_table:
        return self.symbol_table[address]['name']
    return None
    
def auto_generate_labels(self, start_addr, end_addr):
    """Otomatik label oluştur"""
    pc = start_addr
    while pc <= end_addr:
        length, instruction = self.disassembler.instruction_at(pc)
        
        # Jump/Branch hedeflerini bul
        if 'JMP' in instruction or 'JSR' in instruction:
            target = self.extract_target_address(instruction)
            if target and target not in self.symbol_table:
                if 'JSR' in instruction:
                    self.add_symbol(target, f"sub_{target:04X}", 'subroutine')
                else:
                    self.add_symbol(target, f"label_{target:04X}", 'label')
        
        pc += length
```

## Performans Optimizasyonları

### 1. Bellek Yönetimi

```python
class OptimizedMemory(ObservableMemory):
    def __init__(self, size=0x10000):
        super().__init__()
        self._memory = bytearray(size)
        self._read_callbacks = {}
        self._write_callbacks = {}
        
    def fast_read(self, address):
        """Hızlı bellek okuma"""
        return self._memory[address & 0xFFFF]
        
    def fast_write(self, address, value):
        """Hızlı bellek yazma"""
        self._memory[address & 0xFFFF] = value & 0xFF
```

### 2. Batch Disassembly

```python
def batch_disassemble(self, addresses):
    """Toplu disassembly işlemi"""
    results = {}
    
    # Bellekteki tüm veriyi bir kez oku
    memory_data = {}
    for addr in addresses:
        memory_data[addr] = self.mpu.ByteAt(addr)
    
    # Batch işlemi
    for addr in addresses:
        length, instruction = self.disassembler.instruction_at(addr)
        results[addr] = {
            'length': length,
            'instruction': instruction,
            'bytes': [memory_data.get(addr + i, 0) for i in range(length)]
        }
    
    return results
```

## Hata Yönetimi

```python
class DisassemblyError(Exception):
    """Disassembly hata sınıfı"""
    pass

class Py65ErrorHandler:
    def __init__(self):
        self.errors = []
        
    def handle_illegal_opcode(self, address, opcode):
        """Illegal opcode hatası"""
        error = {
            'type': 'illegal_opcode',
            'address': address,
            'opcode': opcode,
            'message': f"Illegal opcode ${opcode:02X} at ${address:04X}"
        }
        self.errors.append(error)
        
    def handle_memory_error(self, address):
        """Bellek hatası"""
        error = {
            'type': 'memory_error',
            'address': address,
            'message': f"Memory access error at ${address:04X}"
        }
        self.errors.append(error)
```

## Kullanım Senaryoları

### 1. C64 PRG Dosyası Disassembly

```python
def disassemble_c64_prg(self, prg_data):
    """C64 PRG dosyasını disassemble et"""
    # PRG header (2 byte load address)
    load_addr = prg_data[0] | (prg_data[1] << 8)
    
    # Belleği yükle
    for i, byte in enumerate(prg_data[2:]):
        self.memory.write(load_addr + i, byte)
    
    # Disassemble
    end_addr = load_addr + len(prg_data) - 3
    return self.advanced_disassemble(load_addr, end_addr)
```

### 2. Kernal ROM Analizi

```python
def analyze_kernal_rom(self, rom_data):
    """C64 Kernal ROM analizi"""
    # ROM'u $E000'e yükle
    for i, byte in enumerate(rom_data):
        self.memory.write(0xE000 + i, byte)
    
    # Bilinen entry point'leri ekle
    self.add_symbol(0xE000, "KERNAL_START", "entry_point")
    self.add_symbol(0xFFD2, "CHROUT", "kernal_call")
    self.add_symbol(0xFFE4, "GETIN", "kernal_call")
    
    # Disassemble
    return self.advanced_disassemble(0xE000, 0xFFFF)
```

## Sonuç

py65 kütüphanesi, 6502 tabanlı sistemler için profesyonel seviyede disassembly ve emülasyon yetenekleri sunar. Modüler yapısı, genişletilebilirliği ve kapsamlı API'si sayesinde gelişmiş disassembler uygulamaları geliştirmek için ideal bir temel sağlar.

**Avantajlar**:
- Tam 6502 opcode desteği
- Esnek bellek sistemi
- Gelişmiş addressing mode desteği
- Interrupt simülasyonu
- Extensible architecture

**Sınırlamalar**:
- Sadece 6502 ailesi işlemciler
- Gerçek zamanlı performans sınırlamaları
- Grafik/ses I/O desteği yok

Bu analiz, py65 kütüphanesini kullanarak profesyonel bir disassembler modülü geliştirmek için gereken tüm bilgileri içermektedir.
