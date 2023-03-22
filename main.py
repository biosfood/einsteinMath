from symbol import *

def diagonal(elements):
    return [[element if i == j else 0 for j in range(len(elements))] for i, element in enumerate(elements)]


t = Symbol('t')
c = Symbol('c')
x = Vector('x')
g = Matrix('g')

xValue = [Symbol(name) for name in ['tau', 'r', 'phi', 'eta']]
gValue = diagonal([c**2, -1, -x[1]**2, -x[1]**2])

magnitude = g(x, x)
print(magnitude)
print(magnitude.withValues({x: xValue, g: gValue}).simplify())
