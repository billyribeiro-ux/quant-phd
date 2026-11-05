"""Independent recomputation of every number on BK4 L01-L03 pages (verifier r13).

Written from the page definitions, not from the lab twins. Uses only the standard library and the same
seeded draws as the labs (random.Random(seed) call order), so the seeded inputs are reproduced.
"""

from fractions import Fraction
from math import ceil
import random

out = []


def p(*a):
    out.append(" ".join(str(x) for x in a))


# ---------- L01: payments ----------
rng = random.Random(20260)
payments = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    payments.append((seq, s, r, 100 * dollars))
gross = sum(a for *_, a in payments)
p("L01 gross cents", gross)
nets, needs, debits = [], [], []
for b in range(3):
    S = 0
    mn = 0
    for _, s, r, a in payments:  # sending order
        if r == b:
            S += a
        if s == b:
            S -= a
        mn = min(mn, S)
    net = S
    need = max(0, -mn)
    debit = max(0, -net)
    nets.append(net)
    needs.append(need)
    debits.append(debit)
    p("L01 bank", "ABC"[b], "need", need, "net", net, "debit", debit, "need>=debit", need >= debit)
p("L01 sum nets", sum(nets), "moved", sum(debits), "funded", sum(d > 0 for d in debits), "beyond", sum(n > d for n, d in zip(needs, debits)))
ratio = Fraction(sum(debits), gross)
p("L01 ratio exact", float(ratio), "to 8 places", f"{float(ratio):.8f}", "to 4 places", f"{float(ratio):.4f}", "percent", f"{float(ratio)*100:.2f}")
p("L01 gross in dollars", Fraction(gross, 100))

# Example 2.6 and Remark 2.7 by hand
ex = [(1, "A", "B", 100), (2, "B", "C", 80), (3, "C", "A", 50)]
def running(order, bank):
    S = 0
    vals = [0]
    for _, s, r, a in order:
        if r == bank:
            S += a
        if s == bank:
            S -= a
        vals.append(S)
    return vals
for bank in "ABC":
    v = running(ex, bank)
    p("L01 Ex2.6", bank, v, "need", max(0, -min(v)))
v2 = running([ex[2], ex[0], ex[1]], "A")
p("L01 Rem2.7 A running", v2, "need", max(0, -min(v2)))

# ---------- L02: netting ----------
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    payer, receiver = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((seq, payer, receiver, 100 * dollars))
G = sum(a for *_, a in trades)
rec = [sum(a for _, pa, re, a in trades if re == m) for m in range(4)]
pay = [sum(a for _, pa, re, a in trades if pa == m) for m in range(4)]
net = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, n) for n in net)
p("L02 trades", trades)
p("L02 rec", rec, "pay", pay)
p("L02 G", G, "net", net, "sum net", sum(net), "A", A, "A==sum neg", A == sum(max(0, -n) for n in net), "reduction", G - A, "bp", 10000 * (G - A) // G, "bp exact", float(Fraction(10000 * (G - A), G)))
p("L02 A dollars", Fraction(A, 100))
# Example 2.4
ex24 = [(1, 1, 2, 100), (2, 2, 3, 80), (3, 3, 1, 50)]
rec24 = {m: sum(a for _, pa, re, a in ex24 if re == m) for m in (1, 2, 3)}
pay24 = {m: sum(a for _, pa, re, a in ex24 if pa == m) for m in (1, 2, 3)}
n24 = {m: rec24[m] - pay24[m] for m in (1, 2, 3)}
A24 = sum(max(0, n) for n in n24.values())
p("L02 Ex2.4 rec", rec24, "pay", pay24, "net", n24, "A", A24, "G", 230, "bp", 10000 * (230 - A24) // 230, "exact bp", float(Fraction(10000 * 180, 230)))
# M1 chain
ch = [(1, 1, 2, 50), (2, 2, 3, 70), (3, 3, 4, 20), (4, 4, 1, 40)]
r_ = {m: sum(a for _, pa, re, a in ch if re == m) for m in (1, 2, 3, 4)}
p_ = {m: sum(a for _, pa, re, a in ch if pa == m) for m in (1, 2, 3, 4)}
nn = {m: r_[m] - p_[m] for m in (1, 2, 3, 4)}
AA = sum(max(0, n) for n in nn.values())
p("L02 M1 net", nn, "A", AA, "G", sum(a for *_, a in ch), "bp", float(Fraction(10000 * (180 - 50), 180)))
p("L02 M2 bp", float(Fraction(10000 * 360, 460)))

# ---------- L03: waterfall ----------
def waterfall(L, defaulter, im, df, K):
    a1 = min(L, im[defaulter])
    a2 = min(L - a1, df[defaulter])
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in df if i != defaulter)
    D = sum(df[i] for i in surv)
    pays = {}
    unc = 0
    if Z >= D:
        pays = {i: df[i] for i in surv}
        unc = Z - D
    else:
        pr = {i: Fraction(Z * df[i], D) for i in surv}
        fl = {i: pr[i].numerator // pr[i].denominator for i in surv}
        ell = Z - sum(fl.values())
        for i in surv:
            pays[i] = fl[i]
        for i in surv:
            if ell and df[i] > 0:
                pays[i] += 1
                ell -= 1
        assert ell == 0
    total = a1 + a2 + a3 + sum(pays.values()) + unc
    assert total == L, (L, total)
    return a1, a2, a3, pays, unc

fim = {1: 0, 2: 0, 3: 100}
fdf = {1: 40, 2: 60, 3: 50}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    p("L03 Ex1.5 fixture", L, waterfall(L, 3, fim, fdf, 30))
p("L03 Ex1.6", [waterfall(L, 4, {1: 0, 2: 0, 3: 0, 4: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0) for L in (1, 2)])

rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
p("L03 inputs im", im, "df", df, "cap", cap)
sv = sum(df[i] for i in (1, 2, 4))
for L in (im[3] // 2, im[3] + df[3] // 2, im[3] + df[3] + cap + sv // 2):
    p("L03 A3 scenario", L, waterfall(L, 3, im, df, cap))
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)
for t in (9900, 9975):
    k = ceil(Fraction(t * 200, 10000))
    margin = srt[k - 1]
    cov = lambda M: 10000 * sum(1 for x in losses if x <= M) // 200
    brute = next(M for M in range(0, 10**6) if cov(M) >= t)
    p("L03 target", t, "k", k, "sized", margin, "brute", brute, "cover at", cov(margin), "cover below", cov(margin - 1))
p("L03 max loss", srt[-1], "count above 9900 margin", sum(1 for x in losses if x > srt[197]))

print("\n".join(out))
