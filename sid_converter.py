# sid_converter.py
import struct
import logging
import os

# Logging yapılandırması
logging.basicConfig(filename='logs/d64_converter.log', level=logging.ERROR)

class SIDConverter:
    def __init__(self):
        self.header = b"PSID" + struct.pack("<H", 2) + struct.pack("<H", 0x76)

    def convert_to_sid(self, sid_data, output_path):
        """SID verisini .sid formatına çevirir."""
        try:
            with open(output_path, "wb") as f:
                f.write(self.header + sid_data)
            logging.info(f"SID dosyası oluşturuldu: {output_path}")
        except Exception as e:
            logging.error(f"SID çevirme hatası: {e}")

    def convert_d64_sid(self, d64_path):
        """D64 dosyasındaki SID'leri çıkarır."""
        try:
            # sid_files klasörünü oluştur
            os.makedirs("sid_files", exist_ok=True)
            
            with open(d64_path, "rb") as f:
                data = f.read()
            
            # SID header'larını ara ($1000-$2000 arasında)
            sid_found = False
            for i in range(0, len(data) - 4):
                if data[i:i+4] == b"PSID":
                    # SID bulundu
                    sid_data = data[i:i+2048]  # 2KB SID data
                    base_name = os.path.splitext(os.path.basename(d64_path))[0]
                    output_path = f"sid_files/{base_name}_{i:04x}.sid"
                    self.convert_to_sid(sid_data, output_path)
                    sid_found = True
            
            # Eğer PSID header bulunamazsa, müzik verisini ara
            if not sid_found:
                # $1000-$2000 bölgesindeki veriyi kontrol et
                for i in range(0x1000, min(0x2000, len(data))):
                    if data[i] != 0:  # Boş olmayan veri
                        # 1KB'lık blokları SID olarak kaydet
                        sid_data = data[i:i+1024]
                        base_name = os.path.splitext(os.path.basename(d64_path))[0]
                        output_path = f"sid_files/{base_name}_music_{i:04x}.sid"
                        self.convert_to_sid(sid_data, output_path)
                        sid_found = True
                        break
            
            return sid_found
            
        except Exception as e:
            logging.error(f"D64 SID çevirme hatası: {e}")
            return False

    def convert_prg_sid(self, prg_path):
        """PRG dosyasındaki SID'leri çıkarır."""
        try:
            # sid_files klasörünü oluştur
            os.makedirs("sid_files", exist_ok=True)
            
            with open(prg_path, "rb") as f:
                data = f.read()
            
            # PRG header'ı atla (2 byte)
            if len(data) > 2:
                data = data[2:]
            
            # SID header'larını ara
            sid_found = False
            for i in range(0, len(data) - 4):
                if data[i:i+4] == b"PSID":
                    # SID bulundu
                    sid_data = data[i:i+2048]  # 2KB SID data
                    base_name = os.path.splitext(os.path.basename(prg_path))[0]
                    output_path = f"sid_files/{base_name}_{i:04x}.sid"
                    self.convert_to_sid(sid_data, output_path)
                    sid_found = True
            
            # Eğer PSID header bulunamazsa, müzik verisini ara
            if not sid_found and len(data) > 512:
                # İlk 512 byte'tan sonrasını kontrol et
                for i in range(512, len(data)):
                    if data[i] != 0:  # Boş olmayan veri
                        # 1KB'lık blokları SID olarak kaydet
                        sid_data = data[i:i+1024]
                        base_name = os.path.splitext(os.path.basename(prg_path))[0]
                        output_path = f"sid_files/{base_name}_music_{i:04x}.sid"
                        self.convert_to_sid(sid_data, output_path)
                        sid_found = True
                        break
            
            return sid_found
            
        except Exception as e:
            logging.error(f"PRG SID çevirme hatası: {e}")
            return False