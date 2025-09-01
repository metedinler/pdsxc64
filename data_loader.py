import os
import json

class DataLoader:
    """
    Generic JSON data loader. Use to load all JSON files from a given subdirectory
    into a dictionary of Python data structures.
    If a JSON file is missing, you can generate defaults or skip.
    """
    def __init__(self, base_path=None):
        # Base directory for data, defaults to this file's directory
        self.base_path = base_path or os.path.dirname(__file__)

    def load_directory(self, rel_dir):
        """
        Load all .json files under base_path/rel_dir
        Returns a dict mapping filename (without .json) to loaded JSON data.
        """
        data = {}
        dir_path = os.path.join(self.base_path, rel_dir)
        if not os.path.isdir(dir_path):
            print(f"Data directory not found: {dir_path}")
            return data

        for fname in sorted(os.listdir(dir_path)):
            if fname.lower().endswith('.json'):
                key = os.path.splitext(fname)[0]
                file_path = os.path.join(dir_path, fname)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data[key] = json.load(f)
                except Exception as e:
                    print(f"Failed to load {file_path}: {e}")
        return data

# Example usage:
# loader = DataLoader()
# c64_rom = loader.load_directory('c64_rom_data/memory_maps')
# opcodes = loader.load_directory('.')  # loads root-level JSON files
