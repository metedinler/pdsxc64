from pdsxv12X import pdsXInterpreter

print('=== C64 GUI Hızlı Test ===')
pdsx = pdsXInterpreter()

# C64 Init test
result = pdsx.execute_command('C64_INIT')
print('C64_INIT çalıştı:', result)

# Window test
result = pdsx.execute_command('WINDOW "Test", 300, 200')
print('WINDOW çalıştı:', result)

# PEEK test
result = pdsx.execute_command('PRINT "PEEK Test:", PEEK(53269)')
print('PEEK test çalıştı:', result)

print('=== Test Tamamlandı ===')
