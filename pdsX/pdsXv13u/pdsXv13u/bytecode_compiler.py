class BytecodeCompiler:
    def __init__(self):
        self.bytecode = []

    def compile(self, code):
        lines = code.split("\n")
        for line in lines:
            tokens = line.split(maxsplit=1)
            opcode = tokens[0].upper()
            operands = tokens[1] if len(tokens) > 1 else ""
            self.bytecode.append({"opcode": opcode, "operands": operands})

    def save_bytecode(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.bytecode, f)

    def load_bytecode(self, filename):
        with open(filename, "rb") as f:
            self.bytecode = pickle.load(f)