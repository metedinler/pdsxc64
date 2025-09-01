import readline

class PdsXException(Exception):
    pass

class ReplUtils:
    @staticmethod
    def enable_tab_completion(commands):
        readline.set_completer(lambda text, state: [cmd for cmd in commands if cmd.startswith(text.upper())][state] if state < len([cmd for cmd in commands if cmd.startswith(text.upper())]) else None)
        readline.parse_and_bind('tab: complete')