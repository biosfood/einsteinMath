from mathOperations import Term

def safeSimplify(parts):
    for index, part in enumerate(parts):
        if isinstance(part, Term):
            parts[index] = part.simplify()
    return parts

def safeDifferentiate(term, symbol):
    if isinstance(term, Term):
        return term.differentiate(symbol)
    return 0

def safeUse(parts, knowledge):
    return [term.use(knowledge) if isinstance(term, Term) else term for term in parts]

class d:
    def __init__(self, term):
        self.term = term

    def __truediv__(self, other):
        return self.term.differentiate(other.term)
