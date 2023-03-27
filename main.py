from symbol import *

def diagonal(elements):
    return [[element if i == j else 0 for j in range(len(elements))] for i, element in enumerate(elements)]


t = Symbol('t')
c = Symbol('c')
A = Vector('A', {t})
U = Vector('U', {t}, A)
x = Vector('x', {t}, U)
g = Matrix('g', {x})

xValue = [Symbol(name) for name in ['tau', 'r', 'phi', 'eta']]
gValue = diagonal([c**2, -1, -x[1]**2, -x[1]**2])

L = g(U, U)

rightSide = d(L)/d(x)
leftSide = d(d(L)/d(U))/d(t)

print(x[0].use({x: xValue}))
print(f'L = {str(L)}')
print('d/dx dL/dU = dL/dx')
print(f'{leftSide} = {rightSide}')
print(L.use({x: xValue, g: gValue}))
