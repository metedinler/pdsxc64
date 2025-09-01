"""
C1541 emülatörü kodlarından Python'a dönüştürülen D64 okuyucu
C++ kaynak kodlarından analiz edilerek geliştirilmiştir
"""

import struct
import os
from pathlib import Path

class C1541PythonEmulator:
    def __init__(self):
        # C1541 sabitler
        self.TRACK_AREAS = 4
        self.FIRST_TRACK = 1
        self.END_TRACK = 36
        
        # Track alanları
        self.TRACK_AREA_FirstTrack = [1, 18, 25, 31, self.END_TRACK]
        self.TRACK_AREA_SectorsPerTrack = [21, 19, 18, 17]
        self.TRACK_AREA_Tracks = [17, 7, 6, 5]
        self.TRACK_AREA_Blocks = [357, 133, 108, 85]
        self.TRACK_AREA_LogicalStartPosition = [0, 91392, 125440, 153088]
        
        # Disk sabitleri
        self.BLOCKS_OF_A_DISK = 683
        self.BLOCK_SIZE = 0x100
        self.BLOCK_HEADER_SIZE = 2
        self.DISK_SIZE = 174848
        self.LOGICAL_BAM_POSITION = 91392
        self.LOGICAL_DIRECTORY_END_POSITION = 96256
        
        # Dosya tipleri
        self.FILE_TYPE_DEL = 0
        self.FILE_TYPE_SEQ = 1
        self.FILE_TYPE_PRG = 2
        self.FILE_TYPE_USR = 3
        self.FILE_TYPE_REL = 4
        self.FILE_TYPE_ANY = 7
        
        # Dosya bayrakları
        self.FILETYPE_CLOSED_FLAG = 0x80
        self.FILETYPE_WRITEPROTECTED_FLAG = 0x40
        self.FILE_TYPE_BITMASK = 0x07
        
        # Dosya tipi isimleri
        self.FILE_TYPE_NAMES = {
            self.FILE_TYPE_DEL: "DEL",
            self.FILE_TYPE_SEQ: "SEQ",
            self.FILE_TYPE_PRG: "PRG",
            self.FILE_TYPE_USR: "USR",
            self.FILE_TYPE_REL: "REL"
        }
        
        # PETSCII -> ASCII dönüşüm
        self.petscii_to_ascii_table = self._create_petscii_table()
    
    def _create_petscii_table(self):
        """PETSCII to ASCII dönüşüm tablosu"""
        table = {}
        
        # Temel ASCII karakterler
        for i in range(32, 127):
            table[i] = chr(i)
        
        # PETSCII özel karakterler
        for i in range(0, 32):
            table[i] = chr(i + 64) if i + 64 < 127 else '?'
        
        # Büyük harfler (PETSCII 193-218 = A-Z)
        for i in range(193, 219):
            table[i] = chr(i - 128)
        
        # Diğer karakterler
        for i in range(127, 256):
            if i not in table:
                table[i] = '?'
        
        # Boşluk karakteri
        table[0xa0] = ' '  # PETSCII space
        
        return table
    
    def petscii_to_ascii(self, petscii_data):
        """PETSCII'yi ASCII'ye çevir"""
        result = ""
        for byte in petscii_data:
            if byte == 0 or byte == 0xa0:  # NULL veya PETSCII space
                break
            result += self.petscii_to_ascii_table.get(byte, '?')
        return result.strip()
    
    def get_track_area(self, track):
        """Track'in hangi alanda olduğunu bul"""
        for i in range(self.TRACK_AREAS):
            if track >= self.TRACK_AREA_FirstTrack[i] and track < self.TRACK_AREA_FirstTrack[i + 1]:
                return i
        return -1
    
    def get_sectors_per_track(self, track):
        """Track'teki sector sayısını döndür"""
        area = self.get_track_area(track)
        if area >= 0:
            return self.TRACK_AREA_SectorsPerTrack[area]
        return 0
    
    def track_sector_to_logical_position(self, track, sector):
        """Track/Sector'u logical pozisyona çevir"""
        if track < self.FIRST_TRACK or track >= self.END_TRACK:
            return -1
        
        position = 0
        
        # Önceki track'lerin pozisyonunu hesapla
        for t in range(self.FIRST_TRACK, track):
            position += self.get_sectors_per_track(t) * self.BLOCK_SIZE
        
        # Sector pozisyonu ekle
        position += sector * self.BLOCK_SIZE
        
        return position
    
    def logical_position_to_track_sector(self, position):
        """Logical pozisyonu track/sector'a çevir"""
        current_pos = 0
        
        for track in range(self.FIRST_TRACK, self.END_TRACK):
            sectors_per_track = self.get_sectors_per_track(track)
            track_size = sectors_per_track * self.BLOCK_SIZE
            
            if current_pos + track_size > position:
                # Bu track'te
                sector_offset = position - current_pos
                sector = sector_offset // self.BLOCK_SIZE
                return track, sector
            
            current_pos += track_size
        
        return -1, -1
    
    def read_block(self, disk_data, track, sector):
        """Disk'ten blok oku"""
        position = self.track_sector_to_logical_position(track, sector)
        if position < 0 or position + self.BLOCK_SIZE > len(disk_data):
            return None
        
        return disk_data[position:position + self.BLOCK_SIZE]
    
    def read_directory(self, disk_data):
        """Directory'yi oku"""
        entries = []
        
        # Directory track 18, sector 1'den başlar
        track = 18
        sector = 1
        
        while track != 0:
            # Directory sector'unu oku
            block = self.read_block(disk_data, track, sector)
            if not block:
                break
            
            # Sonraki directory sector
            track = block[0]
            sector = block[1]
            
            # Bu sector'daki dosya girişleri (8 adet, 32 byte)
            for i in range(8):
                entry_start = 2 + i * 32
                entry_data = block[entry_start:entry_start + 32]
                
                # Dosya tipi
                file_type = entry_data[0]
                if file_type == 0:  # Boş giriş
                    continue
                
                # Track/Sector
                file_track = entry_data[1]
                file_sector = entry_data[2]
                
                # Dosya adı (16 byte)
                filename_data = entry_data[3:19]
                filename = self.petscii_to_ascii(filename_data)
                
                # Dosya boyutu (blok sayısı)
                size_blocks = entry_data[28] + (entry_data[29] << 8)
                
                # Dosya tipini decode et
                actual_file_type = file_type & self.FILE_TYPE_BITMASK
                file_type_name = self.FILE_TYPE_NAMES.get(actual_file_type, "UNK")
                
                # Dosya durumu
                is_closed = (file_type & self.FILETYPE_CLOSED_FLAG) != 0
                is_writeprotected = (file_type & self.FILETYPE_WRITEPROTECTED_FLAG) != 0
                
                entry = {
                    "filename": filename,
                    "type": file_type_name,
                    "track": file_track,
                    "sector": file_sector,
                    "size": size_blocks,
                    "closed": is_closed,
                    "writeprotected": is_writeprotected,
                    "raw_type": file_type
                }
                
                entries.append(entry)
        
        return entries
    
    def read_file_data(self, disk_data, start_track, start_sector):
        """Dosya verisini oku"""
        file_data = bytearray()
        track = start_track
        sector = start_sector
        
        while track != 0:
            # Dosya bloğunu oku
            block = self.read_block(disk_data, track, sector)
            if not block:
                break
            
            # Sonraki track/sector
            next_track = block[0]
            next_sector = block[1]
            
            # Veri kısmı (2. byte'dan itibaren)
            if next_track == 0:
                # Son blok - sadece kullanılan byte'lar
                used_bytes = next_sector - 1 if next_sector > 0 else 0
                if used_bytes > 0:
                    file_data.extend(block[2:2 + used_bytes])
            else:
                # Tam blok
                file_data.extend(block[2:])
            
            track = next_track
            sector = next_sector
        
        return bytes(file_data)
    
    def read_bam(self, disk_data):
        """BAM (Block Availability Map) oku"""
        bam_block = self.read_block(disk_data, 18, 0)
        if not bam_block:
            return None
        
        bam_info = {
            "disk_dos_version": bam_block[2],
            "disk_id": self.petscii_to_ascii(bam_block[162:164]),
            "disk_name": self.petscii_to_ascii(bam_block[144:162])
        }
        
        return bam_info
    
    def get_disk_info(self, disk_data):
        """Disk bilgilerini al"""
        bam = self.read_bam(disk_data)
        entries = self.read_directory(disk_data)
        
        info = {
            "disk_name": bam["disk_name"] if bam else "Unknown",
            "disk_id": bam["disk_id"] if bam else "00",
            "file_count": len(entries),
            "total_blocks": self.BLOCKS_OF_A_DISK,
            "files": entries
        }
        
        return info

