from fractions import Fraction
V = range(-4, 5)
U = range(-6, 7)
pairs = [(v, u) for v in V for u in U]
assert len(pairs) == 117
for b in range(0, 4):
    n = sum(1 for v, u in pairs if abs(1 + v - u) <= b)
    print('band', b, 'hits', n, Fraction(n, 117), float(Fraction(n, 117)))
print('E[e]', Fraction(sum(1 + v - u for v, u in pairs), 117))
print('Var(V)', Fraction(sum(v*v for v in V), 9) - Fraction(sum(V), 9)**2, 'Var(U)', Fraction(sum(u*u for u in U), 13) - Fraction(sum(U), 13)**2)
