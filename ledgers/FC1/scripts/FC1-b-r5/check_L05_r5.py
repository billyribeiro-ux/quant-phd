import random, datetime
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
# independent re-derivation of the L05 seeded draws and every printed number
rng = random.Random(2026)
P = ("P1", "P2", "P3", "P4", "P5")
resting = []
for t in range(3):
    owner = P[t + 1]
    px = 10000 + rng.randint(0, 400)
    q = rng.randint(100, 500)
    resting.append((owner, px, q, t))
best = min(resting, key=lambda o: (o[1], o[3]))
inc_px = best[1] + rng.randint(0, 200)
inc_q = rng.randint(1, best[2])
print("resting", resting, "incoming", inc_px, inc_q)
fill_q = min(inc_q, best[2])
cons = fill_q * best[1]
print("fill", fill_q, "price", best[1], "consideration", cons, "check 216*10060 =", 216 * 10060)
d0 = datetime.date(2026, 10, 28)
def bd(start, k):
    d = start; c = 0
    while c < k:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5: c += 1
    return d
print("settle lag2", bd(d0, 2), bd(d0, 2).strftime("%A"), "lag3", bd(d0, 3), bd(d0, 3).strftime("%A"))
trades = []
for _ in range(20):
    b, s = rng.sample(P, 2)
    trades.append((b, s, rng.randint(5000, 20000), rng.randint(1, 500)))
gross = sum(p * q for _, _, p, q in trades)
net = {p: 0 for p in P}
for b, s, p, q in trades:
    net[s] += p * q
    net[b] -= p * q
np_ = sum(max(-v, 0) for v in net.values())
payers = sum(1 for v in net.values() if v < 0)
print("gross", gross, "net_payments", np_, "payers", payers, "sum", sum(net.values()))
print("net", net)
r = Fraction(np_, gross)
print("ratio exact", float(r), "8dp", f"{float(r):.8f}", "5dp", f"{float(r):.5f}")
q8 = (Decimal(np_) / Decimal(gross)).quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)
print("ratio 8dp via Decimal", q8, "3dp half up", (Decimal(np_) / Decimal(gross)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))
print("4dp half up", (Decimal(np_) / Decimal(gross)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
p5 = net["P5"]
print("E1 P5 receipt / gross (Decimal 2dp):", (Decimal(p5) / Decimal(gross) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "exact pct", float(Fraction(p5, gross) * 100))
print("E1 P5 receipt / net (2dp):", (Decimal(p5) / Decimal(np_) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "exact", float(Fraction(p5, np_) * 100))
print("E1 raw quotient", float(Fraction(11060360, 68398886)), "E1 raw 6dp", f"{11060360/68398886:.6f}")
print("E2 sum of negatives", -(net["P1"] + net["P2"] + net["P4"]), "positives", net["P3"] + net["P5"])
print("E5 ratio P5/gross", 11060360/68398886, "P5 over net", 11060360/14282414)
print("E2 check printed:", 7411991 + 6656379 + 214044, 3222054 + 11060360)
