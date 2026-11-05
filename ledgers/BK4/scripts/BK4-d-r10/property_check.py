"""Randomised and exhaustive checks of the T-graded propositions that cards state, from their definitions.

Each block re-implements the definition from the lesson text. Prints PASS/FAIL per block with the number of cases.
Usage: python -I property_check.py
"""
import itertools
import math
import random
from fractions import Fraction as F

rng = random.Random(12345)
results: list[tuple[str, bool, int]] = []


def block(name: str, cases: int, ok: bool) -> None:
    results.append((name, ok, cases))


# ---- L01 Prop 2.2 / 2.3 / 2.4 / Remark 2.5 on random days (definitions: running sums, Need, Debit)
bad = 0
for _ in range(3000):
    banks = 3
    m = rng.randint(1, 8)
    pays = []
    for _ in range(m):
        s, r = rng.sample(range(banks), 2)
        pays.append((s, r, rng.randint(1, 50)))

    def S(i: int, k: int) -> int:
        tot = 0
        for snd, rcv, a in pays[:k]:
            if rcv == i:
                tot += a
            if snd == i:
                tot -= a
        return tot

    for i in range(banks):
        need_def = min(o for o in range(0, 10**4) if all(o + S(i, k) >= 0 for k in range(m + 1)))
        need_prop = max(0, -min(S(i, k) for k in range(m + 1)))
        net = S(i, m)
        debit = max(0, -net)
        if need_def != need_prop or need_prop < debit:
            bad += 1
    if sum(S(i, m) for i in range(banks)) != 0:
        bad += 1
block("L01 Prop 2.2 (need = running minimum), Prop 2.3 (nets sum 0), Prop 2.4 (need >= debit)", 3000, bad == 0)

# ---- L01 Remark 2.5: net debit independent of order; P2 iff (need = debit iff mu>=0 or S_m = mu)
bad = 0
for _ in range(3000):
    m = rng.randint(1, 7)
    seq = [rng.randint(-20, 20) for _ in range(m)]
    perm = seq[:]
    rng.shuffle(perm)

    def run(xs: list[int]) -> list[int]:
        acc, out = 0, [0]
        for x in xs:
            acc += x
            out.append(acc)
        return out

    r1, r2 = run(seq), run(perm)
    if max(0, -r1[-1]) != max(0, -r2[-1]):
        bad += 1
    need1 = max(0, -min(r1))
    debit1 = max(0, -r1[-1])
    mu = min(r1)
    iff_claim = (mu >= 0 or r1[-1] == mu)
    if (need1 == debit1) != iff_claim:
        bad += 1
block("L01 Remark 2.5 (net debit order-free) and Problem P2 (need = debit iff mu >= 0 or S_m = mu)", 3000, bad == 0)

# ---- L02 Prop 2.2(a)-(d), Prop 2.3, R1, P3 on random trade sets
bad = 0
for _ in range(3000):
    members = rng.randint(2, 5)
    q = rng.randint(1, 8)
    trades = []
    for _ in range(q):
        p_, r_ = rng.sample(range(members), 2)
        trades.append((p_, r_, rng.randint(1, 100)))
    G = sum(a for _, _, a in trades)
    rec = [sum(a for _, r, a in trades if r == i) for i in range(members)]
    pay = [sum(a for p, _, a in trades if p == i) for i in range(members)]
    n = [rec[i] - pay[i] for i in range(members)]
    A = sum(max(0, x) for x in n)
    if sum(rec) != G or sum(pay) != G or sum(n) != 0:
        bad += 1
    if sum(max(0, -x) for x in n) != A or not (0 <= A <= G):
        bad += 1
    A_eq_G = (A == G)
    cond = all(rec[i] == 0 or pay[i] == 0 for i in range(members))
    if A_eq_G != cond:
        bad += 1
    if G > 0:
        bps = (10000 * (G - A)) // G
        if not (0 <= bps <= 10000) or (bps == 10000) != (A == 0):
            bad += 1
