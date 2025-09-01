"""
Gelişmiş D64/D71/D81/G64/T64/TAP/PRG okuyucusu
GitHub cbmcodecs kaynaklarından ilham alınarak geliştirilmiştir





"""

import struct
import os
from pathlib import Path

class EnhancedD64Reader:
    def __init__(self):
        # D64 format specifications
        self.D64_TRACKS = 35
        self.D64_SECTORS = {
            # Track 1-17: 21 sectors
            # Track 18-24: 19 sectors  
            # Track 25-30: 18 sectors
            # Track 31-35: 17 sectors
        }
        
        # File types
        self.FILE_TYPES = {
            0x80: "DEL",  # Deleted
            0x81: "SEQ",  # Sequential
            0x82: "PRG",  # Program
            0x83: "USR",  # User
            0x84: "REL",  # Relative
            0x85: "CBM",  # CBM
            0x86: "DIR",  # Directory
        }
        
        # Doğru PETSCII to ASCII conversion
        self.PETSCII_TO_ASCII = {}
        
        # PETSCII karakter tablosu (C64 standardı)
        for i in range(256):
            if i == 0:
                self.PETSCII_TO_ASCII[i] = ''  # NULL
            elif 1 <= i <= 31:
                self.PETSCII_TO_ASCII[i] = '?'  # Control characters
            elif 32 <= i <= 95:
                self.PETSCII_TO_ASCII[i] = chr(i)  # Normal ASCII
            elif 96 <= i <= 127:
                self.PETSCII_TO_ASCII[i] = chr(i - 32)  # Uppercase letters (C64 style)
            elif 128 <= i <= 159:
                self.PETSCII_TO_ASCII[i] = '?'  # Reverse video control
            elif 160 <= i <= 192:
                self.PETSCII_TO_ASCII[i] = chr(i - 128)  # Shifted characters
            elif 193 <= i <= 218:
                self.PETSCII_TO_ASCII[i] = chr(i - 128)  # Lowercase letters
            else:
                self.PETSCII_TO_ASCII[i] = '?'  # Other characters
    
    def petscii_to_ascii(self, petscii_bytes):
        """PETSCII'yi ASCII'ye çevir"""
        result = ""
        for byte in petscii_bytes:
            if byte == 0:
                break
            result += self.PETSCII_TO_ASCII.get(byte, '?')
        return result.strip()
    
    def get_track_sectors(self, track):
        """Track'e göre sector sayısını döndür"""
        if track <= 17:
            return 21
        elif track <= 24:
            return 19
        elif track <= 30:
            return 18
        else:
            return 17
    
    def track_sector_to_offset(self, track, sector, disk_type="d64"):
        """Track/Sector'u byte offset'e çevir"""
        if disk_type == "d64":
            offset = 0
            for t in range(1, track):
                offset += self.get_track_sectors(t) * 256
            offset += sector * 256
            return offset
        elif disk_type == "d71":
            # D71 = 2 x D64
            if track <= 35:
                return self.track_sector_to_offset(track, sector, "d64")
            else:
                # İkinci taraf
                base_offset = 35 * 21 * 256  # İlk 35 track
                offset = base_offset
                for t in range(36, track):
                    offset += self.get_track_sectors(t - 35) * 256
                offset += sector * 256
                return offset
        elif disk_type == "d81":
            # D81 = 80 tracks, 40 sectors each
            return (track - 1) * 40 * 256 + sector * 256
        
        return 0
    
    def read_directory_d64(self, disk_data, disk_type="d64"):
        """D64 directory'sini oku"""
        entries = []
        
        # Directory track/sector (18,1)
        dir_track = 18
        dir_sector = 1
        
        while dir_track != 0:
            # Directory sector'unu oku
            offset = self.track_sector_to_offset(dir_track, dir_sector, disk_type)
            
            if offset + 256 > len(disk_data):
                break
                
            sector_data = disk_data[offset:offset + 256]
            
            # Sonraki directory sector
            dir_track = sector_data[0]
            dir_sector = sector_data[1]
            
            # Bu sector'daki dosya girişleri (8 adet, 32 byte her biri)
            for i in range(8):
                entry_offset = 2 + i * 32
                if entry_offset + 32 > len(sector_data):
                    break
                    
                entry_data = sector_data[entry_offset:entry_offset + 32]
                
                # Dosya tipi
                file_type = entry_data[0]
                if file_type == 0:  # Boş giriş
                    continue
                
                # Track/Sector
                track = entry_data[1]
                sector = entry_data[2]
                
                # Dosya adı (16 byte)
                filename_bytes = entry_data[3:19]
                filename = self.petscii_to_ascii(filename_bytes)
                
                # Dosya boyutu (blok sayısı)
                size_blocks = entry_data[28] + (entry_data[29] << 8)
                
                # Dosya tipini decode et
                file_type_str = self.FILE_TYPES.get(file_type & 0x87, "UNK")
                
                entries.append({
                    "filename": filename,
                    "type": file_type_str,
                    "track": track,
                    "sector": sector,
                    "size": size_blocks,
                    "file_type": file_type
                })
        
        return entries
    
    def read_prg_file_d64(self, disk_data, track, sector, disk_type="d64"):
        """D64'ten PRG dosyasını oku"""
        prg_data = bytearray()
        
        while track != 0:
            offset = self.track_sector_to_offset(track, sector, disk_type)
            
            if offset + 256 > len(disk_data):
                break
                
            sector_data = disk_data[offset:offset + 256]
            
            # Sonraki track/sector
            next_track = sector_data[0]
            next_sector = sector_data[1]
            
            # Data (2. byte'dan itibaren)
            if next_track == 0:
                # Son sector - sadece kullanılan byte'lar
                used_bytes = next_sector
                if used_bytes > 0:
                    prg_data.extend(sector_data[2:2 + used_bytes])
            else:
                # Tam sector
                prg_data.extend(sector_data[2:])
            
            track = next_track
            sector = next_sector
        
        return bytes(prg_data)
    
    def read_t64_directory(self, t64_data):
        """T64 archive directory'sini oku"""
        entries = []
        
        if len(t64_data) < 64:
            return entries
        
        # T64 header
        header = t64_data[:64]
        
        # Magic check
        if header[:15] != b"C64 tape image":
            return entries
        
        # Directory entries sayısı
        max_entries = struct.unpack('<H', header[24:26])[0]
        used_entries = struct.unpack('<H', header[26:28])[0]
        
        # Directory entries
        for i in range(min(max_entries, used_entries)):
            entry_offset = 64 + i * 32
            if entry_offset + 32 > len(t64_data):
                break
                
            entry_data = t64_data[entry_offset:entry_offset + 32]
            
            # Dosya tipi
            file_type = entry_data[0]
            if file_type == 0:  # Boş giriş
                continue
            
            # Start/End address
            start_addr = struct.unpack('<H', entry_data[2:4])[0]
            end_addr = struct.unpack('<H', entry_data[4:6])[0]
            
            # Offset
            offset = struct.unpack('<L', entry_data[8:12])[0]
            
            # Filename
            filename_bytes = entry_data[16:32]
            filename = self.petscii_to_ascii(filename_bytes)
            
            # Size
            size = end_addr - start_addr if end_addr > start_addr else 0
            
            entries.append({
                "filename": filename,
                "type": "PRG",
                "start_addr": start_addr,
                "end_addr": end_addr,
                "offset": offset,
                "size": size
            })
        
        return entries
    
    def read_prg_file_t64(self, t64_data, offset, size):
        """T64'ten PRG dosyasını oku"""
        if offset + size > len(t64_data):
            return b""
        
        return t64_data[offset:offset + size]
    
    def read_tap_directory(self, tap_data):
        """TAP dosyasını analiz et"""
        entries = []
        
        if len(tap_data) < 20:
            return entries
        
        # TAP header
        if tap_data[:12] != b"C64-TAPE-RAW":
            return entries
        
        # Version ve data offset
        version = tap_data[12]
        data_offset = 20
        
        # TAP data'sını parse et
        pos = data_offset
        file_count = 0
        
        while pos < len(tap_data):
            # Pulse length
            if pos + 4 > len(tap_data):
                break
                
            pulse_len = struct.unpack('<L', tap_data[pos:pos + 4])[0]
            pos += 4
            
            if pulse_len == 0:
                # Overflow marker
                if pos + 3 > len(tap_data):
                    break
                pulse_len = struct.unpack('<L', tap_data[pos:pos + 3] + b'\x00')[0]
                pos += 3
            
            # Basit dosya sayma
            if pulse_len > 1000:  # Uzun pulse = dosya başlangıcı olabilir
                file_count += 1
                
                entries.append({
                    "filename": f"TAP_FILE_{file_count}",
                    "type": "TAP",
                    "offset": pos - 4,
                    "size": pulse_len
                })
            
            if file_count > 50:  # Limit
                break
        
        return entries
    
    def read_prg_file_tap(self, tap_data, offset, size):
        """TAP'ten data oku"""
        if offset + size > len(tap_data):
            return b""
        
        return tap_data[offset:offset + size]
    
    def read_g64_directory(self, g64_data):
        """G64 dosyasını analiz et"""
        entries = []
        
        if len(g64_data) < 12:
            return entries
        
        # G64 header
        if g64_data[:8] != b"GCR-1541":
            return entries
        
        # Track count
        track_count = g64_data[9]
        
        # Track table offset
        track_table_offset = 12
        
        for track in range(1, track_count + 1):
            table_pos = track_table_offset + (track - 1) * 4
            if table_pos + 4 > len(g64_data):
                break
                
            track_offset = struct.unpack('<L', g64_data[table_pos:table_pos + 4])[0]
            
            if track_offset > 0:
                entries.append({
                    "filename": f"G64_TRACK_{track}",
                    "type": "G64",
                    "track": track,
                    "offset": track_offset,
                    "size": 6250  # Standard G64 track size
                })
        
        return entries
    
    def read_prg_file_g64(self, g64_data, offset, size):
        """G64'ten data oku"""
        if offset + size > len(g64_data):
            return b""
        
        return g64_data[offset:offset + size]

