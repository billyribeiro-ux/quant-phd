"""Round 15: exact converse check of Theorem 1.5 on random finite pmfs (no sampling of utilities).
If F_X(t) > F_Y(t) at some support point t, the nondecreasing utility u = 1{x > t} gives
E u(X) = 1 - F_X(t) < 1 - F_Y(t) = E u(Y), so X does not dominate Y. Checked for every pair."""
import random
from fractions import Fraction

rng = random.Random(15)
S = [0, 1, 2, 3, 4]

def rand_pmf():
    w = [rng.randint(0, 6) for _ in S]
    if sum(w) == 0:
        w[0] = 1
    tot = sum(w)
    return [Fraction(x, tot) for x in w]

def cdf(p, t):
    return sum(pi for x, pi in zip(S, p) if x <= t)

pairs = 0
non_dominance = 0
witness_ok = 0
for _ in range(400):
    p, q = rand_pmf(), rand_pmf()
    pairs += 1
    fosd = all(cdf(p, t) <= cdf(q, t) for t in S)
    if fosd:
        continue
    non_dominance += 1
    bad = [t for t in S if cdf(p, t) > cdf(q, t)]
    t = bad[0]
    ex = sum(pi for x, pi in zip(S, p) if x > t)
    ey = sum(qi for x, qi in zip(S, q) if x > t)
    if ex < ey:
        witness_ok += 1
print(f"pairs {pairs}; pairs where F_X<=F_Y fails {non_dominance}; indicator witness refutes X>=Y in {witness_ok} of them")
