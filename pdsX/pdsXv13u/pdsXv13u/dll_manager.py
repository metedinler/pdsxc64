class DllManager:
    def __init__(self):
        self.loaded_dlls = {}

    def load_dll(self, dll_name):
        dll = ctypes.WinDLL(dll_name)
        self.loaded_dlls[dll_name] = dll

    def call_function(self, dll_name, func_name, *args):
        dll = self.loaded_dlls.get(dll_name)
        if dll:
            func = getattr(dll, func_name)
            return func(*args)
        raise Exception(f"DLL not loaded: {dll_name}")

class ApiManager:
    def __init__(self):
        pass

    def call_api(self, url, params=None):
        response = requests.get(url, params=params)
        return response.json()