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

class WithIndex():
    def __init__(self, *indices, position = IndexPosition.UP):
        self.indices = indices
        self.position = position

    def __str__(self):
        indicesString = "".join(self.indices)
        return f'[{indicesString}]' if self.position == IndexPosition.UP else f'{{{indicesString}}}'

class Vector(WithIndex):
    def __init__(self, symbol, replacements=[0 for _ in range(4)], index = getNextIndex()):
        self.symbol = symbol
        self.replacements = replacements
        super().__init__(index)

    def __str__(self):
        return f'{self.symbol.name}{super().__str__()}'

    def __getitem__(self, index):
        return self.replacements[index]

class Matrix(WithIndex):
    def __init__(self, symbol, replacements=[[0 for _ in range(4)] for _ in range(4)], indices = [getNextIndex() for _ in range(2)]):
        self.symbol = symbol
        self.replacements = replacements
        super().__init__(*indices, position = IndexPosition.DOWN)

    def __str__(self):
        return f'{self.symbol.name}{super().__str__()}'