class EnhancedD64ReaderWrapper:
    """Enhanced D64 Reader için GUI uyumlu wrapper sınıf"""
    
    def __init__(self, file_path):
        """Enhanced D64 Reader wrapper constructor"""
        self.file_path = file_path
        self.data = None
        self.ext = None
        self.reader = EnhancedD64Reader()
        
        # Dosyayı oku
        self._load_file()
    
    def _load_file(self):
        """Dosyayı yükle"""
        try:
            self.data, self.ext = enhanced_read_image(self.file_path)
        except Exception as e:
            raise Exception(f"Enhanced D64 Reader dosya yükleme hatası: {e}")
    
    def list_files(self):
        """GUI uyumlu dosya listesi döndür"""
        try:
            if not self.data:
                return []
            
            # Enhanced directory okuma
            entries = enhanced_read_directory(self.data, self.ext)
            
            # GUI uyumlu format'a çevir
            gui_entries = []
            for entry in entries:
                gui_entry = {
                    'filename': entry.get('name', entry.get('filename', 'Unknown')),
                    'filetype': entry.get('type', entry.get('filetype', 'PRG')),
                    'size': entry.get('size', entry.get('blocks', 0)),
                    'track': entry.get('track', 1),
                    'sector': entry.get('sector', 1),
                    'start_address': entry.get('start_addr', entry.get('start_address', 0x0801)),
                    'end_address': entry.get('end_addr', entry.get('end_address', 0)),
                    'offset': entry.get('offset', 0),
                    'source_file': self.file_path  # Kaynak dosya bilgisi ekle
                }
                gui_entries.append(gui_entry)
            
            return gui_entries
            
        except Exception as e:
            raise Exception(f"Enhanced D64 Reader list_files hatası: {e}")
    
    def extract_file(self, entry):
        """Dosyayı çıkar"""
        try:
            return enhanced_extract_prg(self.data, entry, self.ext)
        except Exception as e:
            raise Exception(f"Enhanced D64 Reader extract_file hatası: {e}")

