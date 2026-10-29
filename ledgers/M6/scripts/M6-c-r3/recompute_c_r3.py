"""Independent recomputation for L09-L12 numbers (does not import the lab twins)."""
from fractions import Fraction as F
from itertools import product

print("== L09 hitting time, N=8")
N = 8
paths = list(product((1, -1), repeat=N))
def first_hit(p):
    s = 0
    for k, x in enumerate(p, 1):
        s += x
        if s == 1:
            return k
    return None
for k in range(N + 1):
    cnt = sum(1 for p in paths if (first_hit(p) is not None and first_hit(p) <= k))
    print("k", k, "count", cnt, "prob", F(cnt, 256))
# lookahead rule: first i (0-based) with step i+1 == +1 is index i; event {rule<=k}
def look(p):
    for i, x in enumerate(p):
        if x == 1:
            return i
    return None
fails = []
for k in range(N + 1):
    ev = {}
    ok = True
    for p in paths:
        r = look(p)
        val = r is not None and r <= k
        key = p[:k]
        if ev.setdefault(key, val) != val:
            ok = False
    if not ok:
        fails.append(k)
print("lookahead failing k", fails)
print("P(tau=3)", F(sum(1 for p in paths if first_hit(p) == 3), 256), "P(tau<=2)", F(sum(1 for p in paths if first_hit(p) is not None and first_hit(p) <= 2), 256))
# misconception 3: tau = 2m+1 for m minus-steps then m+1 plus-steps
for m in range(0, 4):
    p = (-1,) * m + (1,) * (m + 1)
    print("m", m, "tau", first_hit(p + (1,) * 0), 2 * m + 1)

print("== L10 doubling")
def doubling_stats(K):
    m = (K + 1).bit_length() - 1
    prob_ruin = F(1, 2 ** m)
    win_wealth = K + 1
    ruin_wealth = K + 1 - 2 ** m
    e = (1 - prob_ruin) * win_wealth + prob_ruin * ruin_wealth
    return m, prob_ruin, win_wealth, ruin_wealth, e
for K in (1, 6, 10, 100, 1000):
    print(K, doubling_stats(K))
# unbounded: E[D_{tau ^ n}] = 0 and P(tau>n)=2^-n
for n in (1, 2, 3, 5, 10):
    pw = F(1 - F(1, 2 ** n))
    e = pw * 1 + F(1, 2 ** n) * (-(2 ** n - 1))
    print("n", n, "E_stopped", e, "P_tau_gt_n", F(1, 2 ** n))

print("== L11 Doob ratios exact")
for n in range(1, 13):
    sample = list(product((1, -1), repeat=n))
    w = F(1, 2 ** n)
    def sums(p):
        s = [0]
        for x in p:
            s.append(s[-1] + x)
        return s
    S = [sums(p) for p in sample]
    EZ = sum(w * abs(s[n]) for s in S)
    best = F(0)
    bestlam = None
    bestP = None
    grid = [F(j, 2) for j in range(1, 2 * (n + 1) + 1)]
    holds = True
    for lam in grid:
        hit = [s for s in S if max(abs(x) for x in s) >= lam]
        P = w * len(hit)
        Ehit = sum(w * abs(s[n]) for s in hit)
        if not (P <= EZ / lam and lam * P <= Ehit <= EZ):
            holds = False
        r = lam * P / EZ
        if r > best:
            best, bestlam, bestP = r, lam, P
    print("N", n, "holds", holds, "max_ratio", best, "float", round(float(best), 6), "lam", bestlam, "P", bestP, "EZ", EZ)

print("== L11 signed walk")
for n in (1, 2):
    sample = list(product((1, -1), repeat=n))
    w = F(1, 2 ** n)
    P = w * sum(1 for p in sample if max([0] + [sum(p[:k]) for k in range(1, n + 1)]) >= 1)
    E = sum(w * sum(p) for p in sample)
    print("N", n, "P", P, "E", E, "holds", P <= E)

print("== L12 dyadic")
for n in range(0, 11):
    cells = 2 ** n
    err = F(0)
    for j in range(cells):
        a, b = F(j, cells), F(j + 1, cells)
        c = (a + b) / 2
        err += ((b - c) ** 3 - (a - c) ** 3) / 3
    print("n", n, "E_err", err, "1/(12*4^n)", F(1, 12 * 4 ** n), err == F(1, 12 * 4 ** n))
print("E_Y2 exact:", sum(F(3 * 0 + 1, 3) for _ in range(1)))
