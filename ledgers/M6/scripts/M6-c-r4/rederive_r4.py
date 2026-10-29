# Independent re-derivation of the M6 L09-L12 numbers (round 4). Uses dict-DP and closed forms, not the lab code.
from fractions import Fraction as F
from itertools import product

# L09: fair walk, N=8, hitting time of +1 (first k>=1 with S_k=1)
def dist_hit(N):
    # dp over (level, hit_flag) with exact weights
    state = {(0, False): F(1)}
    hit_by = []
    cum = F(0)
    per_k = {}
    for k in range(1, N + 1):
        new = {}
        for (lv, h), p in state.items():
            if h:
                new[(lv, True)] = new.get((lv, True), 0) + p
                continue
            for s in (1, -1):
                nl = lv + s
                nh = nl == 1
                new[(nl, nh)] = new.get((nl, nh), 0) + p / 2
        state = new
        per_k[k] = sum(p for (lv, h), p in state.items() if h)
    return per_k
ph = dist_hit(8)
print("L09 P(tau<=k) k=1..8:", [str(ph[k]) for k in range(1, 9)])
print("L09 paths out of 256:", [int(ph[k] * 256) for k in range(1, 9)])

# L10: doubling with finite capital, DP over wealth (no enumeration)
def capital_table(K):
    m = (K + 1).bit_length() - 1
    # states: (wealth, bet index k) ; bet k stake 2^(k-1)
    dist = {K: F(1)}
    win = F(0); ruin = {}; exp_w = F(0)
    k = 1
    while dist:
        new = {}
        stake = 2 ** (k - 1)
        for w, p in dist.items():
            if stake > w:
                ruin[w] = ruin.get(w, 0) + p
                exp_w += p * w
                continue
            win += p / 2
            exp_w += p / 2 * (w + stake)
            new[w - stake] = new.get(w - stake, 0) + p / 2
        dist = new
        k += 1
    return m, win, sum(ruin.values()), sorted(ruin), exp_w
for K in (1, 6, 10, 100, 1000):
    m, w, r, rw, e = capital_table(K)
    print("L10 K", K, "m", m, "win", w, "ruin", r, "=2^-m", r == F(1, 2 ** m), "ruin wealth", rw, "E", e, "E==K", e == K)

# L10 Part B: stopped expectation without capital, closed form
for n in (1, 2, 3, 5, 10):
    p_beyond = F(1, 2 ** n)
    win_part = 1 - p_beyond           # wins contribute +1 each, P(tau<=n)
    loss_part = -(2 ** n - 1) * p_beyond
    print("L10 n", n, "E stopped", win_part + loss_part)

# L11: Doob ratio over horizons 1..12, grid j/2, Z=|S|, by DP over (S_k, running max>=lambda) is heavy; enumerate with own code
def walk_stats(N):
    res = []
    for path in product((1, -1), repeat=N):
        s = 0; mx = 0; zs = []
        for x in path:
            s += x; mx = max(mx, abs(s))
        res.append((abs(s), mx, path))
    return res
for N in range(1, 13):
    stats = walk_stats(N)
    w = F(1, 2 ** N)
    EZ = sum(w * z for z, _, _ in stats)
    best = (F(0), None, None)
    for j in range(1, 2 * (N + 1) + 1):
        lam = F(j, 2)
        pA = w * sum(1 for _, mx, _ in stats if mx >= lam)
        EZA = sum(w * z for z, mx, _ in stats if mx >= lam)
        assert lam * pA <= EZA <= EZ and pA <= EZ / lam
        ratio = lam * pA / EZ
        if ratio > best[0]:
            best = (ratio, lam, pA)
    print("L11 N", N, "EZ", EZ, "largest ratio", float(best[0]), "lambda", best[1], "P(A)", best[2])
# L11 Part C signed walk
for N in (1, 2):
    w = F(1, 2 ** N)
    p = w * sum(1 for path in product((1, -1), repeat=N) if max([0] + list(__import__('itertools').accumulate(path))) >= 1)
    ES = sum(w * sum(path) for path in product((1, -1), repeat=N))
    print("L11 signed N", N, "P", p, "E S_N", ES, "bound holds", p <= ES)

# L12: dyadic martingale, exact cell integrals, independent formulation via midpoints of j/2^n
for n in range(0, 11):
    cells = 2 ** n
    h = F(1, cells)
    err = sum(((h / 2) ** 3 * 2) / 3 for _ in range(cells))  # each cell: int (x-c)^2 = h^3/12
    assert err == F(1, 12 * 4 ** n)
    m2 = sum(((F(2 * j + 1, 2 * cells)) ** 2) * h for j in range(cells))
    assert m2 == F(1, 3) - F(1, 12 * 4 ** n), n
print("L12 dyadic formulas re-derived for n=0..10")
print("L12 level 10 max grid error", F(1, 2 ** 11), "float", float(F(1, 2048)))
# all-heads martingale
print("L12 E[M_n]=1 check:", [str(F(2 ** n) * F(1, 2 ** n)) for n in range(0, 11)])
