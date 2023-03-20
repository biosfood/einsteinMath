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

def safeSimplify(parts):
    for index, part in enumerate(parts):
        if isinstance(part, Term):
            parts[index] = part.simplify()
    return parts

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
        return self

    def __str__(self):
        return f'({self.symbol.join([str(part) for part in self.parts])})'


class Addition(CommutableTerm):
    symbol = '+'
    defaultValue = 0

    def action(self, x,y): return x+y

class Product(CommutableTerm):
    symbol = '*'
    defaultValue = 1

    def action(self, x,y): return x*y

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
            return basis
        if isinstance(self.basis, (int, float)) and isinstance(self.exponent, (int, float)):
            return self.basis ** self.exponent
        return self

class Symbol(Term):
    def __init__(self, name, dimensions=1):
        self.name = name
        self.dimensions = dimensions

    def __str__(self):
        return f'{self.name}'
