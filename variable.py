from enum import Enum

class Calculatable:
    def __add__(self, other):
        return Addition([self, other])

    def __radd__(self, other):
        return Addition([self, other])

    def __sub__(self, other):
        return Addition([self, Product([-1, other])])

    def __sub__(self, other):
        return Addition([other, Product([-1, self])])

    def __truediv__(self, other):
        return Product([self, Exponentiation(other, -1)])

    def __rtruediv__(self, other):
        return Product([other, Exponentiation(self, -1)])

    def __mul__(self, other):
        return Product([self, other])

    def __rmul__(self, other):
        return Product([self, other])

    def __pow__(self, other):
        return Exponentiation(self, other)

    def __rpow__(self,other):
        return Exponentiation(other, self)

def safeSimplify(parts):
    for index, part in enumerate(parts):
        if isinstance(part, Term):
            parts[index] = part.simplify()
    return parts

def safeDifferentiate(term, symbol):
    if isinstance(term, Term):
        return term.differentiate(symbol)
    return 0

class Term(Calculatable):
    def __init__(self):
        pass

    def derive(self, symbol):
        pass

    def simplify(self):
        return self

class CommutableTerm(Term):
    def __init__(self, parts = []):
        self.parts = parts
        self.simplify()

    def simplify(self):
        # simplify all parts
        self.parts = safeSimplify(self.parts)
        # flatten redundant layers
        additionalParts = sum([part.parts for part in self.parts if type(part) == type(self)], [])
        self.parts[:] = [part for part in self.parts if type(part) != type(self)] + additionalParts
        # simplify numerical values
        numericalValue = self.defaultValue
        for part in self.parts:
            if isinstance(part, (int, float)):
                numericalValue = self.action(numericalValue, part)
        self.parts[:] = [part for part in self.parts if not isinstance(part, (int, float))]
        if numericalValue != self.defaultValue:
             self.parts += [numericalValue]
        if len(self.parts) == 1:
            return self.parts[0]
        return self

    def __str__(self):
        return f'({self.symbol.join([str(part) for part in self.parts])})'


class Addition(CommutableTerm):
    symbol = '+'
    defaultValue = 0

    def action(self, x,y): return x+y

    def differentiate(self, symbol):
        return Addition([part.differentiate(symbol) for part in self.parts if isinstance(part, Term)])

class Product(CommutableTerm):
    symbol = '*'
    defaultValue = 1

    def action(self, x,y): return x*y

    def differentiate(self, symbol):
        return Addition([Product([differentiatedPart.differentiate(symbol)] + [part for part in self.parts if part != differentiatedPart]) 
                         for differentiatedPart in self.parts if isinstance(differentiatedPart, Term)])

    def simplify(self):
        superResult = super().simplify()
        if type(superResult) == type(self) and 0 in superResult.parts:
            return 0
        return superResult

class Exponentiation(Term):
    def __init__(self, basis, exponent):
        self.basis = basis
        self.exponent = exponent

    def __str__(self):
        return f'{self.basis}^{self.exponent}'

    def simplify(self):
        self.basis, self.exponent = safeSimplify([self.basis, self.exponent])
        if self.basis == 1:
            return 1
        if self.exponent == 1:
            return self.basis
        if isinstance(self.basis, (int, float)) and isinstance(self.exponent, (int, float)):
            return self.basis ** self.exponent
        if isinstance(self.basis, Exponentiation):
            return self.basis.basis ** (self.exponent * self.basis.exponent)
        return self

    def differentiate(self, symbol):
        return self.basis**(self.exponent-1)*self.exponent*safeDifferentiate(self.basis, symbol)

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

class d:
    def __init__(self, term):
        self.term = term

    def __truediv__(self, other):
        return self.term.differentiate(other.term)
