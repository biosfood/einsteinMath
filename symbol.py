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

def copy(x):
    if isinstance(x, list):
        return list(x)
    if isinstance(x, dict):
        return dict(x)
    return x

class WithIndex(Term):
    def __init__(self, symbol, indices, position = IndexPosition.UP, values = None, indexValues = None):
        if indexValues == None:
            indexValues = {}
        self.indices = indices
        self.symbol = symbol
        self.position = position
        self.values = values
        self.indexValues = indexValues

    def __str__(self):
        indicesString = "".join(self.indices.keys())
        addition = f'[{indicesString}]' if self.position == IndexPosition.UP else f'{{{indicesString}}}'
        return str(self.symbol)+addition

    def withValues(self, values, modifyObject = True):
        if not modifyObject:
            return WithIndex(self.symbol, copy(self.indices), copy(self.position), copy(self.values), copy(self.indexValues)).withValues(values)
        if self.symbol in values:
            self.values = values[self.symbol]
        for index in self.indices.keys():
            if index in values:
                self.indexValues[index] = values[index]
        if len(self.indexValues) == len(self.indices) and self.values != None:
            currentValues = self.values
            for index in self.indices.keys():
                currentValues = currentValues[self.indexValues[index]]
            if isinstance(currentValues, Term):
                currentValues = currentValues.withValues(values, False)
            return currentValues
        return self

class Vector(Symbol):
    def __init__(self, symbol):
        super().__init__(symbol)

    def __str__(self):
        return f'{super().__str__()}'

    def __getitem__(self, index):
        return WithIndex(self, {'index': None}).withValues({'index': index})

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
        xWithIndex = x.withIndex({a: self})
        yWithIndex = y.withIndex({b: self})
        selfWithIndex = WithIndex(self, {a: xWithIndex, b: yWithIndex}, IndexPosition.DOWN)
        xWithIndex.indices[a] = selfWithIndex
        yWithIndex.indices[b] = selfWithIndex
        return selfWithIndex * xWithIndex * yWithIndex
