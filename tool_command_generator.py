#!/usr/bin/env python3
"""
🛠️ Tool Command Generator
Template generator for C64 development tools

Creates command templates with variable substitution
for automated tool execution.
"""

import json
from pathlib import Path

class ToolCommandGenerator:
    """Generate command templates for C64 development tools"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.variables = {
            "%TOOL_PATH%": "Full path to the tool executable",
            "%YOL%": "Working directory path", 
            "%DOSYAADI%": "Input filename (source file)",
            "%CIKTI%": "Output filename (compiled/assembled file)",
            "%BASLANGIC%": "Start address (e.g., $0801)",
            "%FORMAT%": "Output format (prg, bin, etc.)",
            "%LISTING%": "Listing filename (.lst)",
            "%SYMBOLS%": "Symbol filename (.sym/.lbl)",
            "%MODULE%": "Python module name",
            "%OPTIONS%": "Additional command line options"
        }
    
    def _load_templates(self):
        """Load predefined command templates"""
        return {
            "assemblers": {
                "64tass": {
                    "basic": "%TOOL_PATH% %DOSYAADI% -o %CIKTI%",
                    "with_listing": "%TOOL_PATH% %DOSYAADI% -o %CIKTI% --list=%LISTING%",
                    "with_labels": "%TOOL_PATH% %DOSYAADI% -o %CIKTI% --labels=%SYMBOLS%",
                    "full_featured": "%TOOL_PATH% --verbose %DOSYAADI% -o %CIKTI% --list=%LISTING% --labels=%SYMBOLS%",
                    "cross_reference": "%TOOL_PATH% %DOSYAADI% -o %CIKTI% --list=%LISTING% --labels=%SYMBOLS% --vice-labels",
                    "multiple_files": "%TOOL_PATH% %DOSYAADI% -I %YOL% -o %CIKTI%"
                },
                "acme": {
                    "basic": "%TOOL_PATH% %DOSYAADI%",
                    "with_output": "%TOOL_PATH% --outfile %CIKTI% %DOSYAADI%",
                    "cbm_format": "%TOOL_PATH% --format cbm %DOSYAADI%",
                    "with_listing": "%TOOL_PATH% --outfile %CIKTI% --report %LISTING% %DOSYAADI%",
                    "with_symbols": "%TOOL_PATH% --outfile %CIKTI% --labeldump %SYMBOLS% %DOSYAADI%",
                    "full_featured": "%TOOL_PATH% --format cbm --outfile %CIKTI% --report %LISTING% --labeldump %SYMBOLS% %DOSYAADI%"
                },
                "dasm": {
                    "basic": "%TOOL_PATH% %DOSYAADI% -o%CIKTI%",
                    "with_listing": "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -l%LISTING%",
                    "with_symbols": "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -s%SYMBOLS%",
                    "full_featured": "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -l%LISTING% -s%SYMBOLS%",
                    "verbose": "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -v3",
                    "format_1": "%TOOL_PATH% %DOSYAADI% -o%CIKTI% -f1"
                },
                "kickass": {
                    "basic": "java -jar %TOOL_PATH% %DOSYAADI%",
                    "with_output": "java -jar %TOOL_PATH% -o %CIKTI% %DOSYAADI%",
                    "with_symbols": "java -jar %TOOL_PATH% -symbolfile -vicesymbols %DOSYAADI%",
                    "with_listing": "java -jar %TOOL_PATH% -showmem %DOSYAADI%",
                    "full_featured": "java -jar %TOOL_PATH% -o %CIKTI% -symbolfile -vicesymbols -showmem %DOSYAADI%",
                    "with_lib": "java -jar %TOOL_PATH% -libdir %YOL%/lib %DOSYAADI%"
                },
                "ca65": {
                    "basic": "%TOOL_PATH% %DOSYAADI%",
                    "with_output": "%TOOL_PATH% -o %CIKTI% %DOSYAADI%",
                    "with_listing": "%TOOL_PATH% -l %LISTING% %DOSYAADI%",
                    "c64_target": "%TOOL_PATH% -t c64 %DOSYAADI%",
                    "with_debug": "%TOOL_PATH% -g -o %CIKTI% %DOSYAADI%",
                    "full_featured": "%TOOL_PATH% -t c64 -g -l %LISTING% -o %CIKTI% %DOSYAADI%"
                },
                "xa": {
                    "basic": "%TOOL_PATH% %DOSYAADI%",
                    "with_output": "%TOOL_PATH% -o %CIKTI% %DOSYAADI%",
                    "with_listing": "%TOOL_PATH% -l %LISTING% %DOSYAADI%",
                    "c64_compatible": "%TOOL_PATH% -XC %DOSYAADI%",
                    "full_featured": "%TOOL_PATH% -XC -o %CIKTI% -l %LISTING% %DOSYAADI%"
                }
            },
            "compilers": {
                "cc65": {
                    "basic": "%TOOL_PATH% -t c64 %DOSYAADI%",
                    "optimized": "%TOOL_PATH% -t c64 -O %DOSYAADI%",
                    "with_output": "%TOOL_PATH% -t c64 -o %CIKTI% %DOSYAADI%",
                    "with_listing": "%TOOL_PATH% -t c64 -l %LISTING% %DOSYAADI%",
                    "debug": "%TOOL_PATH% -t c64 -g %DOSYAADI%",
                    "full_featured": "%TOOL_PATH% -t c64 -O -o %CIKTI% -l %LISTING% %DOSYAADI%"
                },
                "oscar64": {
                    "basic": "%TOOL_PATH% %DOSYAADI%",
                    "with_output": "%TOOL_PATH% %DOSYAADI% -o %CIKTI%",
                    "c64_target": "%TOOL_PATH% -tm=c64 %DOSYAADI%",
                    "optimized": "%TOOL_PATH% -O2 %DOSYAADI% -o %CIKTI%",
                    "with_listing": "%TOOL_PATH% %DOSYAADI% -o %CIKTI% -l",
                    "full_featured": "%TOOL_PATH% -tm=c64 -O2 %DOSYAADI% -o %CIKTI% -l"
                }
            },
            "interpreters": {
                "python": {
                    "basic": "%TOOL_PATH% %DOSYAADI%",
                    "with_module": "%TOOL_PATH% -m %MODULE% %DOSYAADI%",
                    "interactive": "%TOOL_PATH% -i %DOSYAADI%",
                    "optimized": "%TOOL_PATH% -O %DOSYAADI%",
                    "with_options": "%TOOL_PATH% %OPTIONS% %DOSYAADI%"
                }
            },
            "utilities": {
                "c1541": {
                    "format_disk": "%TOOL_PATH% -format diskname,id d64 %CIKTI%",
                    "attach_disk": "%TOOL_PATH% -attach %DOSYAADI%",
                    "write_file": "%TOOL_PATH% -attach %DOSYAADI% -write %CIKTI% filename",
                    "read_file": "%TOOL_PATH% -attach %DOSYAADI% -read filename %CIKTI%",
                    "list_files": "%TOOL_PATH% -attach %DOSYAADI% -list"
                },
                "petcat": {
                    "tokenize": "%TOOL_PATH% -w2 -o %CIKTI% -- %DOSYAADI%",
                    "detokenize": "%TOOL_PATH% -2 -o %CIKTI% -- %DOSYAADI%",
                    "list_program": "%TOOL_PATH% -2 -- %DOSYAADI%"
                }
            }
        }
    
    def get_templates_for_tool(self, tool_name):
        """Get all templates for a specific tool"""
        for category, tools in self.templates.items():
            if tool_name in tools:
                return tools[tool_name]
        return {}
    
    def generate_command(self, tool_name, template_name, variables):
        """Generate a command with variable substitution"""
        templates = self.get_templates_for_tool(tool_name)
        if template_name not in templates:
            return None
        
        command = templates[template_name]
        
        # Substitute variables
        for var, value in variables.items():
            if var.startswith('%') and var.endswith('%'):
                command = command.replace(var, str(value))
        
        return command
    
    def list_tools(self):
        """List all available tools and their templates"""
        result = {}
        for category, tools in self.templates.items():
            result[category] = {}
            for tool_name, templates in tools.items():
                result[category][tool_name] = list(templates.keys())
        return result
    
    def save_templates(self, filename):
        """Save templates to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "templates": self.templates,
                "variables": self.variables
            }, f, indent=2, ensure_ascii=False)
    
    def create_batch_script(self, tool_name, template_name, output_file="run_tool.bat"):
        """Create a Windows batch script for the command"""
        templates = self.get_templates_for_tool(tool_name)
        if template_name not in templates:
            return False
        
        template = templates[template_name]
        
        # Create batch script with variable prompts
        batch_content = f"""@echo off
REM Auto-generated batch script for {tool_name}
REM Template: {template_name}

echo === {tool_name.upper()} EXECUTION SCRIPT ===
echo.

REM Set variables (modify these as needed)
set TOOL_PATH=C:\\Tools\\{tool_name}\\{tool_name}.exe
set YOL=%CD%
set DOSYAADI=input.asm
set CIKTI=output.prg
set BASLANGIC=$0801
set FORMAT=prg
set LISTING=output.lst
set SYMBOLS=output.lbl

echo Tool Path: %TOOL_PATH%
echo Working Directory: %YOL%
echo Input File: %DOSYAADI%
echo Output File: %CIKTI%
echo.

REM Check if tool exists
if not exist "%TOOL_PATH%" (
    echo ERROR: Tool not found at %TOOL_PATH%
    echo Please modify TOOL_PATH variable in this script
    pause
    exit /b 1
)

REM Check if input file exists
if not exist "%DOSYAADI%" (
    echo ERROR: Input file not found: %DOSYAADI%
    echo Please ensure input file exists or modify DOSYAADI variable
    pause
    exit /b 1
)

echo Executing command...
echo.

REM Execute the command
{template}

echo.
echo Return code: %ERRORLEVEL%

if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Command completed successfully
    if exist "%CIKTI%" (
        echo Output file created: %CIKTI%
    )
) else (
    echo ERROR: Command failed with return code %ERRORLEVEL%
)

pause
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)
            return True
        except Exception:
            return False

# Example usage and testing
if __name__ == "__main__":
    generator = ToolCommandGenerator()
    
    # List all available tools
    print("🛠️ Available Tools and Templates:")
    print("=" * 50)
    
    tools_list = generator.list_tools()
    for category, tools in tools_list.items():
        print(f"\n📂 {category.upper()}:")
        for tool_name, templates in tools.items():
            print(f"  🔧 {tool_name}:")
            for template in templates:
                print(f"    • {template}")
    
    # Example command generation
    print("\n🚀 Example Command Generation:")
    print("=" * 50)
    
    variables = {
        "%TOOL_PATH%": "C:\\Tools\\64tass\\64tass.exe",
        "%YOL%": "C:\\C64Projects\\MyProject",
        "%DOSYAADI%": "main.asm", 
        "%CIKTI%": "main.prg",
        "%LISTING%": "main.lst",
        "%SYMBOLS%": "main.lbl"
    }
    
    command = generator.generate_command("64tass", "full_featured", variables)
    print(f"Generated command: {command}")
    
    # Save templates
    generator.save_templates("tool_templates.json")
    print(f"\n💾 Templates saved to: tool_templates.json")
    
    # Create batch script
    if generator.create_batch_script("64tass", "full_featured", "test_64tass.bat"):
        print(f"📄 Batch script created: test_64tass.bat")
