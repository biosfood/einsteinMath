class Calculatable:
    def __add__(self, other):
        return Addition([self, other])

    def __radd__(self, other):
        return Addition([self, other])

    def __mul__(self, other):
        return Product([self, other])

    def __rmul__(self, other):
        return Product([self, other])


class Term(Calculatable):
    def __init__(self):
        pass

    def derive(self, symbol):
        pass

    def simplify(self):
        pass

class CommutableTerm(Term):
    def __init__(self, parts = []):
        self.parts = parts

    def simplify(self):
        for (index, part) in enumerate(self.parts):
            if type(part) == Addition:
                del self.parts[index]
                self.parts.extend(part.parts)

    def __str__(self):
        return f'{self.symbol.join([str(part) for part in self.parts])}'


class Addition(CommutableTerm):
    symbol = '+'

class Product(CommutableTerm):
    symbol = '*'

class Symbol(Calculatable):
    def __init__(self, name, dimensions=1):
        self.name = name
        self.dimensions = dimensions

    def __str__(self):
        return f'{self.name}'
