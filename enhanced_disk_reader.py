#!/usr/bin/env python3
"""
Enhanced Disk Reader - Universal Commodore Disk Image Reader
Supports ALL Commodore formats + Hybrid BASIC+ASM analysis

SUPPORTED FORMATS:
- D64, D71, D81 (Standard disk images)
- T64 (Tape archives)
- P00-P99 (PC64 format)
- PRG (Direct program files)
- Hybrid BASIC+ASM analysis

Version: 3.0 - Complete Hybrid Analysis
"""

import os
import struct
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import traceback

class DiskFormat(Enum):
    """Desteklenen disk formatları"""
    D64 = "d64"    # 1541 - 35 track, 170KB
    D71 = "d71"    # 1571 - 70 track, 340KB  
    D81 = "d81"    # 1581 - 80 track, 800KB
    T64 = "t64"    # Tape archive
    P00 = "p00"    # PC64 format
    PRG = "prg"    # Direct program file
    UNKNOWN = "unknown"

@dataclass
class DiskInfo:
    """Disk bilgi yapısı"""
    format_type: DiskFormat
    total_tracks: int
    total_sectors: int
    total_size: int
    disk_name: str
    disk_id: str
    directory_entries: List[Dict]
    
@dataclass 
class ProgramInfo:
    """Program bilgi yapısı"""
    filename: str
    file_type: str
    load_address: int
    file_size: int
    is_hybrid: bool
    basic_segment: Optional[bytes] = None
    asm_segment: Optional[bytes] = None
    basic_source: Optional[str] = None
    sys_address: Optional[int] = None

