# D64 Converter - User Guide

## About the Program

D64 Converter is an advanced reverse engineering tool developed for Commodore 64 disk images (.d64) and program files (.prg). It's a modern disassembler that can convert 6502 Assembly code to multiple programming languages.

## Key Features

### 🔄 Multi-Format Support
- **Assembly (ASM)**: Traditional 6502 Assembly output
- **C Language**: Compilable C code with full function support
- **QBasic**: Microsoft QBasic compatible code
- **PDSX BASIC**: Line-numbered BASIC format
- **Commodore BASIC V2**: Authentic C64 BASIC syntax
- **Pseudo Code**: Readable pseudo code output

### 🎯 Advanced Code Generation
- **Real C Code**: Compilable, executable C programs
- **Register Emulation**: Complete 6502 register emulation
- **Memory Management**: 64KB memory array with full memory support
- **Stack Operations**: Proper stack push/pop functions
- **Flag Operations**: Zero, Negative, Carry flag operations
- **Helper Functions**: Utility functions and type definitions

### 🖥️ User Interface
- **Modern GUI**: Tkinter-based user-friendly interface
- **Drag & Drop**: File drag-and-drop support
- **Tabbed Interface**: Separate tab for each format
- **Per-Format Conversion**: Dedicated convert buttons for each format
- **Real-time Preview**: Instant code preview

### 📁 File Formats
- **D64**: Commodore 64 disk images
- **PRG**: Program files
- **T64**: Tape images (future version)

## Directory Structure

```
d64_converter/
├── main.py                     # Main program launcher
├── d64_converter.py            # GUI application
├── advanced_disassembler.py    # Advanced disassembler
├── improved_disassembler.py    # New code generation system
├── opcode_manager.py           # Opcode and translation manager
├── d64_reader.py               # D64 disk reader
├── disassembler.py             # Basic disassembler
├── sprite_converter.py         # Sprite converter
├── sid_converter.py            # SID music converter
├── c64_basic_parser.py         # BASIC parser
├── parser.py                   # General parser
├── c64_memory_map.json         # C64 memory map
├── memory_map.json             # General memory map
├── opcode_map.json             # Opcode translations
├── hex_opcode_map.json         # Hex opcode table
├── venv_asmto/                 # Virtual environment directory
├── logs/                       # Log files
├── asm_files/                  # Assembly outputs
├── c_files/                    # C code outputs
├── qbasic_files/               # QBasic outputs
├── pdsx_files/                 # PDSX BASIC outputs
├── pseudo_files/               # Pseudo code outputs
├── commodorebasicv2_files/     # Commodore BASIC outputs
├── prg_files/                  # PRG files
├── png_files/                  # PNG outputs
├── sid_files/                  # SID files
├── help/                       # Help files
│   ├── opcode.html
│   ├── opcode.json
│   ├── opcode.md
│   └── opcodeaciklama.md
├── d64converter.md             # Turkish documentation
└── README.md                   # This file is English documentation, translate from Turkish.
```

## Python Libraries Used

### Core Libraries
```python
import tkinter as tk              # GUI framework
import tkinter.ttk as ttk         # Modern widgets
import tkinterdnd2               # Drag & drop support
import PIL                       # Image processing
import numpy                     # Numerical operations
import json                      # JSON data handling
import subprocess                # Process management
import venv                      # Virtual environment
import argparse                  # Command line parsing
import logging                   # Logging system
import pathlib                   # Path operations
```

### Optional Libraries
```python
import py65                      # 6502 emulation (optional)
```

## Virtual Environment System

The program automatically creates and manages a virtual environment called `venv_asmto`:

```
venv_asmto/
├── Scripts/                     # Windows executables
│   ├── python.exe
│   ├── pip.exe
│   └── activate.bat
├── Lib/                         # Python libraries
└── pyvenv.cfg                   # Virtual environment configuration
```

## Command Line Usage

