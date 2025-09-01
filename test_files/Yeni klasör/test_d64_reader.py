from d64_reader import *

# Test D64 dosyasını oku
data, ext = read_image('test.d64')
print(f"Dosya okundu: {ext}, Boyut: {len(data)} bytes")

# Directory'yi oku
entries = read_directory(data, ext)
print(f'Bulunan dosyalar: {len(entries)}')

for e in entries:
    print(f"- {e['filename']} ({e.get('file_type', 'Unknown')})")
    print(f"  Track: {e['track']}, Sector: {e['sector']}, Size: {e['size_blocks']} blocks")
