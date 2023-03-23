from enum import Enum
from mathOperations import *

class Symbol(Term):
    def __init__(self, name, knowledge=None):
        super().__init__(knowledge)
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def differentiate(self, symbol):
        if self == symbol:
            return 1
        return 0

    def clone(self, knowledge):
        if self in knowledge:
            return knowledge[self]
        return type(self)(self.name, knowledge)

greekLetters = [chr(i) for i in range(945, 970)]
index = 0

def getNextIndex():
    global index
    index += 1
    return greekLetters[index-1]

class IndexPosition(Enum):
    UP = 1
    DOWN = 0

def copy(x):
    if isinstance(x, list):
        return list(x)
    if isinstance(x, dict):
        return dict(x)
    return x

class WithIndex(Term):
    def __init__(self, symbol, indices, position = IndexPosition.UP, knowledge = None):
        super().__init__(knowledge)
        self.indices = indices
        self.symbol = symbol
        self.position = position

    def __str__(self):
        indicesString = "".join(self.indices)
        addition = f'[{indicesString}]' if self.position == IndexPosition.UP else f'{{{indicesString}}}'
        return str(self.symbol)+addition

    def clone(self, knowledge):
        if not self.symbol in knowledge:
            return WithIndex(copy(self.symbol), copy(self.indices), copy(self.position), knowledge)
        for index in self.indices:
            if not index in knowledge:
                return WithIndex(copy(self.symbol), copy(self.indices), copy(self.position), knowledge)
        currentValues = knowledge[self.symbol]
        for index in self.indices:
            currentValues = currentValues[knowledge[index]]
        if isinstance(currentValues, Term):
            currentValues = currentValues.use(knowledge)
        return currentValues

class Vector(Symbol):
    def __init__(self, symbol):
        super().__init__(symbol)

    def __str__(self):
        return f'{super().__str__()}'

    def __getitem__(self, index):
        return WithIndex(self, {'index': None}).use({'index': index})

    def withIndex(self, index):
        return WithIndex(self, index)

class Matrix(Symbol):
    def __init__(self, symbol):
        super().__init__(symbol)

    def __str__(self):
        return f'{super().__str__()}'

    def __call__(self, x, y):
        a = getNextIndex()
        b = getNextIndex()
        return x.withIndex({a}) * WithIndex(self, {a, b}, IndexPosition.DOWN) * y.withIndex({b})
