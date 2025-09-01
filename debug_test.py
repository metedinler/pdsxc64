from pdsxv12X import pdsXInterpreter

print('=== C64 GUI Debug Test ===')
pdsx = pdsXInterpreter()

# C64_INIT komutunu trace edelim
print('📍 C64_INIT komutu test ediliyor...')
result = pdsx.execute_command('C64_INIT')
print(f'📋 C64_INIT sonuç: {result}')

print('📍 WINDOW komutu test ediliyor...')
result = pdsx.execute_command('WINDOW "Debug", 300, 200')
print(f'📋 WINDOW sonuç: {result}')

print('=== Debug Test Tamamlandı ===')
