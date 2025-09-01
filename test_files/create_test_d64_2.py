"""
D64 test dosyası oluşturma scripti - Doğru CBM DOS yapısı ile
"""
import os

# Basit D64 header oluştur (dummy data)
d64_size = 683 * 256  # Standard D64 size (35 tracks * variable sectors * 256 bytes)
d64_data = bytearray(d64_size)

# Track/Sector calculation for D64
def get_d64_offset(track, sector):
    """D64 dosyasında track/sector için offset hesapla"""
    if track < 1 or track > 35:
        return -1
    
    # Track başına sector sayıları
    if track <= 17:
        sectors_per_track = 21
    elif track <= 24:
        sectors_per_track = 19
    elif track <= 30:
        sectors_per_track = 18
    else:
        sectors_per_track = 17
    
    if sector >= sectors_per_track:
        return -1
    
    # Track offset hesapla
    offset = 0
    for t in range(1, track):
        if t <= 17:
            offset += 21 * 256
        elif t <= 24:
            offset += 19 * 256
        elif t <= 30:
            offset += 18 * 256
        else:
            offset += 17 * 256
    
    offset += sector * 256
    return offset

# BAM sector (Track 18, Sector 0) - Block Allocation Map
bam_offset = get_d64_offset(18, 0)

# BAM header oluştur
d64_data[bam_offset] = 18      # Directory track
d64_data[bam_offset + 1] = 1   # Directory sector
d64_data[bam_offset + 2] = 0x41 # DOS version "A"
d64_data[bam_offset + 3] = 0   # Unused

# Disk name: "TEST DISK      " (16 chars padded with 0xA0)
disk_name = "TEST DISK"
for i, char in enumerate(disk_name):
    d64_data[bam_offset + 0x90 + i] = ord(char)
for i in range(len(disk_name), 16):
    d64_data[bam_offset + 0x90 + i] = 0xa0  # PETSCII space

# Disk ID: "2A" 
d64_data[bam_offset + 0xa2] = ord('2')
d64_data[bam_offset + 0xa3] = ord('A')
d64_data[bam_offset + 0xa4] = 0xa0  # PETSCII space
d64_data[bam_offset + 0xa5] = ord('2')
d64_data[bam_offset + 0xa6] = ord('A')

# Directory entry oluştur (Track 18, Sector 1)
dir_offset = get_d64_offset(18, 1)

# Directory sector header
d64_data[dir_offset] = 0      # Next track (0 = end)
d64_data[dir_offset + 1] = 255  # Next sector (255 = end)

# İlk dosya entry (32 bytes)
entry_offset = dir_offset + 2
d64_data[entry_offset + 0] = 0x00   # Next entry track (0 = empty)
d64_data[entry_offset + 1] = 0x00   # Next entry sector
d64_data[entry_offset + 2] = 0x82   # File type: PRG, closed (0x82)
d64_data[entry_offset + 3] = 2      # Start track
d64_data[entry_offset + 4] = 0      # Start sector

# Filename: "HELLO WORLD" (16 chars padded with 0xA0)
filename = "HELLO WORLD"
for i, char in enumerate(filename):
    d64_data[entry_offset + 5 + i] = ord(char)
for i in range(len(filename), 16):
    d64_data[entry_offset + 5 + i] = 0xa0  # PETSCII space

# Unused bytes
for i in range(21, 28):
    d64_data[entry_offset + i] = 0x00

# File size in blocks
d64_data[entry_offset + 28] = 1  # Low byte
d64_data[entry_offset + 29] = 0  # High byte

# İkinci dosya entry - Assembly program
entry_offset2 = dir_offset + 2 + 32
d64_data[entry_offset2 + 0] = 0x00   # Next entry track (0 = empty)
d64_data[entry_offset2 + 1] = 0x00   # Next entry sector
d64_data[entry_offset2 + 2] = 0x82   # File type: PRG, closed (0x82)
d64_data[entry_offset2 + 3] = 3      # Start track
d64_data[entry_offset2 + 4] = 0      # Start sector

