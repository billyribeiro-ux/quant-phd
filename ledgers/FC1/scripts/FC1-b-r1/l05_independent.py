# Independent re-derivation of Lab 1 L05 numbers and the prose figures (Fractions, not the lab's helpers).
import random, datetime
from fractions import Fraction
rng = random.Random(2026)
P = ["P1", "P2", "P3", "P4", "P5"]
resting = []
for t in range(3):
    owner = P[t + 1]
    px = 10000 + rng.randint(0, 400)
    q = rng.randint(100, 500)
    resting.append((owner, px, q, t))
best = min(resting, key=lambda r: (r[1], r[3]))
inc_px = best[1] + rng.randint(0, 200)
inc_q = rng.randint(1, best[2])
print("resting", resting, "incoming", ("P1", inc_px, inc_q))
# one fill: incoming quantity <= best quantity
fill_q = min(inc_q, best[2]); cons = fill_q * best[1]
print("fill", fill_q, "at", best[1], "owner", best[0], "consideration", cons, "limit", inc_px, "price<=limit", best[1] <= inc_px)
td = datetime.date(2026, 10, 28)
def bd(start, k):
    d = start; c = 0
    while c < k:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            c += 1
    return d
print("trade date weekday", td.strftime("%A"), "settle(2)", bd(td, 2), bd(td, 2).strftime("%A"), "settle(3)", bd(td, 3))
batch = []
for _ in range(20):
    b, s = rng.sample(P, 2)
    batch.append((b, s, rng.randint(5000, 20000), rng.randint(1, 500)))
G = sum(px * q for _, _, px, q in batch)
net = {p: 0 for p in P}
for b, s, px, q in batch:
    net[s] += px * q; net[b] -= px * q
NP = sum(max(-v, 0) for v in net.values())
payers = [p for p in P if net[p] < 0]
print("G", G, "NP", NP, "payers", payers, "sum", sum(net.values()))
print("net", net)
r = Fraction(NP, G)
print("ratio exact", float(r), "8dp", f"{float(r):.8f}", "5dp", f"{float(r):.5f}", "3dp half-up", float(Fraction(1000*NP,G)+Fraction(1,2)))
print("ratio 8dp exact digits", float(Fraction(NP*10**8, G)))
print("E1: P5 net receipt / gross", float(Fraction(11060360, G)) * 100, " / NP", float(Fraction(11060360, NP)) * 100)
print("E2: sum negatives", 7411991 + 6656379 + 214044, " positives", 3222054 + 11060360)
print("M3 check", 100*10000, "G", 2*100*10000)
print("Q4 settle day", bd(td, 2).day)
print("Fractions NP/G to 4dp", round(float(r), 4))
