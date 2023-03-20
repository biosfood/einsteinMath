from variable import Symbol, Vector

t = Symbol('t')
x = Vector('x')
term = x**2 + 3/x**2
print(term)
print(term.differentiate(x))
