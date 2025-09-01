import os
from data_loader import DataLoader

# Load memory maps and zero page maps
loader = DataLoader(os.path.dirname(__file__))
mem_maps = loader.load_directory('c64_rom_data/memory_maps')
zero_maps = loader.load_directory('c64_rom_data/zeropage')

# Combine address labels
ADDRESS_LABELS = {}
# memory_maps JSONs may include c64_memory_map, memory_areas
for key, val in mem_maps.get('c64_memory_map', {}).items():
    try:
        addr = int(key, 16)
        # val can be description or dict
        if isinstance(val, dict) and 'name' in val:
            label = val['name']
        else:
            label = val
        ADDRESS_LABELS[addr] = label
    except:
        continue
for fname, data in zero_maps.items():
    for key, label in data.items():
        try:
            addr = int(key, 16)
            # label dict or string
            if isinstance(label, dict):
                name = label.get('name', '')
            else:
                name = label
            ADDRESS_LABELS[addr] = name
        except:
            continue


def format_address(addr: int) -> str:
    """Return formatted address with label if available"""
    addr = int(addr)
    if addr in ADDRESS_LABELS:
        return f"{ADDRESS_LABELS[addr]}(${addr:04X})"
    return f"${addr:04X}"
