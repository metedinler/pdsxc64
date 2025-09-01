"""
py65 doğru kullanım test
"""
try:
    from py65.devices.mpu6502 import MPU
    from py65.memory import ObservableMemory
    from py65.disassembler import Disassembler as PY65Disassembler

    print("py65 version debug:")
    
    # py65 setup - doğru parametreler
    memory = ObservableMemory()
    mpu = MPU(memory)
    
    # Disassembler'ı farklı yöntemlerle oluşturmayı dene
    print("Disassembler oluşturuluyor...")
    
    try:
        # Method 1: Sadece mpu
        py65_disassembler = PY65Disassembler(mpu)
        print("Method 1: PY65Disassembler(mpu) - başarılı")
    except Exception as e:
        print(f"Method 1 hatası: {e}")
        try:
            # Method 2: mpu ve memory
            py65_disassembler = PY65Disassembler(mpu, memory)
            print("Method 2: PY65Disassembler(mpu, memory) - başarılı")
        except Exception as e2:
            print(f"Method 2 hatası: {e2}")
            
            # Method 3: Parametresiz
            try:
                py65_disassembler = PY65Disassembler()
                print("Method 3: PY65Disassembler() - başarılı")
            except Exception as e3:
                print(f"Method 3 hatası: {e3}")
                print("Hiçbir method çalışmadı!")
                exit()

    # Test verisi
    test_data = bytes([0x4C, 0xE1, 0xCC])
    start_address = 0xCC00

    # Memory'ye kodu yükle
    memory[start_address:start_address + len(test_data)] = test_data

    print(f"\nMemory yüklendi:")
    print(f"Memory[$CC00]: 0x{memory[start_address]:02X}")
    print(f"Memory[$CC01]: 0x{memory[start_address+1]:02X}")  
    print(f"Memory[$CC02]: 0x{memory[start_address+2]:02X}")

    # instruction_at test
    print(f"\ninstruction_at test:")
    try:
        result = py65_disassembler.instruction_at(start_address)
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        if isinstance(result, tuple) and len(result) >= 2:
            length, disasm_text = result[:2]
            print(f"$CC00: {disasm_text} (length: {length})")
        else:
            print(f"Unexpected result format: {result}")
            
    except Exception as e:
        print(f"instruction_at hatası: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"py65 import hatası: {e}")
except Exception as e:
    print(f"Genel hata: {e}")
    import traceback
    traceback.print_exc()
