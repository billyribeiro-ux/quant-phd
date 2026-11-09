import math, random
from fractions import Fraction
prizes = [5000, 10000, 20000]; probs = [0.25, 0.5, 0.25]
def ce(x, p, g):
    if g == 1: return math.exp(sum(pi*math.log(xi) for pi, xi in zip(p, x)))
    s = 1-g; return sum(pi*xi**s for pi, xi in zip(p, x))**(1/s)
for g in (0, 0.25, 0.5, 1, 2, 4):
    v = ce(prizes, probs, g); print(g, f"{v:.4f}", math.floor(v+0.5))
print("exact mean", sum(Fraction(q)*x for q, x in zip([Fraction(1,4),Fraction(1,2),Fraction(1,4)], prizes)))
print("harmonic", 1/sum(Fraction(q)/x for q, x in zip([Fraction(1,4),Fraction(1,2),Fraction(1,4)], prizes)), float(1/sum(Fraction(q)/x for q, x in zip([Fraction(1,4),Fraction(1,2),Fraction(1,4)], prizes))))
random.seed(1); worst = 0
for _ in range(20000):
    w = random.uniform(0.01, 1e4); i = random.uniform(-5, 5); L = random.uniform(-5, 5)
    lhs = (w**i)**L; rhs = w**(i*L)
    worst = max(worst, abs(lhs-rhs)/abs(rhs))
print("Prop 1.2 max rel err over 20000 random (w,iota,Lambda):", worst)
