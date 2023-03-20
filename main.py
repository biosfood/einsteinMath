from variable import Symbol

x = Symbol('x')
y = Symbol('y')
term = x**2 + 3/x**2
print(term)
print(term.differentiate(x))
