#!/usr/bin/env python3
"""
İyileştirilmiş GUI Test
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_improved_ui():
    """İyileştirilmiş UI'yi test et"""
    print("🎨 Testing Improved GUI Design...")
    print("=" * 40)
    
    try:
        import pygubu
        import tkinter as tk
        
        # İyileştirilmiş UI dosyasını yükle
        ui_file = Path(__file__).parent / "gui_designs" / "d64_converter_improved.ui"
        
        if not ui_file.exists():
            print(f"❌ Improved UI file not found: {ui_file}")
            return
        
        print(f"✅ Loading improved UI: {ui_file}")
        
        # PyGubu builder
        builder = pygubu.Builder()
        builder.add_from_file(str(ui_file))
        
        # Root ve pencere
        root = tk.Tk()
        root.withdraw()
        
        main_window = builder.get_object('main_window', root)
        main_window.title("D64 Converter - Improved Design Test")
        
        # Widget'ları kontrol et
        widgets_to_test = [
            'open_file_btn', 'hybrid_analysis_btn', 'save_all_btn', 'settings_btn',
            'disassemble_btn', 'transpile_btn', 'file_tree', 'disassembly_output'
        ]
        
        print("\n🧩 Testing widgets:")
        for widget_id in widgets_to_test:
            try:
                widget = builder.get_object(widget_id)
                print(f"  ✅ {widget_id}: {type(widget).__name__}")
            except:
                print(f"  ❌ {widget_id}: Not found")
        
        # Pencereyi göster
        main_window.deiconify()
        
        # Test verisi ekle
        try:
            file_tree = builder.get_object('file_tree')
            test_files = [
                "📁 MYDISK.D64",
                "📄 GAME.PRG (BASIC) [$0801-$2000]",
                "📄 LOADER.PRG (ML) [$C000-$C500]", 
                "📄 SPRITES.PRG (DATA) [$3000-$3800]",
                "📄 MUSIC.SID (PLAYER) [$1000-$2000]",
                "📄 CHARSET.PRG (DATA) [$2800-$3000]"
            ]
            
            for file_entry in test_files:
                file_tree.insert('end', file_entry)
            
            print("✅ Test data added to file tree")
        except:
            print("⚠️ Could not add test data")
        
        # Test çıktısı ekle
        try:
            output_area = builder.get_object('disassembly_output')
            test_output = """
; D64 Converter - Improved GUI Test
; Professional C64 Decompiler v6.0
; Generated: 2025-07-27 14:30:00

; ====================================
; GAME.PRG - BASIC Program Analysis
; ====================================

*=$0801        ; BASIC Start Address

BASIC_START:
    .WORD $080B    ; Next line pointer
    .WORD $000A    ; Line number 10
    .BYTE $9E      ; SYS token
    .TEXT "2064"   ; SYS 2064
    .BYTE $00      ; End of line
    .WORD $0000    ; End of program

*=$0810        ; Machine Language Start

MAIN_PROGRAM:
    LDA #$00       ; Clear accumulator
    STA $D020      ; Set border color to black
    STA $D021      ; Set background color to black
    
    ; Initialize game variables
    LDX #$FF       ; Initialize stack pointer
    TXS
    
    ; Main game loop
GAME_LOOP:
    JSR $FFE4      ; Get key from keyboard
    BEQ GAME_LOOP  ; If no key, continue loop
    
    CMP #$20       ; Space key?
    BEQ FIRE_BUTTON
    
    CMP #$91       ; Cursor up?
    BEQ MOVE_UP
    
    JMP GAME_LOOP  ; Continue loop

FIRE_BUTTON:
    ; Handle fire button
    INC $D020      ; Flash border
    JMP GAME_LOOP

MOVE_UP:
    ; Handle move up
    DEC $0400      ; Move character on screen
    JMP GAME_LOOP

; End of disassembly
"""
            output_area.delete(1.0, 'end')
            output_area.insert(1.0, test_output)
            
            print("✅ Test output added")
        except:
            print("⚠️ Could not add test output")
        
        print("\n💡 Improved GUI Test Window Opened!")
        print("   • Modern dark theme applied")
        print("   • Professional button layout") 
        print("   • Better color scheme")
        print("   • Improved typography")
        print("   • Close window to exit")
        
        # 10 saniye sonra otomatik kapat
        root.after(10000, root.quit)
        root.mainloop()
        
        print("\n🎉 Improved GUI test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_ui()
