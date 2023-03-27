class Calculatable:
    def __add__(self, other):
        return Addition([self, other]).simplify()

    def __radd__(self, other):
        return Addition([self, other]).simplify()

    def __sub__(self, other):
        return Addition([self, Product([-1, other])]).simplify()

    def __rsub__(self, other):
        return Addition([other, Product([-1, self])]).simplify()

    def __truediv__(self, other):
        return Product([self, Exponentiation(other, -1)]).simplify()

    def __rtruediv__(self, other):
        return Product([other, Exponentiation(self, -1)]).simplify()

    def __mul__(self, other):
        return Product([self, other]).simplify()

    def __rmul__(self, other):
        return Product([self, other]).simplify()

    def __pow__(self, other):
        return Exponentiation(self, other).simplify()

    def __rpow__(self,other):
        return Exponentiation(other, self).simplify()

    def __neg__(self):
        return Product([-1, self]).simplify()

class Term(Calculatable):
    def __init__(self, knowledge = None):
        if knowledge == None:
            knowledge = {}
        self.knowledge = knowledge

    def simplify(self):
        return self

    def clone(self, knowledge):
        raise Exception("clone not implemented", knowledge)

    def use(self, values):
        return self.clone(knowledge={**self.knowledge, **values})

    def differentiate(self, _):
        return self

from safeOperations import *

class CommutableTerm(Term):
    symbol=''
    defaultValue=None

    def __init__(self, parts = [], knowledge = None):
        super().__init__(knowledge)
        self.parts = parts

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

    def clone(self, knowledge):
        return type(self)(safeUse(self.parts, knowledge), knowledge).simplify()

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

def testAny(array, function):
    for element in array:
        if function(element):
            return True
    return False

class Product(CommutableTerm):
    symbol = '*'
    defaultValue = 1

    def action(self, x,y): return x*y

    def differentiate(self, symbol):
        return Addition([Product([differentiatedPart.differentiate(symbol)] + [part for part in self.parts if part != differentiatedPart])
                         for differentiatedPart in self.parts if isinstance(differentiatedPart, Term)]).simplify()

    def simplify(self):
        from symbol import WithIndex, IndexPosition
        superResult = super().simplify()
        if type(superResult) != type(self):
            return superResult
        if 0 in superResult.parts:
            return 0
        lowerIndices = set()
        upperIndices = set()
        for part in self.parts:
            if isinstance(part, WithIndex) and part.symbol in part.knowledge:
                if part.position == IndexPosition.UP:
                    upperIndices.update(part.indices)
                elif part.position == IndexPosition.DOWN:
                    lowerIndices.update(part.indices)
        indicesToIterate = lowerIndices.intersection(lowerIndices)
        indexPossibilities = generateAllIndices(list(indicesToIterate), {})
        if len(indexPossibilities) == 1:
            return self
        result = sum([self.use({**self.knowledge, **option}) for option in indexPossibilities])
        return result

class Exponentiation(Term):
    def __init__(self, basis, exponent, knowledge = None):
        super().__init__(knowledge)
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

    def clone(self, knowledge):
        basis, exponent = safeUse([self.basis, self.exponent], knowledge)
        return Exponentiation(basis, exponent, knowledge)

class Differential(Term):
    def __init__(self, term, variable):
        self.term = term
        self.variable = variable

    def __str__(self):
        from symbol import Matrix, WithIndex
        if isinstance(self.term, WithIndex) and isinstance(self.term.symbol, Matrix) and isinstance(self.variable, WithIndex):
            matrixString = str(self.term)
            return f'{matrixString[:-1]},{"".join(self.variable.indices)}{matrixString[-1]}'
        return f'd({self.term})/d{self.variable}'
