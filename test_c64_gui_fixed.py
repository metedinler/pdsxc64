# C64 GUI TEST - Düzeltilmiş Versiyon
from pdsxv12X import pdsXInterpreter

print('🚀 C64 GUI Test Başlatılıyor...')

# PDSX interpreter oluştur
pdsx = pdsXInterpreter()

# Test kodu
test_code = '''
# C64 GUI Initialize
C64_INIT

# C64 Graphics Test
C64_CLEAR
POKE 53280, 0
POKE 53281, 1
C64_PIXEL 100, 100, 2
C64_CHAR 10, 10, 65, 3

# GUI Window
WINDOW "C64 GUI Demo", 400, 300

# Print memory test
PRINT "VIC II Register: ", PEEK(53269)

# Test response
PRINT "✅ C64 GUI test tamamlandı!"
'''

try:
    print('📝 Test kodu yürütülüyor...')
    result = pdsx.execute_command(test_code)
    print('✅ C64 GUI test tamamlandı!')
    print(f'📊 Sonuç: {result}')
except Exception as e:
    print(f'❌ Test hatası: {e}')
    import traceback
    traceback.print_exc()
