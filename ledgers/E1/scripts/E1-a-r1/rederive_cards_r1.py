from fractions import Fraction as Fr
import itertools
ok = True
def qstar(p, c, k):
    return max(Fr(0), (p - c) / (2 * k))
def mc(q, c, k):
    return c + 2 * k * q
def profit(q, p, F, c, k):
    return p * q - (F + c * q + k * q * q)
# grid of rational parameters
vals = [Fr(0), Fr(1, 2), Fr(1), Fr(2), Fr(3), Fr(7, 3), Fr(10), Fr(100)]
n_cases = 0
for p, c, k, F in itertools.product([Fr(1, 2), Fr(1), Fr(2), Fr(10)], [Fr(0), Fr(1), Fr(2), Fr(3, 2)], [Fr(1, 2), Fr(1), Fr(3)], [Fr(0), Fr(12), Fr(100)]):
    n_cases += 1
    # L02 Prop 1.3 proof identity: pi(q) = pi0 - k (q - q0)^2 with pi0 = (p-c)^2/(4k) - F, for every rational q
    q0 = (p - c) / (2 * k); pi0 = (p - c) ** 2 / (4 * k) - F
    for q in [Fr(j, 7) for j in range(0, 60)]:
        if profit(q, p, F, c, k) != pi0 - k * (q - q0) ** 2:
            ok = False; print('pi identity fail', p, c, k, F, q)
    qs = qstar(p, c, k)
    # c018: q* is the unique maximiser on a fine rational grid
    grid = [Fr(j, 48) for j in range(0, 48 * 12)]
    best = max(profit(q, p, F, c, k) for q in grid)
    argmax = [q for q in grid if profit(q, p, F, c, k) == best]
    if p > c:
        # c161: MC(q*) = p and q* > 0
        if not (qs > 0 and mc(qs, c, k) == p):
            ok = False; print("c161 fail", p, c, k)
        if p > c and qs != (p - c) / (2 * k):
            ok = False
    if qs not in argmax and qs <= 8:
        ok = False; print("c018 grid fail", p, c, k, F, qs, argmax[:3])
    # c162: q(p) nondecreasing and 0 at p = c
    prices = [c + Fr(i, 4) for i in range(0, 20)]
    vals_q = [qstar(pp, c, k) for pp in prices]
    if any(vals_q[i] > vals_q[i + 1] for i in range(len(vals_q) - 1)):
        ok = False; print("c162 fail")
    if qstar(c, c, k) != 0:
        ok = False; print("c162 zero at c fail")
    # c163 / c030 with Setting a > bc, b>0, n>=1, k>0
for a, b, n, c, k in itertools.product([Fr(100), Fr(7), Fr(3, 2)], [Fr(2), Fr(1, 3), Fr(1)], [1, 2, 10], [Fr(0), Fr(2), Fr(1, 2)], [Fr(1), Fr(1, 2)]):
    if not (a > b * c):
        continue
    s = Fr(n) / (2 * k)
    pstar = (a + s * c) / (b + s)
    Q = s * (pstar - c)
    if not (Q == a - b * pstar and Q > 0 and pstar - c == (a - b * c) / (b + s) and pstar > c):
        ok = False; print("c163/c030 fail", a, b, n, c, k)
    # Z(p*) = 0 directly from the firm-level supply with the Setting
    Z = (a - b * pstar) - Fr(n) * qstar(pstar, c, k)
    if Z != 0:
        ok = False; print("Z fail", a, b, n, c, k)
print("cases", n_cases, "all ok", ok)
# Example 1.5 numbers
a, b, n, c, k = Fr(100), Fr(2), 10, Fr(2), Fr(1)
s = Fr(n) / (2 * k); p = (a + s * c) / (b + s)
print("Ex1.5 p*", p, "Q*", a - b * p, s * (p - c), "one firm", (p - c) / (2 * k))
