# d64_reader.py
import struct
from pathlib import Path
import logging

# Logging yapılandırması
logging.basicConfig(filename='logs/d64_converter.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Disk format sabitleri
D64_SECTOR_COUNT = 683
D71_SECTOR_COUNT = 1366  # Double-sided D64
D81_SECTOR_COUNT = 3200
D84_SECTOR_COUNT = 6400  # Double-sided D81

# Sector sayıları track başına
SECTOR_SIZES = [
    21 if t <= 17 else 19 if t <= 24 else 18 if t <= 30 else 17
    for t in range(1, 36)
]
D71_SECTOR_SIZES = SECTOR_SIZES + SECTOR_SIZES  # Her iki yüz için
D81_SECTOR_SIZES = [40] * 80
D84_SECTOR_SIZES = [40] * 160  # Double-sided

# Track offsetleri
TRACK_OFFSETS = [0]
for t in range(1, 35):
    TRACK_OFFSETS.append(TRACK_OFFSETS[-1] + SECTOR_SIZES[t - 1])

D71_TRACK_OFFSETS = TRACK_OFFSETS + [TRACK_OFFSETS[-1] + sector for sector in TRACK_OFFSETS[1:]]

D81_TRACK_OFFSETS = [0]
for t in range(1, 80):
    D81_TRACK_OFFSETS.append(D81_TRACK_OFFSETS[-1] + D81_SECTOR_SIZES[t - 1])

D84_TRACK_OFFSETS = [0]
for t in range(1, 160):
    D84_TRACK_OFFSETS.append(D84_TRACK_OFFSETS[-1] + D84_SECTOR_SIZES[t - 1])

def read_image(file_path):
    """D64, D71, D81, D84, TAP, T64, P00, PRG, LNX, CRT, BIN dosyalarını okur."""
    try:
        ext = Path(file_path).suffix.lower()
        with open(file_path, "rb") as f:
            data = bytearray(f.read())
        
        # Format validation
        if ext == ".d64" and len(data) < D64_SECTOR_COUNT * 256:
            raise ValueError("Geçersiz D64 dosyası - boyut çok küçük")
        elif ext == ".d71" and len(data) < D71_SECTOR_COUNT * 256:
            raise ValueError("Geçersiz D71 dosyası - boyut çok küçük")
        elif ext == ".d81" and len(data) < D81_SECTOR_COUNT * 256:
            raise ValueError("Geçersiz D81 dosyası - boyut çok küçük")
        elif ext == ".d84" and len(data) < D84_SECTOR_COUNT * 256:
            raise ValueError("Geçersiz D84 dosyası - boyut çok küçük")
        elif ext == ".tap" and len(data) < 20:
            # TAP minimum header kontrolü
            raise ValueError("Geçersiz TAP dosyası - boyut çok küçük")
        elif ext == ".t64" and len(data) < 64:
            raise ValueError("Geçersiz T64 dosyası - boyut çok küçük")
        elif ext == ".p00" and len(data) < 26:
            raise ValueError("Geçersiz P00 dosyası - boyut çok küçük")
        elif ext == ".prg" and len(data) < 3:
            raise ValueError("Geçersiz PRG dosyası - boyut çok küçük")
        elif ext in [".lnx", ".lynx"] and len(data) < 32:
            raise ValueError("Geçersiz LNX dosyası - boyut çok küçük")
        elif ext == ".crt" and len(data) < 64:
            raise ValueError("Geçersiz CRT dosyası - boyut çok küçük")
        elif ext == ".bin" and len(data) < 1:
            raise ValueError("Geçersiz BIN dosyası - boyut çok küçük")
        elif ext == ".g64" and len(data) < 256:
            raise ValueError("Geçersiz G64 dosyası - boyut çok küçük")
        
        logging.info(f"Dosya okundu: {file_path}, Format: {ext}, Boyut: {len(data)} bytes")
        return data, ext
    except Exception as e:
        logging.error(f"Dosya okuma hatası ({file_path}): {e}")
        raise Exception(f"Dosya okuma hatası: {e}")

def get_sector_offset(track, sector, ext):
    """Track ve sector için dosya ofsetini hesaplar."""
    try:
        if ext == ".d64":
            if not (1 <= track <= 35):
                return -1
            if sector >= SECTOR_SIZES[track - 1]:
                return -1
            index = TRACK_OFFSETS[track - 1] + sector
            return index * 256
        elif ext == ".d71":
            if not (1 <= track <= 70):
                return -1
            # D71 iki taraflı: track 36-70 ikinci taraf
            if track <= 35:
                if sector >= SECTOR_SIZES[track - 1]:
                    return -1
                index = TRACK_OFFSETS[track - 1] + sector
            else:
                # İkinci taraf (track 36-70 -> track 1-35 ikinci taraf)
                real_track = track - 35
                if sector >= SECTOR_SIZES[real_track - 1]:
                    return -1
                index = TRACK_OFFSETS[34] + TRACK_OFFSETS[real_track - 1] + sector
            return index * 256
        elif ext == ".d81":
            if not (1 <= track <= 80):
                return -1
            if sector >= D81_SECTOR_SIZES[track - 1]:
                return -1
            index = D81_TRACK_OFFSETS[track - 1] + sector
            return index * 256
        elif ext == ".d84":
            if not (1 <= track <= 160):
                return -1
            if sector >= D84_SECTOR_SIZES[track - 1]:
                return -1
            index = D84_TRACK_OFFSETS[track - 1] + sector
            return index * 256
        return -1
    except Exception as e:
        logging.error(f"Sector offset hesaplama hatası: {e}")
        return -1

def read_directory(disk_data, ext):
    """Disk formatına göre dosya dizinini okur."""
    dir_entries = []
    
    try:
        if ext == ".d64":
            track, sector = 18, 1  # D64 directory track/sector
        elif ext == ".d71":
            track, sector = 18, 1  # D71 directory track/sector  
        elif ext == ".d81":
            track, sector = 40, 3  # D81 directory track/sector
        elif ext == ".d84":
            track, sector = 40, 3  # D84 directory track/sector
        else:
            logging.warning(f"Directory okuma desteklenmiyor: {ext}")
            return dir_entries

        logging.info(f"Directory okunuyor: {ext}, Track: {track}, Sector: {sector}")
        sector_count = 0
        max_sectors = 50  # Sonsuz döngü koruması
        
        while sector_count < max_sectors:
            offset = get_sector_offset(track, sector, ext)
            if offset < 0:
                logging.warning(f"Geçersiz directory offset: Track {track}, Sector {sector}")
                break
                
            if offset + 256 > len(disk_data):
                logging.warning(f"Directory offset disk boyutunu aşıyor: {offset}")
                break
                
            next_track = disk_data[offset]
            next_sector = disk_data[offset + 1]
            
            logging.debug(f"Directory sector {sector_count}: Track {track}, Sector {sector}, Next: {next_track}/{next_sector}")
            
            # Directory entries (8 entry per sector)
            for i in range(8):
                entry_offset = offset + 2 + (i * 32)
                if entry_offset + 32 > len(disk_data):
                    break
                    
                file_type = disk_data[entry_offset + 2]
                
                # Dosya mevcut mu kontrol et (bit 7 set olmalı)
                if file_type & 0x80 == 0:
                    continue
                    
                # Filename decode (PETSCII to ASCII)
                filename_bytes = disk_data[entry_offset + 5:entry_offset + 21]
                filename = ""
                for b in filename_bytes:
                    if b == 0xa0:  # PETSCII space
                        break
                    elif 32 <= b <= 126:  # ASCII printable
                        filename += chr(b)
                    else:
                        filename += f"\\x{b:02x}"
                
                filename = filename.strip()
                if not filename:
                    continue
                    
                start_track = disk_data[entry_offset + 3]
                start_sector = disk_data[entry_offset + 4]
                file_size_lo = disk_data[entry_offset + 28]  # 30 değil 28
                file_size_hi = disk_data[entry_offset + 29]  # 31 değil 29
                file_size = file_size_lo + (file_size_hi << 8)
                
                # Dosya tipi decode (CBM DOS file types)
                file_type_raw = file_type & 0x07  # Lower 3 bits
                closed = (file_type & 0x80) != 0  # Bit 7
                
                file_type_names = {
                    0: "DEL",  # Deleted
                    1: "SEQ",  # Sequential
                    2: "PRG",  # Program
                    3: "USR",  # User
                    4: "REL",  # Relative
                    5: "CBM",  # CBM
                    6: "DIR"   # Directory (rare)
                }
                
                file_type_name = file_type_names.get(file_type_raw, f"T{file_type_raw}")
                if not closed:
                    file_type_name += "*"  # Unclosed file
                
                dir_entries.append({
                    "filename": filename,
                    "track": start_track,
                    "sector": start_sector,
                    "size_blocks": file_size,
                    "file_type": file_type_name,
                    "raw_type": file_type
                })
                
                logging.debug(f"Dosya bulundu: {filename} ({file_type_name}), Track: {start_track}, Sector: {start_sector}")
            
            # Sonraki directory sector'e geç
            if next_track == 0:
                break
            track, sector = next_track, next_sector
            sector_count += 1
            
        logging.info(f"Directory okuma tamamlandı: {len(dir_entries)} dosya bulundu")
        return dir_entries
        
    except Exception as e:
        logging.error(f"Directory okuma hatası ({ext}): {e}")
        return []

def read_t64_directory(t64_data):
    """T64 dosyasından dizini okur."""
    dir_entries = []
    try:
        if len(t64_data) < 64:
            raise ValueError("T64 dosyası çok küçük")
            
        # T64 header kontrol
        header = t64_data[0:32].decode("ascii", errors="ignore")
        if not ("C64" in header or "T64" in header):
            logging.warning("T64 header kontrolü başarısız, devam ediliyor...")
            
        # Entry sayısı
        max_entries = int.from_bytes(t64_data[34:36], "little")
        used_entries = int.from_bytes(t64_data[36:38], "little")
        
        logging.info(f"T64: Max entries: {max_entries}, Used: {used_entries}")
        
        for i in range(min(max_entries, 64)):  # Maksimum 64 entry kontrol et
            entry_offset = 64 + i * 32
            if entry_offset + 32 > len(t64_data):
                break
                
            file_type = t64_data[entry_offset]
            if file_type != 1:  # Sadece PRG dosyaları (type 1)
                continue
                
            # Filename decode
            filename_bytes = t64_data[entry_offset + 16:entry_offset + 32]
            filename = ""
            for b in filename_bytes:
                if b == 0:
                    break
                elif 32 <= b <= 126:
                    filename += chr(b)
                else:
                    filename += f"\\x{b:02x}"
                    
            filename = filename.strip()
            if not filename:
                filename = f"FILE_{i}"
                
            start_addr = int.from_bytes(t64_data[entry_offset + 2:entry_offset + 4], "little")
            end_addr = int.from_bytes(t64_data[entry_offset + 4:entry_offset + 6], "little")
            file_offset = int.from_bytes(t64_data[entry_offset + 8:entry_offset + 12], "little")
            
            if file_offset > 0 and file_offset < len(t64_data):
                file_size = end_addr - start_addr if end_addr > start_addr else 0
                dir_entries.append({
                    "filename": filename,
                    "start_addr": start_addr,
                    "end_addr": end_addr,
                    "offset": file_offset,
                    "size": file_size
                })
                logging.debug(f"T64 dosya: {filename}, Addr: ${start_addr:04X}-${end_addr:04X}")
                
        logging.info(f"T64 directory: {len(dir_entries)} dosya bulundu")
        return dir_entries
        
    except Exception as e:
        logging.error(f"T64 directory okuma hatası: {e}")
        return []

def read_tap_directory(tap_data):
    """TAP dosyasından program listesini çıkarır."""
    dir_entries = []
    try:
        if len(tap_data) < 20:
            raise ValueError("TAP dosyası çok küçük")
            
        # TAP header
        signature = tap_data[0:12]
        version = tap_data[12]
        platform = tap_data[13]
        video_standard = tap_data[14]
        
        logging.info(f"TAP: Version {version}, Platform {platform}, Video {video_standard}")
        
        offset = 20  # TAP data başlangıcı
        file_count = 0
        
        while offset < len(tap_data) - 4 and file_count < 100:  # Maksimum 100 dosya
            # TAP pulse veri uzunluğu
            pulse_length = int.from_bytes(tap_data[offset:offset+4], "little")
            
            if pulse_length == 0:
                offset += 4
                break
                
            if offset + 4 + pulse_length > len(tap_data):
                break
                
            # Basit TAP dosya tespiti (C64 loader pattern arama)
            pulse_data = tap_data[offset + 4:offset + 4 + pulse_length]
            
            # CBM header pattern arama (sync pattern + identifier)
            if len(pulse_data) > 200:  # Minimum dosya boyutu
                filename = f"TAPE_PROGRAM_{file_count + 1}"
                
                dir_entries.append({
                    "filename": filename,
                    "offset": offset + 4,
                    "size": pulse_length,
                    "type": "TAP_DATA"
                })
                file_count += 1
                logging.debug(f"TAP program bulundu: {filename}, Size: {pulse_length}")
                
            offset += 4 + pulse_length
            
        if not dir_entries:
            # Fallback: Tek program olarak tüm veriyi ekle
            dir_entries.append({
                "filename": "TAPE_PROGRAM",
                "offset": 20,
                "size": len(tap_data) - 20,
                "type": "TAP_RAW"
            })
            
        logging.info(f"TAP directory: {len(dir_entries)} program bulundu")
        return dir_entries
        
    except Exception as e:
        logging.error(f"TAP directory okuma hatası: {e}")
        return []

def extract_prg_file(disk_data, start_track, start_sector, ext):
    """PRG dosyasını diskten çıkarır."""
    try:
        blocks = []
        sector_count = 0
        max_sectors = 200  # Sonsuz döngü koruması
        
        while sector_count < max_sectors:
            offset = get_sector_offset(start_track, start_sector, ext)
            if offset < 0:
                raise ValueError(f"Geçersiz track/sector: {start_track}/{start_sector}")
                
            if offset + 256 > len(disk_data):
                raise ValueError(f"Disk veri sınırı aşıldı: {offset}")
                
            next_track = disk_data[offset]
            next_sector = disk_data[offset + 1]
            
            # Son sector'da sadece kullanılan byte'ları al
            if next_track == 0:
                # Son sector - sadece kullanılan kısmı al
                used_bytes = next_sector if next_sector > 0 else 254
                blocks.append(disk_data[offset + 2: offset + 2 + used_bytes])
                break
            else:
                # Tam sector
                blocks.append(disk_data[offset + 2: offset + 256])
                
            start_track, start_sector = next_track, next_sector
            sector_count += 1
            
        prg_data = b''.join(blocks)
        logging.info(f"PRG çıkarıldı: {len(prg_data)} byte, {sector_count + 1} sector")
        return prg_data
        
    except Exception as e:
        logging.error(f"PRG çıkarma hatası: {e}")
        raise Exception(f"PRG çıkarma hatası: {e}")

def extract_seq_file(disk_data, start_track, start_sector, ext):
    """SEQ (Sequential) dosyasını diskten çıkarır."""
    try:
        blocks = []
        sector_count = 0
        max_sectors = 200  # Sonsuz döngü koruması
        
        while sector_count < max_sectors:
            offset = get_sector_offset(start_track, start_sector, ext)
            if offset < 0:
                raise ValueError(f"Geçersiz track/sector: {start_track}/{start_sector}")
                
            if offset + 256 > len(disk_data):
                raise ValueError(f"Disk veri sınırı aşıldı: {offset}")
                
            next_track = disk_data[offset]
            next_sector = disk_data[offset + 1]
            
            # Son sector'da sadece kullanılan byte'ları al
            if next_track == 0:
                # Son sector - sadece kullanılan kısmı al
                used_bytes = next_sector if next_sector > 0 else 254
                blocks.append(disk_data[offset + 2: offset + 2 + used_bytes])
                break
            else:
                # Tam sector
                blocks.append(disk_data[offset + 2: offset + 256])
                
            start_track, start_sector = next_track, next_sector
            sector_count += 1
            
        seq_data = b''.join(blocks)
        logging.info(f"SEQ çıkarıldı: {len(seq_data)} byte, {sector_count + 1} sector")
        return seq_data
        
    except Exception as e:
        logging.error(f"SEQ çıkarma hatası: {e}")
        raise Exception(f"SEQ çıkarma hatası: {e}")

def extract_usr_file(disk_data, start_track, start_sector, ext):
    """USR dosyasını diskten çıkarır."""
    try:
        blocks = []
        sector_count = 0
        max_sectors = 200  # Sonsuz döngü koruması
        
        while sector_count < max_sectors:
            offset = get_sector_offset(start_track, start_sector, ext)
            if offset < 0:
                raise ValueError(f"Geçersiz track/sector: {start_track}/{start_sector}")
                
            if offset + 256 > len(disk_data):
                raise ValueError(f"Disk veri sınırı aşıldı: {offset}")
                
            next_track = disk_data[offset]
            next_sector = disk_data[offset + 1]
            
            # Son sector'da sadece kullanılan byte'ları al
            if next_track == 0:
                # Son sector - sadece kullanılan kısmı al
                used_bytes = next_sector if next_sector > 0 else 254
                blocks.append(disk_data[offset + 2: offset + 2 + used_bytes])
                break
            else:
                # Tam sector
                blocks.append(disk_data[offset + 2: offset + 256])
                
            start_track, start_sector = next_track, next_sector
            sector_count += 1
            
        usr_data = b''.join(blocks)
        logging.info(f"USR çıkarıldı: {len(usr_data)} byte, {sector_count + 1} sector")
        return usr_data
        
    except Exception as e:
        logging.error(f"USR çıkarma hatası: {e}")
        raise Exception(f"USR çıkarma hatası: {e}")

def extract_del_file(disk_data, start_track, start_sector, ext):
    """DEL (Deleted) dosyasını diskten çıkarır."""
    try:
        # DEL dosyaları silinmiş dosyalar - genellikle kurtarma için
        blocks = []
        sector_count = 0
        max_sectors = 200  # Sonsuz döngü koruması
        
        while sector_count < max_sectors:
            offset = get_sector_offset(start_track, start_sector, ext)
            if offset < 0:
                raise ValueError(f"Geçersiz track/sector: {start_track}/{start_sector}")
                
            if offset + 256 > len(disk_data):
                raise ValueError(f"Disk veri sınırı aşıldı: {offset}")
                
            next_track = disk_data[offset]
            next_sector = disk_data[offset + 1]
            
            # Son sector'da sadece kullanılan byte'ları al
            if next_track == 0:
                # Son sector - sadece kullanılan kısmı al
                used_bytes = next_sector if next_sector > 0 else 254
                blocks.append(disk_data[offset + 2: offset + 2 + used_bytes])
                break
            else:
                # Tam sector
                blocks.append(disk_data[offset + 2: offset + 256])
                
            start_track, start_sector = next_track, next_sector
            sector_count += 1
            
        del_data = b''.join(blocks)
        logging.info(f"DEL çıkarıldı: {len(del_data)} byte, {sector_count + 1} sector")
        return del_data
        
    except Exception as e:
        logging.error(f"DEL çıkarma hatası: {e}")
        raise Exception(f"DEL çıkarma hatası: {e}")

def extract_t64_prg(t64_data, offset, size):
    """T64 dosyasından PRG'yi çıkarır."""
    try:
        if offset + size > len(t64_data):
            # Dosya boyutu aşılırsa mevcut veriyi al
            size = len(t64_data) - offset
            
        prg_data = t64_data[offset:offset + size]
        logging.info(f"T64 PRG çıkarıldı: {len(prg_data)} byte")
        return prg_data
    except Exception as e:
        logging.error(f"T64 PRG çıkarma hatası: {e}")
        raise Exception(f"T64 PRG çıkarma hatası: {e}")

def extract_tap_prg(tap_data, offset, size):
    """TAP dosyasından program verisi çıkarır."""
    try:
        if offset + size > len(tap_data):
            size = len(tap_data) - offset
            
        prg_data = tap_data[offset:offset + size]
        
        # TAP verisi binary pulse data - C64 program'a çevirmek için 
        # basit pulse-to-byte conversion (gerçek TAP decoder gerekir)
        # Şimdilik raw data olarak döndür
        
        logging.info(f"TAP program çıkarıldı: {len(prg_data)} byte")
        return prg_data
    except Exception as e:
        logging.error(f"TAP çıkarma hatası: {e}")
        raise Exception(f"TAP çıkarma hatası: {e}")

def extract_p00_prg(p00_data):
    """P00 dosyasından PRG verisi çıkarır."""
    try:
        if len(p00_data) < 26:
            raise ValueError("P00 dosyası çok küçük")
            
        # P00 header: 8 byte signature + 16 byte filename + 2 byte record size
        signature = p00_data[0:8]
        filename = p00_data[8:24]
        
        # PRG verisi offset 26'dan başlar
        prg_data = p00_data[26:]
        
        logging.info(f"P00 PRG çıkarıldı: {len(prg_data)} byte")
        return prg_data
    except Exception as e:
        logging.error(f"P00 çıkarma hatası: {e}")
        raise Exception(f"P00 çıkarma hatası: {e}")