block("L02 Prop 2.2(a)-(d), Prop 2.3 iff, R1 range and equality at 10000 iff A=0", 3000, bad == 0)

# P3 cycles
bad = 0
for k in range(2, 8):
    a = rng.randint(1, 1000)
    trades = [(i, (i + 1) % k, a) for i in range(k)]
    G = k * a
    rec = [a] * k
    pay = [a] * k
    n = [rec[i] - pay[i] for i in range(k)]
    A = sum(max(0, x) for x in n)
    if A != 0 or (10000 * (G - A)) // G != 10000:
        bad += 1
block("L02 P3 complete cycle: A = 0 and reduction 10000 bps", 6, bad == 0)

# ---- L03 Def 1.1, Prop 1.2, Prop 1.3 on random inputs
bad = 0
cases = 0
for _ in range(4000):
    cases += 1
    IM = rng.randint(0, 500)
    DFd = rng.randint(0, 300)
    K = rng.randint(0, 300)
    surv = {i: rng.randint(0, 200) for i in rng.sample(range(10, 20), rng.randint(1, 4))}
    L = rng.randint(0, 1500)
    a1 = min(L, IM)
    a2 = min(L - a1, DFd)
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv.values())
    if Z >= D:
        pays = dict(surv)
        u = Z - D
    else:
        assert D > 0
        pays = {i: Z * v // D for i, v in surv.items()}
        ell = Z - sum(pays.values())
        npos = sum(1 for v in surv.values() if v > 0)
        if not (0 <= ell <= npos - 1):
            bad += 1
        for i in sorted(surv):
            if ell == 0:
                break
            if surv[i] > 0:
                pays[i] += 1
                ell -= 1
        if ell != 0:
            bad += 1
        u = 0
        for i in surv:
            if pays[i] > surv[i]:
                bad += 1
    if a1 + a2 + a3 + sum(pays.values()) + u != L:
        bad += 1
    if a2 > 0 and a1 != IM:
        bad += 1
    if a3 > 0 and a2 != DFd:
        bad += 1
    if Z > 0 and a3 != K:
        bad += 1
block("L03 Def 1.1 conservation, Prop 1.2, Prop 1.3 bounds, Remark 1.4 layer waits", cases, bad == 0)

# ---- L03 Prop 2.3 (sized margin = L_(k)) and Cor 2.4 on random scenario sets
bad = 0
cases = 0
for _ in range(2000):
    S = rng.randint(1, 30)
    losses = [rng.randint(0, 100) for _ in range(S)]
    srt = sorted(losses)
    t_prev = None
    prevM = None
    for t in sorted(rng.sample(range(1, 10001), 3)):
        cases += 1
        k = math.ceil(F(t * S, 10000))
        if not (1 <= k <= S):
            bad += 1
        M = srt[k - 1]
        c = lambda mm: sum(1 for x in losses if x <= mm)  # noqa: E731
        cov = lambda mm: (10000 * c(mm)) // S  # noqa: E731
        brute = next(mm for mm in range(0, 101) if cov(mm) >= t)
        if brute != M:
            bad += 1
        for mm in range(0, 101):
            if (cov(mm) >= t) != (mm >= M):
                bad += 1
                break
        if prevM is not None and M < prevM:
            bad += 1
        prevM = M
block("L03 Prop 2.3 (smallest margin = L_(k), iff cover) and Cor 2.4 (monotone in t)", cases, bad == 0)

# ---- L04 Prop 2.2, 2.4, 2.5, 2.6, Prop 2.7 with exact fractions on random grids
bad = 0
cases = 0
for _ in range(1500):
    rho = F(rng.randint(1, 60), rng.randint(1, 60))
    xs = sorted({F(rng.randint(0, 99), 100) for _ in range(4)})
    xs = [x for x in xs if x <= rho and x < 1]
    th = {x: (rho - x) / (1 - x) for x in xs}
    for x in xs:
        cases += 1
        if th[x] - 1 != (rho - 1) / (1 - x):
            bad += 1
        if (th[x] < 1) != (rho < 1) or (th[x] == 1) != (rho == 1):
            bad += 1
        if rho <= 1 and th[x] > rho:
            bad += 1
        if rho >= 1 and th[x] < rho:
            bad += 1
        if th[x] - rho != x * (rho - 1) / (1 - x):
            bad += 1
    for x, y in itertools.permutations(xs, 2):
        if x < y:
            cases += 1
            lhs = th[y] - th[x]
            rhs = (y - x) * (rho - 1) / ((1 - x) * (1 - y))
            if lhs != rhs:
                bad += 1
            if (lhs > 0) != (rho > 1) and rho != 1:
                bad += 1
for _ in range(20000):
    cases += 1
    y = F(rng.randint(0, 10**6), rng.randint(1, 10**3))
    fl = math.floor(y)
    if (fl >= 10000) != (y >= 10000):
        bad += 1
block("L04 Prop 2.2, 2.4, 2.5, 2.6 and Prop 2.7 floor threshold (exact)", cases, bad == 0)

# Remark 4.1: measured coverage >= 1 iff rho(1-h) >= 1; threshold 20/19 for h=1/20
bad = 0
for _ in range(2000):
    h = F(rng.randint(0, 99), 100)
    rho = F(rng.randint(1, 300), 100)
    eff = rho * (1 - h)
    xs = [F(k, 50) for k in range(0, 50) if F(k, 50) <= eff]
    for x in xs:
        if x >= 1:
            continue
        cov = (eff - x) / (1 - x)
        if (cov >= 1) != (eff >= 1):
            bad += 1
block("L04 Remark 4.1 measured coverage threshold 1/(1-h)", 2000, bad == 0)
bad = 0 if (1 / (1 - F(1, 20))) == F(20, 19) else 1
block("L04 Remark 4.1 threshold for h=1/20 is 20/19", 1, bad == 0)

# ---- L05 Prop 2.1, 2.2, 2.4, 2.5, 2.6 by enumeration over random parameters
bad = 0
cases = 0
for _ in range(400):
    cases += 1
    p = F(rng.randint(1, 99), 100)
    kappa = rng.randint(0, 50)
    ell = [rng.randint(0, 6) for _ in range(3)]
    a = [kappa * l for l in ell]
    mean_closed = p * kappa * sum(ell)
    ind = []
    for pat in itertools.product((0, 1), repeat=3):
        pr = F(1)
        for x in pat:
            pr *= p if x else 1 - p
        ind.append((pr, sum(ai * x for ai, x in zip(a, pat))))
    mean3 = sum(pr * c for pr, c in ind)
    com = [(1 - p, 0), (p, kappa * sum(ell))]
    mean4 = sum(pr * c for pr, c in com)
    if not (mean3 == mean_closed == mean4):
        bad += 1
    var3 = sum(pr * c * c for pr, c in ind) - mean3 ** 2
    var4 = sum(pr * c * c for pr, c in com) - mean4 ** 2
    diff_closed = 2 * kappa * kappa * p * (1 - p) * sum(ell[i] * ell[j] for i in range(3) for j in range(i + 1, 3))
    if var4 - var3 != diff_closed:
        bad += 1
    if var4 - var3 < 0:
        bad += 1
    if (var4 - var3 == 0) != (sum(1 for l in ell if l > 0) <= 1 or kappa == 0):
        bad += 1
    if all(l >= 1 for l in ell) and kappa >= 1:
        p0_ind = sum(pr for pr, c in ind if c == 0)
        p0_com = sum(pr for pr, c in com if c == 0)
        if not (p0_ind < p0_com):
            bad += 1
block("L05 Prop 2.1/2.2/2.4 (mean), Prop 2.5 (variance difference and sign), Prop 2.6 (no-cost probability)",
      cases, bad == 0)

for name, ok, n in results:
    print(("PASS " if ok else "FAIL ") + f"[{n} cases] " + name)
print(f"blocks {len(results)} pass {sum(1 for _, ok, _ in results if ok)} fail {sum(1 for _, ok, _ in results if not ok)}")
