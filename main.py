from variable import Symbol

x = Symbol('x')
y = Symbol('y')
term = 3*x+2*y+3*x*y
print(term)
print(term.differentiate(x))
