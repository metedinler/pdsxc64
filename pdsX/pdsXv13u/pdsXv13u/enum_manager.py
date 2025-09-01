class EnumInstance:
    def __init__(self, values):
        self.values = values
        self.current_value = None

    def set_value(self, value):
        if value in self.values:
            self.current_value = value
        else:
            raise PdsXException(f"Geçersiz ENUM değeri: {value}")

    def get_value(self):
        return self.current_value

    def get_values(self):
        return list(self.values.keys())