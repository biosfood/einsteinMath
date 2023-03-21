from enum import Enum
from mathOperations import *

class Symbol(Term):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def differentiate(self, symbol):
        if self == symbol:
            return 1
        return 0

greekLetters = [chr(i) for i in range(945, 970)]
index = 0

def getNextIndex():
    global index
    index += 1
    return greekLetters[index-1]

class IndexPosition(Enum):
    UP = 1
    DOWN = 0

class WithIndex(Term):
    def __init__(self, symbol, *indices, position = IndexPosition.UP):
        self.indices = indices
        self.symbol = symbol
        self.position = position

    def __str__(self):
        indicesString = "".join(self.indices)
        addition = f'[{indicesString}]' if self.position == IndexPosition.UP else f'{{{indicesString}}}'
        return str(self.symbol)+addition

class Vector(Symbol):
    def __init__(self, symbol, replacements=[0 for _ in range(4)]):
        super().__init__(symbol)
        self.replacements = replacements

    def __str__(self):
        return f'{super().__str__()}'

    def __getitem__(self, index):
        return self.replacements[index]

    def withIndex(self, index):
        return WithIndex(self, index)

class Matrix(Symbol):
    def __init__(self, symbol, replacements=[[0 for _ in range(4)] for _ in range(4)]):
        super().__init__(symbol)
        self.replacements = replacements

    def __str__(self):
        return f'{super().__str__()}'

    def __call__(self, x, y):
        a = getNextIndex()
        b = getNextIndex()
        return WithIndex(self, a, b, position=IndexPosition.DOWN) * x.withIndex(a) * y.withIndex(b)
