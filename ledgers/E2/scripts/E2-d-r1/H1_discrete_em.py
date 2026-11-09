# H1: exact E[M] (largest of n uniform whole-cent noises on -a..a), the formula of L08 Proposition 2.2
# cross-checked against enumeration for small n, a; then the values the changed card E2-c105 and its neighbours use.
from fractions import Fraction
import itertools, math
def em_formula(n, a):
    total = Fraction(-a)
    for x in range(-a, a):
        total += 1 - Fraction(x + a + 1, 2 * a + 1) ** n
    return total
def em_enum(n, a):
    vals = range(-a, a + 1)
    tup = list(itertools.product(vals, repeat=n))
    return Fraction(sum(max(t) for t in tup), len(tup))
ok = all(em_formula(n, a) == em_enum(n, a) for n in range(1, 5) for a in range(0, 4))
print("formula == enumeration for n in 1..4, a in 0..3:", ok)
print("n=2 a=1 E[M] =", em_formula(2, 1), "=", float(em_formula(2, 1)))
print("n=3 a=1 E[M] =", em_formula(3, 1), "=", float(em_formula(3, 1)))
e = em_formula(5, 2000)
print("n=5 a=2000 E[M] =", e, "=", float(e))
print("numerator/denominator:", e.numerator, e.denominator)
print("E[M] to 8 dp:", f"{float(e):.8f}")
print("1333 - E[M] =", float(1333 - e), "rounds to", f"{float(1333 - e):.2f}")
print("1334 - E[M] =", float(1334 - e), "rounds to", f"{float(1334 - e):.8f}")
print("continuous 4000/3 =", float(Fraction(4000, 3)))
print("smallest whole c >= E[M] (n=5,a=2000):", math.ceil(e))
# c105 candidate back: a positive whole-cent shading does not always suffice (1333 fails) and E[M] for n=2,a=1 is 4/9
print("n=2 a=1: 1-cent shading minus E[M] =", float(1 - em_formula(2, 1)), "(positive)")
print("n=2 a=1: smallest whole c with c >= E[M]:", math.ceil(em_formula(2, 1)))
# expected profit per auction at c=1333 under Proposition 3.1 for n=5, a=2000
print("Prop 3.1 expected profit at c=1333:", Fraction(1333) - e, float(Fraction(1333) - e))
# the probability of a positive shading c with c - E[M] < 0 exists: any c in 1..1333
print("positive whole c with c < E[M] (n=5,a=2000): count =", 1333)