### Basic Commands

```bash
# Run in GUI mode (default)
python main.py

# Start GUI with specific file
python main.py --file game.prg

# Test mode - generate all formats
python main.py --test --file game.prg

# List supported formats
python main.py --list-formats

# Run with debug mode
python main.py --debug --file game.prg
```

### Argparse Parameters

#### Main Operation Modes
- `--gui`: Run in GUI mode (default)
- `--test`: Test mode - generate all formats
- `--no-gui`: Run without GUI

#### File Options
- `--file, -f`: File to process (D64, PRG, T64, etc.)
- `--format, -o`: Output format (asm, c, qbasic, pdsx, pseudo, commodorebasicv2)

#### System Options
- `--debug`: Debug mode - detailed logging
- `--log-level`: Log level (DEBUG, INFO, WARNING, ERROR)
- `--log-file`: Log file (default: logs/timestamp.log)

#### Information Options
- `--list-formats`: List supported formats
- `--version`: Version information

### Example Usage

```bash
# Simple GUI startup
python main.py

# Start GUI with file
python main.py --file "games/pacman.prg"

# Test mode - generate all formats
python main.py --test --file "games/pacman.prg"

# Generate only C output
python main.py --file "games/pacman.prg" --format c

# Debug mode with detailed log
python main.py --debug --file "games/pacman.prg"

# Run with custom log file
python main.py --log-file "my_conversion.log" --file "games/pacman.prg"
```

## New Code Generation System

### Improved Disassembler
The program uses a new `ImprovedDisassembler` class to generate much higher quality code:

#### C Code Features
- **Real C Syntax**: Compilable C code
- **Type Definitions**: Proper types like `uint8_t`, `uint16_t`
- **Register Emulation**: Complete 6502 register set
- **Memory Array**: 64KB memory emulation
- **Stack Operations**: Proper stack push/pop
- **Flag Functions**: Zero, Negative flag operations
- **Helper Functions**: Utility functions

#### Example C Output
```c
// C64 6502 Assembly to C Conversion
// Generated by D64 Converter

#include <stdio.h>
#include <stdint.h>

// 6502 Registers
uint8_t a = 0;    // Accumulator
uint8_t x = 0;    // X Register
uint8_t y = 0;    // Y Register
uint8_t sp = 0xFF; // Stack Pointer
uint8_t status = 0; // Status Register

// Memory array
uint8_t memory[65536];

int main() {
    // Initialize memory
    for(int i = 0; i < 65536; i++) memory[i] = 0;
    
    // Program starts here
    a = 10; set_zero_flag(a); set_negative_flag(a);
    memory[1024] = a;
    a = a | 201; set_zero_flag(a); set_negative_flag(a);
    
    return 0;
}

// Helper functions
void set_zero_flag(uint8_t val) {
    if(val == 0) status |= 0x02;
    else status &= ~0x02;
}
```

#### QBasic Output
```basic
REM C64 6502 Assembly to QBasic Conversion
REM Generated by D64 Converter

DIM A AS INTEGER
DIM X AS INTEGER
DIM Y AS INTEGER
DIM MEMORY(65535) AS INTEGER

A = 10
MEMORY(1024) = A
A = A OR 201
```

#### Commodore BASIC V2 Output
```basic
10 REM C64 6502 ASSEMBLY TO COMMODORE BASIC V2
20 REM GENERATED BY D64 CONVERTER
50 A=0:X=0:Y=0:SP=255:ST=0
250 A=10
260 M(1024)=A
280 A=A OR 201
```

## Module Descriptions

### Main Modules

#### `main.py`
- Main program launcher
- Virtual environment management
- Argument parsing
- Logging system setup
- Package installation

#### `d64_converter.py`
- GUI application
- Tkinter-based interface
- Drag & drop support
- Per-format conversion
- Real-time preview