def enhanced_read_image(file_path):
    """Gelişmiş disk image okuyucu"""
    file_path = Path(file_path)
    ext = file_path.suffix.lower()
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    return data, ext

def enhanced_read_directory(data, ext):
    """Gelişmiş directory okuyucu"""
    reader = EnhancedD64Reader()
    
    if ext in ['.d64', '.d71', '.d81']:
        disk_type = ext[1:]  # Remove dot
        return reader.read_directory_d64(data, disk_type)
    elif ext == '.t64':
        return reader.read_t64_directory(data)
    elif ext == '.tap':
        return reader.read_tap_directory(data)
    elif ext == '.g64':
        return reader.read_g64_directory(data)
    else:
        return []

def enhanced_extract_prg(data, entry, ext):
    """Gelişmiş PRG çıkarıcı"""
    reader = EnhancedD64Reader()
    
    if ext in ['.d64', '.d71', '.d81']:
        disk_type = ext[1:]  # Remove dot
        return reader.read_prg_file_d64(data, entry["track"], entry["sector"], disk_type)
    elif ext == '.t64':
        return reader.read_prg_file_t64(data, entry["offset"], entry["size"])
    elif ext == '.tap':
        return reader.read_prg_file_tap(data, entry["offset"], entry["size"])
    elif ext == '.g64':
        return reader.read_prg_file_g64(data, entry["offset"], entry["size"])
    else:
        return b""

if __name__ == "__main__":
    # Test
    import os
    
    test_files = [
        "test_dosyalari/ALPA.D64",
        "test_dosyalari/Hard_Rock.t64",
        "test_dosyalari/best-of-apc-side-a.tap"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n=== {test_file} ===")
            try:
                data, ext = enhanced_read_image(test_file)
                entries = enhanced_read_directory(data, ext)
                
                print(f"Dosya sayısı: {len(entries)}")
                for entry in entries[:5]:  # İlk 5 dosya
                    print(f"  {entry['filename']} - {entry['type']} - {entry.get('size', 'N/A')}")
                    
            except Exception as e:
                print(f"Hata: {e}")
