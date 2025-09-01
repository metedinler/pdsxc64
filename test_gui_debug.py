"""
GUI Debug Test Script
Test GUI debug sistemini command line üzerinden
"""

import sys
import os

# GUI manager'ı import et
try:
    from gui_manager import gui_debug, debug_button, debug_label, debug_frame, debug_messagebox
    print("✅ GUI Debug system import successful")
    
    # Debug sistemi test et
    print("\n=== GUI Debug System Test ===")
    
    # Debug mode test
    print("1. Debug mode başlangıç durumu:", gui_debug.debug_mode)
    
    # Debug modunu aç
    gui_debug.enable_debug()
    
    # Test component oluşturma
    print("\n2. Test component simulations:")
    
    # Simulated component creation (GUI olmadan)
    code1 = gui_debug.get_component_code("BUTTON", "Test Button")
    print(f"   Created: {code1} for BUTTON 'Test Button'")
    
    code2 = gui_debug.get_component_code("FRAME", "Main Frame")  
    print(f"   Created: {code2} for FRAME 'Main Frame'")
    
    code3 = gui_debug.get_component_code("LABEL", "Header Label")
    print(f"   Created: {code3} for LABEL 'Header Label'")
    
    # Registry göster
    print("\n3. Component Registry:")
    gui_debug.show_registry()
    
    # Debug formatla test et
    print("\n4. Debug formatting test:")
    formatted_text = gui_debug.format_text_with_debug("BUTTON", "Save File")
    print(f"   Original: 'Save File' → Debug: '{formatted_text}'")
    
    print("\n✅ GUI Debug System Test tamamlandı!")
    print("🎯 Artık GUI'de debug kodları [G1], [G2], [G3]... şeklinde görünecek")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("GUI manager modülü bulunamadı")
    
except Exception as e:
    print(f"❌ Test error: {e}")
    import traceback
    print(traceback.format_exc())
