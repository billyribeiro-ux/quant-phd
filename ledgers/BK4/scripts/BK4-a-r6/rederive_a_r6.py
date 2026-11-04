"""Independent re-derivation of the printed numbers of BK4 L01, L02, L03 (slice a, round 6).

Run as: python3 -I ledgers/BK4/scripts/BK4-a-r6/rederive_a_r6.py
Uses only the standard library. The seeded draws reproduce the twins' RNG call order (the only way to
recover the printed day); every derived value is then computed here by a different method (brute force,
fractions, or a direct sort), not by importing the twins.
"""
import random
from fractions import Fraction
from math import floor

print("== L01 (seed 20260, 12 payments, 3 banks)")
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    d = rng.randint(100, 5000)
    day.append((seq, s, r, 100 * d))
for seq, s, r, a in day:
    print(f"payment {seq:2d}: B{s + 1} pays B{r + 1} {a:>9d}")
gross = sum(a for *_, a in day)
net = [sum(a for _, s, r, a in day if r == b) - sum(a for _, s, r, a in day if s == b) for b in range(3)]
debit = [max(0, -x) for x in net]
# peak need by brute force: least o >= 0 such that o + running sum >= 0 at every prefix
need = []
for b in range(3):
    run, sums = 0, [0]
    for _, s, r, a in day:
        if s == b:
            run -= a
        elif r == b:
            run += a
        sums.append(run)
    o = 0
    while any(o + x < 0 for x in sums):
        o += 1
    need.append(o)
    # the minimal-o argument: o-1 must fail when o > 0 (checked by the loop) and need == max(0,-min)
    assert o == max(0, -min(sums))
for b in range(3):
    print(f"B{b + 1}: need {need[b]} net {net[b]:+d} debit {debit[b]} need>=debit {need[b] >= debit[b]}")
print("net sum zero", sum(net) == 0, "all need>=debit", all(need[b] >= debit[b] for b in range(3)))
print("gross", gross, "moved", sum(debit))
ratio = Fraction(sum(debit), gross)
print("ratio", float(ratio), "to 4 places (half up):", round(float(ratio) + 1e-12, 4), "percent", float(ratio * 100))
print("banks positive debit", sum(1 for x in debit if x > 0), "need>debit", sum(1 for b in range(3) if need[b] > debit[b]))

print("== L02 (seed 2026, 6 trades, 4 members)")
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    p, r = rng.sample(range(4), 2)
    d = rng.randint(500, 20000)
    trades.append((seq, p, r, 100 * d))
for seq, p, r, a in trades:
    print(f"trade {seq}: m{p + 1} owes m{r + 1} {a}")
G = sum(a for *_, a in trades)
rec = [sum(a for _, p, r, a in trades if r == m) for m in range(4)]
pay = [sum(a for _, p, r, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
print("rec", rec, "pay", pay)
print("G", G, "sum rec", sum(rec), "sum pay", sum(pay), "n", n, "sum n", sum(n))
print("A", A, "sum max(0,-n)", sum(max(0, -x) for x in n), "reduction", G - A, "bp", (10000 * (G - A)) // G)
print("exact bp value", float(Fraction(10000 * (G - A), G)))
# Example 2.4 and M1, M2, M3 hand examples
def netting(tr):
    """tr: list of (payer, receiver, cents). Returns (G, A, net obligations dict, floored bp reduction)."""
    G = sum(a for _, _, a in tr)
    members = sorted({p for p, _, _ in tr} | {r for _, r, _ in tr})
    rec = {m: sum(a for _, r, a in tr if r == m) for m in members}
    pay = {m: sum(a for p, _, a in tr if p == m) for m in members}
    n = {m: rec[m] - pay[m] for m in members}
    A = sum(max(0, x) for x in n.values())
    return G, A, n, (10000 * (G - A)) // G
D = 100
ex24 = [(1, 2, 100 * D), (2, 3, 80 * D), (3, 1, 50 * D)]
print("Ex2.4", netting(ex24))
ex24x2 = [(p, r, 2 * a) for p, r, a in ex24]
print("Ex2.4 doubled (M2)", netting(ex24x2))
m1 = [(1, 2, 5000), (2, 3, 7000), (3, 4, 2000), (4, 1, 4000)]
print("M1", netting(m1))
m3 = [(1, 2, 10000), (1, 3, 10000)]
print("M3", netting(m3))
print("P3 cycle k=3 a=1", netting([(1, 2, 1), (2, 3, 1), (3, 1, 1)]))
print("R2 X A", netting([(1, 2, 10000)])[1], "Y A", netting([(1, 2, 10000), (3, 4, 5000), (4, 3, 5000)])[1], "G X", netting([(1, 2, 10000)])[0], "G Y", netting([(1, 2, 10000), (3, 4, 5000), (4, 3, 5000)])[0])
print("9-bp:", float(Fraction(10000 * 2502700, 7596300)))

print("== L03 (seed 2026 margins, DF, capital, 200 losses)")
def waterfall(loss, defaulter, im, df, cap):
    a1 = min(loss, im[defaulter])
    a2 = min(loss - a1, df[defaulter])
    a3 = min(loss - a1 - a2, cap)
    Z = loss - a1 - a2 - a3
    surv = sorted(i for i in df if i != defaulter)
    Dtot = sum(df[i] for i in surv)
    if Z >= Dtot:
        pays = {i: df[i] for i in surv}
        u = Z - Dtot
    else:
        x = {i: floor(Fraction(Z * df[i], Dtot)) for i in surv}
        l = Z - sum(x.values())
        pays = dict(x)
        for i in surv:
            if l == 0:
                break
            if df[i] > 0:
                pays[i] += 1
                l -= 1
        assert l == 0
        u = 0
    assert a1 + a2 + a3 + sum(pays.values()) + u == loss
    return a1, a2, a3, pays, u
fix_im = {1: 0, 2: 0, 3: 100}
fix_df = {1: 40, 2: 60, 3: 50}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    print("fixture", L, waterfall(L, 3, fix_im, fix_df, 30))
for L in (1, 2):
    print("remainder", L, waterfall(L, 4, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0))
rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
print("im", im, "df", df, "cap", cap)
for L in (1529, 3160, 5850):
    pass
print("A3 1529", waterfall(1529, 3, im, df, cap))
print("A3 3160", waterfall(3160, 3, im, df, cap))
print("A3 5850", waterfall(5850, 3, im, df, cap))
losses = [rng.randint(0, 3000) for _ in range(200)]
sl = sorted(losses)
for target in (9900, 9975):
    k = -(-target * 200 // 10000)
    # brute-force smallest integer margin with cover >= target (bp, floored)
    def cover(M):
        c = sum(1 for x in losses if x <= M)
        return (10000 * c) // 200
    brute = next(M for M in range(0, 3001) if cover(M) >= target)
    print(f"target {target}: k {k}, sorted[k-1] {sl[k - 1]}, brute {brute}, cover(sized) {cover(sl[k - 1])}, cover(sized-1) {cover(sl[k - 1] - 1)}")
print("L(198), L(199), L(200):", sl[197], sl[198], sl[199], "max", max(losses), "min", min(losses))
print("count <= 2961:", sum(1 for x in losses if x <= 2961), "count <= 2960:", sum(1 for x in losses if x <= 2960))
print("count <= 2992:", sum(1 for x in losses if x <= 2992), "count <= 2991:", sum(1 for x in losses if x <= 2991))
print("above 2961:", sum(1 for x in losses if x > 2961), "above 2992:", sum(1 for x in losses if x > 2992))
print("ties at L(198)=L(199)?", sl[197] == sl[198])
