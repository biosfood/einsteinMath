from variable import Symbol, Vector, d, Matrix

def diagonal(elements):
    return [[element if i == j else 0 for j in range(len(elements))] for i, element in enumerate(elements)]

t = Symbol('t')
c = Symbol('c')
x = Vector(Symbol('x'), [Symbol(name) for name in ['tau', 'r', 'phi']])
g = Matrix(Symbol('g'), diagonal([c**2, -1, x[2]**2]))
print(g.replacements)
print(t, c, x, g)
