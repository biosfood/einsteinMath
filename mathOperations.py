class Calculatable:
    def __add__(self, other):
        return Addition([self, other])

    def __radd__(self, other):
        return Addition([self, other])

    def __sub__(self, other):
        return Addition([self, Product([-1, other])])

    def __rsub__(self, other):
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

    def __neg__(self):
        return Product([-1, self])

class Term(Calculatable):
    def simplify(self):
        return self

    def withValues(self, values, modifyObject = True):
        _ = values
        _ = modifyObject
        return self

    def differentiate(self, _):
        return self

from safeOperations import *

class CommutableTerm(Term):
    symbol=''
    defaultValue=None
    action=lambda x,y,z: 0

    def __init__(self, parts = []):
        self.parts = parts
        self.simplify()
        self.values = {}

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

    def withValues(self, values, modifyObject = True):
        parts = safeApply(self.parts, values, modifyObject)
        if modifyObject:
            self.parts = parts
            self.values.update(values)
            return self
        return type(self)(parts)

class Addition(CommutableTerm):
    symbol = '+'
    defaultValue = 0

    def action(self, x,y): return x+y

    def differentiate(self, symbol):
        return Addition([part.differentiate(symbol) for part in self.parts if isinstance(part, Term)])

def generateAllIndices(remainingIndices, values):
    if len(remainingIndices) == 0:
        return [values]
    return sum([generateAllIndices(remainingIndices[1:], {**values, remainingIndices[0]: i}) for i in range(4)], [])

class Product(CommutableTerm):
    symbol = '*'
    defaultValue = 1

    def action(self, x,y): return x*y

    def differentiate(self, symbol):
        return Addition([Product([differentiatedPart.differentiate(symbol)] + [part for part in self.parts if part != differentiatedPart])
                         for differentiatedPart in self.parts if isinstance(differentiatedPart, Term)])

    def simplify(self):
        from symbol import WithIndex
        superResult = super().simplify()
        if type(superResult) != type(self):
            return superResult
        if 0 in superResult.parts:
            return 0
        indicesToIterate = set(())
        for part in self.parts:
            if isinstance(part, WithIndex) and part.values != None:
                abort = False
                for testIndex in part.indices:
                    if not part.indices[testIndex] in self.parts:
                        abort = True
                        break
                if abort: break
                indicesToIterate.update(part.indices.keys())
        indexPossibilities = generateAllIndices(list(indicesToIterate), {})
        if len(indexPossibilities) == 1:
            return self
        result = sum([self.withValues({**self.values, **option}, False) for option in indexPossibilities])
        return result

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

    def withValues(self, values, modifyObject = True):
        basis, exponent = safeApply([self.basis, self.exponent], values, modifyObject)
        if modifyObject:
            self.basis = basis
            self.exponent = exponent
            return self
        return Exponentiation(basis, exponent)