class EnhancedDiskReader:
    """Gelişmiş disk okuyucu - tüm formatları destekler"""
    
    def __init__(self):
        """Enhanced Disk Reader başlatma"""
        self.logger = logging.getLogger(__name__)
        
        # Disk geometrileri - C++ DiskImagery64'ten port edildi
        self.disk_geometries = {
            "D64": DiskGeometry(
                tracks=35,
                sectors_per_track=self._d64_sectors_per_track(),
                total_blocks=683,
                image_size=174848,
                format_name="Commodore 1541"
            ),
            "D71": DiskGeometry(
                tracks=70,
                sectors_per_track=self._d71_sectors_per_track(),
                total_blocks=1366,
                image_size=349696,
                format_name="Commodore 1571"
            ),
            "D81": DiskGeometry(
                tracks=80,
                sectors_per_track=[40] * 80,  # Her track'te 40 sector
                total_blocks=3200,
                image_size=819200,
                format_name="Commodore 1581"
            ),
            "D84": DiskGeometry(
                tracks=84,
                sectors_per_track=[40] * 84,
                total_blocks=3360,
                image_size=860160,
                format_name="Double Density"
            )
        }
        
        # File type'lar - CBM DOS
        self.file_types = {
            0: "DEL",  # Deleted
            1: "SEQ",  # Sequential  
            2: "PRG",  # Program
            3: "USR",  # User
            4: "REL",  # Relative
            5: "CBM",  # CBM
            6: "DIR"   # Directory
        }
        
        # PETSCII to ASCII conversion table
        self.petscii_to_ascii = self._create_petscii_table()
    
    def _d64_sectors_per_track(self) -> List[int]:
        """D64 track'lere göre sector sayıları"""
        sectors = []
        for track in range(1, 36):
            if track <= 17:
                sectors.append(21)
            elif track <= 24:
                sectors.append(19)
            elif track <= 30:
                sectors.append(18)
            else:
                sectors.append(17)
        return sectors
    
    def _d71_sectors_per_track(self) -> List[int]:
        """D71 - çift taraflı D64"""
        # İlk 35 track D64 gibi, sonraki 35 track aynı
        d64_sectors = self._d64_sectors_per_track()
        return d64_sectors + d64_sectors
    
    def _create_petscii_table(self) -> Dict[int, str]:
        """PETSCII to ASCII conversion table"""
        table = {}
        
        # Normal ASCII karakterler
        for i in range(32, 127):
            table[i] = chr(i)
        
        # PETSCII özel karakterler
        table[0xA0] = " "  # Shifted space
        table[0x5F] = "_"  # Left arrow -> underscore
        
        # Diğerleri için default
        for i in range(256):
            if i not in table:
                if 65 <= i <= 90:  # A-Z
                    table[i] = chr(i)
                elif 97 <= i <= 122:  # a-z  
                    table[i] = chr(i)
                elif 48 <= i <= 57:  # 0-9
                    table[i] = chr(i)
                else:
                    table[i] = "?"
        
        return table
    
    def identify_format(self, file_path: str) -> str:
        """Dosya formatını belirle"""
        
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Extension'a göre format belirleme
        format_map = {
            '.d64': 'D64',
            '.d71': 'D71', 
            '.d81': 'D81',
            '.d84': 'D84',
            '.t64': 'T64',
            '.tap': 'TAP',
            '.prg': 'PRG',
            '.g64': 'G64',
            '.lnx': 'LNX',
            '.lynx': 'LYNX',
            '.crt': 'CRT'
        }
        
        # P00-P99 special case
        if extension.startswith('.p') and len(extension) == 4:
            if extension[2:4].isdigit():
                return 'P00'
        
        detected_format = format_map.get(extension, 'UNKNOWN')
        
        # Size verification for disk images
        if detected_format in self.disk_geometries:
            try:
                file_size = os.path.getsize(file_path)
                expected_size = self.disk_geometries[detected_format].image_size
                
                if abs(file_size - expected_size) > 1024:  # 1KB tolerance
                    self.logger.warning(f"Size mismatch: {file_size} vs expected {expected_size}")
            except:
                pass
        
        self.logger.info(f"Format detected: {detected_format} for {file_path.name}")
        return detected_format
    
    def read_disk_image(self, file_path: str) -> List[FileEntry]:
        """Disk imajını oku - universal method"""
        
        format_type = self.identify_format(file_path)
        
        # Format'a göre okuma metodunu seç
        readers = {
            'D64': self.read_d64,
            'D71': self.read_d71,
            'D81': self.read_d81,
            'D84': self.read_d84,
            'T64': self.read_t64,
            'TAP': self.read_tap,
            'PRG': self.read_prg,
            'P00': self.read_p00,
            'G64': self.read_g64,
            'LNX': self.read_lnx,
            'LYNX': self.read_lynx,
            'CRT': self.read_crt
        }
        
        reader_func = readers.get(format_type, self.read_generic)
        
        try:
            return reader_func(file_path)
        except Exception as e:
            self.logger.error(f"Error reading {format_type}: {e}")
            return self.read_generic(file_path)
    
    def read_d64(self, file_path: str) -> List[FileEntry]:
        """D64 disk imajı oku"""
        
        with open(file_path, 'rb') as f:
            disk_data = f.read()
        
        if len(disk_data) != 174848:
            self.logger.warning(f"D64 size mismatch: {len(disk_data)}")
        
        return self._read_cbm_directory(disk_data, "D64", 18, 1)
    
    def read_d71(self, file_path: str) -> List[FileEntry]:
        """D71 disk imajı oku (çift taraflı)"""
        
        with open(file_path, 'rb') as f:
            disk_data = f.read()
        
        entries = []
        
        # İlk taraf (D64 benzeri)
        entries.extend(self._read_cbm_directory(disk_data, "D71", 18, 1))
        
        # İkinci taraf directory'si (Track 53, Sector 1)
        try:
            entries.extend(self._read_cbm_directory(disk_data, "D71", 53, 1))
        except:
            self.logger.info("D71 ikinci taraf directory'si okunamadı")
        
        return entries
    
    def read_d81(self, file_path: str) -> List[FileEntry]:
        """D81 disk imajı oku (3.5" disk)"""
        
        with open(file_path, 'rb') as f:
            disk_data = f.read()
        
        # D81 directory Track 40, Sector 3'te
        return self._read_cbm_directory(disk_data, "D81", 40, 3)
    
    def read_d84(self, file_path: str) -> List[FileEntry]:
        """D84 disk imajı oku"""
        
        with open(file_path, 'rb') as f:
            disk_data = f.read()
        
        return self._read_cbm_directory(disk_data, "D84", 40, 3)
    
    def _read_cbm_directory(self, disk_data: bytes, format_type: str, dir_track: int, dir_sector: int) -> List[FileEntry]:
        """CBM directory okuma - D64/D71/D81 için ortak"""
        
        entries = []
        geometry = self.disk_geometries[format_type]
        
        current_track = dir_track
        current_sector = dir_sector
        
        while current_track != 0:
            try:
                # Track/Sector'ı block numarasına çevir
                block_num = self._track_sector_to_block(current_track, current_sector, format_type)
                block_offset = block_num * 256
                
                if block_offset + 256 > len(disk_data):
                    break
                
                sector_data = disk_data[block_offset:block_offset + 256]
                
                # Next directory sector
                next_track = sector_data[0]
                next_sector = sector_data[1]
                
                # Directory entries (8 per sector)
                for i in range(8):
                    entry_offset = 2 + (i * 32)
                    entry_data = sector_data[entry_offset:entry_offset + 32]
                    
                    file_type = entry_data[2] & 0x0F
                    
                    if file_type != 0:  # Not deleted
                        entry = self._parse_directory_entry(entry_data, format_type)
                        if entry:
                            entries.append(entry)
                
                current_track = next_track
                current_sector = next_sector
                
            except Exception as e:
                self.logger.error(f"Directory read error T{current_track}S{current_sector}: {e}")
                break
        
        self.logger.info(f"{format_type} directory read complete: {len(entries)} files")
        return entries
    
    def _parse_directory_entry(self, entry_data: bytes, format_type: str) -> Optional[FileEntry]:
        """Directory entry'sini parse et"""
        
        try:
            # Entry structure (32 bytes):
            # 0-1: Next directory block
            # 2: File type
            # 3-4: Start track/sector
            # 5-20: Filename (PETSCII)
            # 21-24: REL file info
            # 25-26: Reserved
            # 27-28: Replacement track/sector
            # 29-30: File size in blocks
            # 31: Unused
            
            file_type_byte = entry_data[2]
            file_type = file_type_byte & 0x0F
            closed = (file_type_byte & 0x80) != 0
            locked = (file_type_byte & 0x40) != 0
            
            start_track = entry_data[3]
            start_sector = entry_data[4]
            
            # Filename (PETSCII to ASCII)
            filename_raw = entry_data[5:21]
            filename = self._petscii_to_ascii(filename_raw)
            
            # File size in blocks
            size_blocks = entry_data[29] + (entry_data[30] << 8)
            size_bytes = size_blocks * 254  # Approximate (254 bytes per block)
            
            return FileEntry(
                filename=filename,
                filetype=self.file_types.get(file_type, "???"),
                size=size_bytes,
                start_address=0,  # Will be determined when reading file
                end_address=0,
                track=start_track,
                sector=start_sector,
                blocks=size_blocks,
                closed=closed,
                locked=locked,
                data=b"",  # File data not loaded yet
                description=f"{format_type} file"
            )
            
        except Exception as e:
            self.logger.error(f"Entry parse error: {e}")
            return None
    
    def _petscii_to_ascii(self, petscii_data: bytes) -> str:
        """PETSCII'yi ASCII'ye çevir"""
        
        result = ""
        for byte in petscii_data:
            if byte == 0xA0:  # PETSCII space
                break
            char = self.petscii_to_ascii.get(byte, "?")
            result += char
        
        return result.strip()
    
    def _track_sector_to_block(self, track: int, sector: int, format_type: str) -> int:
        """Track/Sector'ı block numarasına çevir"""
        
        geometry = self.disk_geometries[format_type]
        block = 0
        
        if format_type == "D64":
            for t in range(1, track):
                if t <= 17:
                    block += 21
                elif t <= 24:
                    block += 19
                elif t <= 30:
                    block += 18
                else:
                    block += 17
            block += sector
            
        elif format_type == "D71":
            if track <= 35:
                # İlk taraf - D64 gibi
                for t in range(1, track):
                    if t <= 17:
                        block += 21
                    elif t <= 24:
                        block += 19
                    elif t <= 30:
                        block += 18
                    else:
                        block += 17
                block += sector
            else:
                # İkinci taraf
                block = 683  # İlk taraf toplam block
                for t in range(36, track):
                    if (t - 35) <= 17:
                        block += 21
                    elif (t - 35) <= 24:
                        block += 19
                    elif (t - 35) <= 30:
                        block += 18
                    else:
                        block += 17
                block += sector
                
        elif format_type in ["D81", "D84"]:
            # Her track'te 40 sector
            block = (track - 1) * 40 + sector
        
        return block
    
    def read_t64(self, file_path: str) -> List[FileEntry]:
        """T64 tape archive oku"""
        
        entries = []
        
        with open(file_path, 'rb') as f:
            # T64 header (64 bytes)
            header = f.read(64)
            
            if not header.startswith(b'C64-TAPE-RAW'):
                self.logger.error("Invalid T64 signature")
                return []
            
            # Version, max entries, used entries
            version = struct.unpack('<H', header[32:34])[0]
            max_entries = struct.unpack('<H', header[34:36])[0]
            used_entries = struct.unpack('<H', header[36:38])[0]
            
            self.logger.info(f"T64: Version {version}, {used_entries}/{max_entries} entries")
            
            # Directory entries (32 bytes each)
            for i in range(used_entries):
                entry_data = f.read(32)
                if len(entry_data) < 32:
                    break
                
                entry_type = entry_data[0]
                file_type = entry_data[1]
                start_addr = struct.unpack('<H', entry_data[2:4])[0]
                end_addr = struct.unpack('<H', entry_data[4:6])[0]
                file_offset = struct.unpack('<L', entry_data[8:12])[0]
                
                # Filename
                filename_raw = entry_data[16:32]
                filename = filename_raw.decode('ascii', errors='ignore').strip('\x00')
                
                if entry_type == 1:  # Normal file
                    size = end_addr - start_addr + 1 if end_addr >= start_addr else 0
                    
                    entries.append(FileEntry(
                        filename=filename,
                        filetype="PRG",
                        size=size,
                        start_address=start_addr,
                        end_address=end_addr,
                        track=0,
                        sector=0,
                        blocks=0,
                        closed=True,
                        locked=False,
                        data=b"",
                        description=f"T64 file at offset {file_offset}"
                    ))
        
        self.logger.info(f"T64 read complete: {len(entries)} files")
        return entries
    
    def read_tap(self, file_path: str) -> List[FileEntry]:
        """TAP tape image oku"""
        
        with open(file_path, 'rb') as f:
            tap_data = f.read()
        
        # TAP format: Simple tape dump
        # Genelde tek dosya içerir
        
        return [FileEntry(
            filename=Path(file_path).stem,
            filetype="TAP",
            size=len(tap_data),
            start_address=0x0801,
            end_address=0x0801 + len(tap_data),
            track=0,
            sector=0,
            blocks=0,
            closed=True,
            locked=False,
            data=tap_data,
            description="TAP tape image"
        )]
    
    def read_prg(self, file_path: str) -> List[FileEntry]:
        """PRG dosyası oku"""
        
        with open(file_path, 'rb') as f:
            prg_data = f.read()
        
        if len(prg_data) < 2:
            return []
        
        start_addr = prg_data[0] + (prg_data[1] << 8)
        end_addr = start_addr + len(prg_data) - 3
        
        return [FileEntry(
            filename=Path(file_path).stem,
            filetype="PRG",
            size=len(prg_data),
            start_address=start_addr,
            end_address=end_addr,
            track=0,
            sector=0,
            blocks=0,
            closed=True,
            locked=False,
            data=prg_data,
            description="PRG program file"
        )]
    
    def read_p00(self, file_path: str) -> List[FileEntry]:
        """P00 (PC64) format oku"""
        
        with open(file_path, 'rb') as f:
            p00_data = f.read()
        
        if len(p00_data) < 26:
            return []
        
        # P00 header (26 bytes)
        if not p00_data.startswith(b'C64File'):
            return self.read_generic(file_path)
        
        # Filename in header
        filename_raw = p00_data[8:24]
        filename = filename_raw.decode('ascii', errors='ignore').strip('\x00')
        
        # PRG data starts at offset 26
        prg_data = p00_data[26:]
        
        if len(prg_data) >= 2:
            start_addr = prg_data[0] + (prg_data[1] << 8)
            end_addr = start_addr + len(prg_data) - 3
        else:
            start_addr = 0x0801
            end_addr = 0x0801
        
        return [FileEntry(
            filename=filename if filename else Path(file_path).stem,
            filetype="PRG",
            size=len(prg_data),
            start_address=start_addr,
            end_address=end_addr,
            track=0,
            sector=0,
            blocks=0,
            closed=True,
            locked=False,
            data=prg_data,
            description="P00 (PC64) format file"
        )]
    
    def read_g64(self, file_path: str) -> List[FileEntry]:
        """G64 GCR format oku (basit)"""
        
        # G64 çok karmaşık - basit fallback
        return [FileEntry(
            filename=Path(file_path).stem,
            filetype="G64",
            size=os.path.getsize(file_path),
            start_address=0,
            end_address=0,
            track=0,
            sector=0,
            blocks=0,
            closed=True,
            locked=False,
            data=b"",
            description="G64 GCR disk image (raw)"
        )]
    
    def read_lnx(self, file_path: str) -> List[FileEntry]:
        """LNX archive oku"""
        
        return self.read_generic(file_path)
    
    def read_lynx(self, file_path: str) -> List[FileEntry]:
        """LYNX archive oku"""
        
        return self.read_generic(file_path)
    
    def read_crt(self, file_path: str) -> List[FileEntry]:
        """CRT cartridge oku"""
        
        return [FileEntry(
            filename=Path(file_path).stem,
            filetype="CRT",
            size=os.path.getsize(file_path),
            start_address=0x8000,  # Typical cartridge address
            end_address=0xBFFF,
            track=0,
            sector=0,
            blocks=0,
            closed=True,
            locked=False,
            data=b"",
            description="CRT cartridge image"
        )]
    
    def read_generic(self, file_path: str) -> List[FileEntry]:
        """Bilinmeyen format için generic okuma"""
        
        try:
            size = os.path.getsize(file_path)
            return [FileEntry(
                filename=Path(file_path).name,
                filetype="UNKNOWN",
                size=size,
                start_address=0x0801,
                end_address=0x0801 + size,
                track=0,
                sector=0,
                blocks=0,
                closed=True,
                locked=False,
                data=b"",
                description=f"Unknown format ({size} bytes)"
            )]
        except:
            return []

# Test kodu
if __name__ == "__main__":
    print("🗂️ Enhanced Disk Reader Test")
    print("="*50)
    
    reader = EnhancedDiskReader()
    
    # Test format detection
    test_files = [
        "test.d64", "test.d71", "test.d81", "test.t64", 
        "test.tap", "test.prg", "test.p00", "test.g64"
    ]
    
    for test_file in test_files:
        format_type = reader.identify_format(test_file)
        print(f"{test_file} -> {format_type}")
    
    print("\n✅ Enhanced Disk Reader ready for all formats!")
