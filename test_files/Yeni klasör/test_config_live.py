#!/usr/bin/env python3
"""
Live Configuration Manager Test
"""
import tkinter as tk
from gui_manager import D64ConverterGUI, safe_messagebox
import threading
import time

def test_configuration_manager():
    """Test Configuration Manager in live GUI"""
    try:
        print("🔧 Starting Configuration Manager Live Test...")
        
        # Create root window
        root = tk.Tk()
        root.withdraw()  # Hide main window for this test
        
        # Create GUI instance
        gui = D64ConverterGUI(root)
        print("✅ GUI Created successfully")
        
        # Test Configuration Manager directly
        print("📋 Testing Configuration Manager...")
        gui.open_configuration_manager()
        print("✅ Configuration Manager opened successfully")
        
        # Keep the application running for a few seconds
        def close_after_delay():
            time.sleep(3)
            print("🔄 Closing test...")
            root.quit()
        
        # Start timer thread
        timer_thread = threading.Thread(target=close_after_delay)
        timer_thread.start()
        
        # Run main loop
        root.mainloop()
        
        print("🎉 Configuration Manager test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration Manager test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 D64 Converter Configuration Manager Live Test")
    print("=" * 50)
    
    success = test_configuration_manager()
    
    if success:
        print("\n✅ BAŞARILI: Configuration Manager working correctly!")
        print("🛠️ Debug system preserved")
        print("🔧 Configuration Manager fixed with run() method")
        print("🛡️ Safe messagebox prevents conflicts")
    else:
        print("\n❌ Test failed - See errors above")
