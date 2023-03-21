from symbol import *

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

class Term(Calculatable):
    def simplify(self):
        return self

    def withValues(self, _):
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

    def withValues(self, values):
        self.parts = safeApply(self.parts, values)
        return self

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
        if type(superResult) != type(self):
            return superResult
        if 0 in superResult.parts:
            return 0
        #for index, part in enumerate(self.parts):
        #    if isinstance(part, WithIndex) and part.values != None:
        #        for otherPart in self.parts[index:]:
        #            if otherPart.
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

    def withValues(self, values):
        self.basis, self.exponent = safeApply([self.basis, self.exponent], values)
        return self
