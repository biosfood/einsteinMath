def safeSimplify(parts):
    for index, part in enumerate(parts):
        if isinstance(part, Term):
            parts[index] = part.simplify()
    return parts

def safeDifferentiate(term, symbol):
    if isinstance(term, Term):
        return term.differentiate(symbol)
    return 0

class d:
    def __init__(self, term):
        self.term = term

    def __truediv__(self, other):
        return self.term.differentiate(other.term)
