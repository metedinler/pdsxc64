from mpmath import mp, mpf
import numpy as np
from abc import ABC, abstractmethod
import struct
import sys

class PdsXException(Exception):
    pass

class DataType(ABC):
    def __init__(self, bit_depth, signed):
        self.bit_depth = bit_depth
        self.signed = signed
        self._validate()

    def _validate(self):
        if self.bit_depth not in [8, 12, 16, 24, 32, 48, 64, 128, 256, 512]:
            raise PdsXException(f"Geçersiz bit derinliği: {self.bit_depth}")
        self._set_bounds()

    @abstractmethod
    def _set_bounds(self):
        pass

    @abstractmethod
    def set_value(self, value):
        pass

    @abstractmethod
    def get_value(self):
        pass

class FloatType(DataType):
    def __init__(self, bit_depth, signed=True):
        super().__init__(bit_depth, signed)
        self.value = None
        mp.dps = bit_depth // 4  # Hassasiyet ayarı

    def _set_bounds(self):
        if self.bit_depth <= 64:
            self.min_val = float(f"-{2**(self.bit_depth-1)}") if self.signed else 0.0
            self.max_val = float(f"{2**(self.bit_depth-1)-1}") if self.signed else float(f"{2**self.bit_depth-1}")
        else:
            self.min_val = mpf(f"-{2**(self.bit_depth-1)}") if self.signed else mpf("0")
            self.max_val = mpf(f"{2**(self.bit_depth-1)-1}") if self.signed else mpf(f"{2**self.bit_depth-1}")

    def set_value(self, value):
        try:
            val = mpf(value) if self.bit_depth > 64 else float(value)
            if self.signed:
                if val < self.min_val or val > self.max_val:
                    raise PdsXException(f"Değer sınır dışında: {val}")
            else:
                if val < 0 or val > self.max_val:
                    raise PdsXException(f"Değer sınır dışında: {val}")
            self.value = val
        except (ValueError, TypeError):
            raise PdsXException(f"Geçersiz float değeri: {value}")

    def get_value(self):
        return self.value

class Scalar(FloatType):
    def __init__(self, bit_depth, signed=True):
        super().__init__(bit_depth, signed)

class Vector(FloatType):
    def __init__(self, bit_depth, signed=True, size=0):
        super().__init__(bit_depth, signed)
        self.size = size
        self.value = [mpf(0) if self.bit_depth > 64 else 0.0] * size if size else []

    def set_value(self, values):
        if not isinstance(values, (list, tuple)) or len(values) != self.size:
            raise PdsXException(f"Vektör boyutu uyumsuz: {len(values)} beklenen {self.size}")
        self.value = []
        for val in values:
            super().set_value(val)
            self.value.append(self.get_value())

    def get_value(self):
        return self.value

class Matrix(FloatType):
    def __init__(self, bit_depth, signed=True, rows=0, cols=0):
        super().__init__(bit_depth, signed)
        self.rows = rows
        self.cols = cols
        self.value = [[mpf(0) if self.bit_depth > 64 else 0.0 for _ in range(cols)] for _ in range(rows)] if rows and cols else []

    def set_value(self, values):
        if not isinstance(values, (list, tuple)) or len(values) != self.rows or any(len(row) != self.cols for row in values):
            raise PdsXException(f"Matris boyutu uyumsuz: {len(values)}x{len(values[0] if values else 0)} beklenen {self.rows}x{self.cols}")
        self.value = []
        for row in values:
            new_row = []
            for val in row:
                super().set_value(val)
                new_row.append(self.get_value())
            self.value.append(new_row)

    def get_value(self):
        return self.value

class Tensor(FloatType):
    def __init__(self, bit_depth, signed=True, shape=()):
        super().__init__(bit_depth, signed)
        self.shape = shape
        self.value = np.zeros(shape, dtype=object if self.bit_depth > 64 else np.float64) if shape else []

    def set_value(self, values):
        values = np.array(values, dtype=object if self.bit_depth > 64 else np.float64)
        if values.shape != self.shape:
            raise PdsXException(f"Tensor boyutu uyumsuz: {values.shape} beklenen {self.shape}")
        flat_values = values.flatten()
        for val in flat_values:
            super().set_value(val)
        self.value = values

    def get_value(self):
        return self.value.tolist()