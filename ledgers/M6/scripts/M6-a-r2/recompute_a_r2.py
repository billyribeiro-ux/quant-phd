"""M6 slice a, round 2 (verifier-authored): independent recomputation of the numbers printed in L01-L04 prose.

Standard library only; run as: .venv/bin/python -I ledgers/M6/scripts/M6-a-r2/recompute_a_r2.py
"""

from decimal import Decimal as D
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60


def dyadic_lower_sum(n: int) -> D:
    """Integral of floor(2^n x^2)/2^n over [0,1] with the length measure: sum over k of (k/2^n) * length of level set."""
    total = D(0)
    big = 2**n
    for k in range(big):
        lo = D(k) / D(big)
        hi = D(k + 1) / D(big)
        a = lo.sqrt()
        b = min(hi.sqrt(), D(1))
        if b > a:
            total += lo * (b - a)
    return total


third = D(1) / D(3)
print("L03 Part B table (n, I_n, 1/3 - I_n, 2^-n) and bracket check")
for n in range(1, 11):
    v = dyadic_lower_sum(n)
    err = third - v
    bound = D(2) ** (-n)
    print(n, f"{float(v):.10f}", f"{float(err):.10f}", f"{float(bound):.10f}", 0 <= err <= bound)

print("L03 p.291: I_1 closed form (1/2)(1 - sqrt(1/2)) =", f"{float(D(1) / 2 * (1 - (D(1) / 2).sqrt())):.10f}")
print("L03 p.291: gap 1/3 - I_1 =", f"{float(third - dyadic_lower_sum(1)):.10f}")

print("L03 E3 terms, unrounded and rounded to 4 places")
terms = [
    D(1) / 4 * ((D(1) / 2).sqrt() - (D(1) / 4).sqrt()),
    D(1) / 2 * (D(3) / 4).sqrt() - D(1) / 2 * (D(1) / 2).sqrt(),
    D(3) / 4 * (D(1) - (D(3) / 4).sqrt()),
]
s = sum(terms, D(0))
for t in terms:
    print(f"  term {float(t):.7f} rounded {float(t):.4f}")
print(f"  sum unrounded {float(s):.7f}; sum of rounded {sum(round(float(t), 4) for t in terms):.4f}")
print("  I_2 from the dyadic sum", f"{float(dyadic_lower_sum(2)):.10f}")

print("L02 quiz: ordered disjoint pairs fail additivity for nu(A) = (|A|/6)^2 on six points")
pairs = 0
fail = 0
subsets = range(64)
for A in subsets:
    for B in subsets:
        if A & B:
            continue
        pairs += 1
        na, nb, nab = bin(A).count("1"), bin(B).count("1"), bin(A | B).count("1")
        if F(nab, 6) ** 2 != F(na, 6) ** 2 + F(nb, 6) ** 2:
            fail += 1
print("  ordered disjoint pairs", pairs, "fail", fail)

print("L02 fair die: P({1,2})+P({2,3}) and P({1,2,3}), P({2})")
print("  ", F(2, 6) + F(2, 6), F(3, 6), F(1, 6))
print("L02 biased weights sum to 1:", F(1, 2) + F(1, 4) + F(1, 8) + F(1, 16) + F(1, 32) + F(1, 32))
print("L02 odd outcomes {1,3,5} probability:", F(1, 2) + F(1, 8) + F(1, 32), "=", F(21, 32))

print("L04 partial sums of 1/(n+1), n = 1..N")
H = F(0)
partial = {}
for n in range(1, 101):
    H += F(1, n + 1)
    if n in (10, 100):
        partial[n] = H
print("  N=10:", f"{float(partial[10]):.6f}", " N=100:", f"{float(partial[100]):.6f}")

print("L04 Example 3.2 integral of f_n = 2 - 1/n (calculus), n=1..5 exact:")
for n in range(1, 6):
    val = F(1, n) + (F(2) - F(2, n))
    print("  n", n, val, val == F(2) - F(1, n))

print("L04 problem M3 solution: 2*(1/4) + int_{1/4}^1 x^(-1/2) dx =", F(1, 2) + (F(2) - F(1)))