# Filename: "ASM DEMO" (16 chars padded with 0xA0)
filename2 = "ASM DEMO"
for i, char in enumerate(filename2):
    d64_data[entry_offset2 + 5 + i] = ord(char)
for i in range(len(filename2), 16):
    d64_data[entry_offset2 + 5 + i] = 0xa0  # PETSCII space

# File size in blocks
d64_data[entry_offset2 + 28] = 1  # Low byte
d64_data[entry_offset2 + 29] = 0  # High byte

# Test PRG data #1: BASIC program (Track 2, Sector 0)
prg_offset = get_d64_offset(2, 0)
d64_data[prg_offset] = 0      # Next track (0 = end)
d64_data[prg_offset + 1] = 50  # Last byte used in sector (50 bytes)

# PRG header: Load address $0801 (BASIC start)
d64_data[prg_offset + 2] = 0x01
d64_data[prg_offset + 3] = 0x08

# BASIC program: 10 PRINT "HELLO WORLD": END
basic_program = [
    0x0C, 0x08,  # Next line pointer ($080C)
    0x0A, 0x00,  # Line number 10
    0x99,        # PRINT token
    0x20,        # Space
    0x22,        # Quote
] + [ord(c) for c in "HELLO WORLD"] + [
    0x22,        # Quote
    0x3A,        # Colon
    0x80,        # END token
    0x00,        # End of line
    0x00, 0x00   # End of program
]

for i, byte in enumerate(basic_program):
    d64_data[prg_offset + 4 + i] = byte

# Test PRG data #2: Assembly program (Track 3, Sector 0)
asm_offset = get_d64_offset(3, 0)
d64_data[asm_offset] = 0      # Next track (0 = end)
d64_data[asm_offset + 1] = 20  # Last byte used in sector

# PRG header: Load address $C000 (Assembly program)
d64_data[asm_offset + 2] = 0x00
d64_data[asm_offset + 3] = 0xC0

# Simple assembly code: LDA #$41; STA $0400; RTS
asm_program = [
    0xA9, 0x41,        # LDA #$41 (Load 'A')
    0x8D, 0x00, 0x04,  # STA $0400 (Store to screen)
    0xA9, 0x05,        # LDA #$05 (Color green)
    0x8D, 0x00, 0xD8,  # STA $D800 (Store to color RAM)
    0x60               # RTS (Return)
]

for i, byte in enumerate(asm_program):
    d64_data[asm_offset + 4 + i] = byte

# BAM entries: Mark used blocks
# Track 2, Sector 0 used (BASIC program)
bam_track2_offset = bam_offset + 4 + (2-1) * 4
d64_data[bam_track2_offset] = 20  # Free sectors (21-1)
d64_data[bam_track2_offset + 1] = 0xFE  # Sector 0 used (bit 0 clear)
d64_data[bam_track2_offset + 2] = 0xFF
d64_data[bam_track2_offset + 3] = 0xFF

# Track 3, Sector 0 used (ASM program)
bam_track3_offset = bam_offset + 4 + (3-1) * 4
d64_data[bam_track3_offset] = 20  # Free sectors (21-1)
d64_data[bam_track3_offset + 1] = 0xFE  # Sector 0 used (bit 0 clear)
d64_data[bam_track3_offset + 2] = 0xFF
d64_data[bam_track3_offset + 3] = 0xFF

# Track 18 used for directory
bam_track18_offset = bam_offset + 4 + (18-1) * 4
d64_data[bam_track18_offset] = 17  # Free sectors (19-2)
d64_data[bam_track18_offset + 1] = 0xFC  # Sectors 0,1 used
d64_data[bam_track18_offset + 2] = 0xFF
d64_data[bam_track18_offset + 3] = 0x07

# D64 dosyasını kaydet
with open('test.d64', 'wb') as f:
    f.write(d64_data)

print("Gelişmiş test.d64 dosyası oluşturuldu!")
print("İçerik:")
print("- HELLO WORLD (BASIC program)")
print("- ASM DEMO (Assembly program)")
print("- Doğru CBM DOS yapısı")
print("- BAM (Block Allocation Map) ile")