#### `advanced_disassembler.py`
- Advanced disassembler
- Multi-format support
- Memory map integration
- py65 support (optional)

#### `improved_disassembler.py`
- New code generation system
- High-quality C code generation
- Proper syntax handling
- Format-specific optimization

#### `opcode_manager.py`
- Opcode table management
- JSON file loading
- Translation system
- Hex opcode mapping

### Helper Modules

#### `d64_reader.py`
- D64 disk image reading
- File extraction
- Directory parsing

#### `disassembler.py`
- Basic disassembler
- Simple opcode table
- Legacy support

#### `sprite_converter.py`
- Sprite conversion
- PNG output
- Graphics processing

#### `sid_converter.py`
- SID music conversion
- Audio processing

#### `c64_basic_parser.py`
- BASIC code parsing
- Tokenization
- Syntax analysis

## Installation and Startup

### Automatic Installation
```bash
# Run the program - automatic installation is performed
python main.py
```

### Manual Installation
```bash
# Create virtual environment
python -m venv venv_asmto

# Activate virtual environment (Windows)
venv_asmto\Scripts\activate

# Install required packages
pip install tkinterdnd2 pillow numpy py65

# Run the program
python main.py
```

## Logging System

The program uses a detailed logging system:

### Log Files
- `logs/d64_converter_YYYYMMDD_HHMMSS.log`: Main log
- `logs/system_info.json`: System information

### Log Levels
- `DEBUG`: Detailed debug information
- `INFO`: General information messages
- `WARNING`: Warning messages
- `ERROR`: Error messages

### Example Log Output
```
2025-07-16 02:00:49,985 - INFO - main:52 - Logging system started
2025-07-16 02:00:49,986 - INFO - main:53 - Log level: INFO
2025-07-16 02:00:50,612 - INFO - main:439 - D64 Converter starting...
2025-07-16 02:00:50,613 - INFO - main:440 - Arguments: {'gui': True, 'test': False}
```

## Output Formats

### Assembly (ASM)
```assembly
$0801: LDA #$0A
$0803: STA $0400
$0806: RTS
```

### C Language
```c
a = 10; set_zero_flag(a); set_negative_flag(a);
memory[1024] = a;
return; // Return from subroutine
```

### QBasic
```basic
A = 10
MEMORY(1024) = A
RETURN
```

### PDSX BASIC
```basic
100 A = 10
110 MEMORY(1024) = A
120 RETURN
```

### Commodore BASIC V2
```basic
100 A=10
110 M(1024)=A
120 RETURN
```

### Pseudo Code
```
load_accumulator(10)
store_accumulator_to(memory[1024])
return_from_subroutine()
```

## Troubleshooting

### Common Issues

#### PIL Import Error
```bash
# Solution: Reinstall Pillow
pip install --force-reinstall Pillow
```

#### Virtual Environment Error
```bash
# Solution: Delete and recreate virtual environment
rmdir /s venv_asmto
python main.py
```

#### GUI Not Opening
```bash
# Solution: Check Tkinter installation
python -c "import tkinter; print('Tkinter OK')"
```

## Contributing

### Development Environment
```bash
# Clone repository
git clone [repository-url]
cd d64_converter

# Virtual environment for development
python -m venv venv_dev
venv_dev\Scripts\activate

# Install development packages
pip install -e .
pip install pytest black flake8
```

### Testing
```bash
# Run all tests
python -m pytest

# Run specific test
python main.py --test --file test_files/sample.prg
```

## Version History

### v1.0.0
- First stable release
- Multi-format support
- Modern GUI
- Improved disassembler
- Proper C code generation

## License

This project is distributed under the MIT license.

## Contact

For questions and suggestions:
- GitHub Issues : metedinler
- Email: [zmetedinler@gmail.com]

---

*D64 Converter - Commodore 64 Assembly Reverse Engineering Tool*
*© 2025 - Modern 6502 Disassembler with Multi-Language Output*
