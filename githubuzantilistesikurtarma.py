import os
import subprocess

UZANTI_LISTESI_DOSYASI = "vscode_uzantilar.txt"  # Bu dosyada uzantı ID'leri olmalı (her satırda bir tane)

def uzantilari_yukle(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        print(f"❌ Dosya bulunamadı: {dosya_yolu}")
        return

    with open(dosya_yolu, "r", encoding="utf-8") as f:
        uzantilar = [satir.strip() for satir in f if satir.strip()]

    print(f"🔎 Toplam {len(uzantilar)} uzantı bulunuyor. Yükleme başlıyor...\n")

    for uzanti in uzantilar:
        print(f"➕ {uzanti} yükleniyor...")
        try:
            subprocess.run(["code", "--install-extension", uzanti], check=True)
            print(f"✅ {uzanti} başarıyla yüklendi.\n")
        except subprocess.CalledProcessError:
            print(f"⚠️  {uzanti} yüklenemedi.\n")

if __name__ == "__main__":
    uzantilari_yukle(UZANTI_LISTESI_DOSYASI)