def enhanced_c1541_read_image(file_path):
    """C1541 emülatörü ile disk okuma"""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    ext = Path(file_path).suffix.lower()
    return data, ext

def enhanced_c1541_read_directory(data, ext):
    """C1541 emülatörü ile directory okuma"""
    if ext not in ['.d64', '.d71']:
        return []
    
    emulator = C1541PythonEmulator()
    
    try:
        entries = emulator.read_directory(data)
        return entries
    except Exception as e:
        print(f"Directory okuma hatası: {e}")
        return []

def enhanced_c1541_extract_prg(data, ext, entry):
    """C1541 emülatörü ile PRG çıkarma"""
    if ext not in ['.d64', '.d71']:
        return b""
    
    emulator = C1541PythonEmulator()
    
    try:
        prg_data = emulator.read_file_data(data, entry["track"], entry["sector"])
        return prg_data
    except Exception as e:
        print(f"PRG çıkarma hatası: {e}")
        return b""

def enhanced_c1541_get_disk_info(data, ext):
    """C1541 emülatörü ile disk bilgisi"""
    if ext not in ['.d64', '.d71']:
        return None
    
    emulator = C1541PythonEmulator()
    
    try:
        info = emulator.get_disk_info(data)
        return info
    except Exception as e:
        print(f"Disk bilgisi okuma hatası: {e}")
        return None

if __name__ == "__main__":
    # Test
    test_file = "test_dosyalari/ALPA.D64"
    
    if os.path.exists(test_file):
        print(f"=== {test_file} C1541 Test ===")
        
        data, ext = enhanced_c1541_read_image(test_file)
        info = enhanced_c1541_get_disk_info(data, ext)
        
        if info:
            print(f"Disk Adı: {info['disk_name']}")
            print(f"Disk ID: {info['disk_id']}")
            print(f"Dosya Sayısı: {info['file_count']}")
            print()
            
            for i, entry in enumerate(info['files'][:10]):
                print(f"{i+1:2d}. {entry['filename']:<16} {entry['type']:>3} {entry['size']:>4} blok")
        else:
            print("Disk bilgisi okunamadı")
    else:
        print(f"Test dosyası bulunamadı: {test_file}")
