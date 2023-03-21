from variable import Symbol, Vector, d

t = Symbol('t')
x = Vector('x')
term = x**2 + 3/x**2
print(term)
print(d(term)/d(x))
