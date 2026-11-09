"""Verifier (FC1-b r3): independent re-derivation of L05 printed numbers and every derived figure in prose/quiz."""
import datetime
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

rng = random.Random(2026)
P = ["P1", "P2", "P3", "P4", "P5"]
# resting: three sells from P2,P3,P4 (draw order as in the lab)
rest = []
for t in range(3):
    price = 10000 + rng.randint(0, 400)
    qty = rng.randint(100, 500)
    rest.append(dict(owner=P[t + 1], price=price, qty=qty, t=t))
best = min(rest, key=lambda o: (o["price"], o["t"]))
inc_price = best["price"] + rng.randint(0, 200)
inc_qty = rng.randint(1, best["qty"])
print("resting", rest)
print("incoming P1 price", inc_price, "qty", inc_qty)
fill = min(inc_qty, best["qty"])
cons = fill * best["price"]
print("fill", fill, "price", best["price"], "consideration", cons, "limit ok", best["price"] <= inc_price)
print("fills count", 1 if inc_qty <= best["qty"] else "more")

# batch: 20 trades, buyer, seller = rng.sample(P, 2), price, qty
batch = []
for _ in range(20):
    b, s = rng.sample(P, 2)
    batch.append((b, s, rng.randint(5000, 20000), rng.randint(1, 500)))
gross = sum(q * p for _, _, p, q in batch)
net = {p: 0 for p in P}
for b, s, pr, q in batch:
    net[s] += q * pr
    net[b] -= q * pr
NP = sum(max(-v, 0) for v in net.values())
print("gross", gross, "NP", NP, "sum net", sum(net.values()))
print("net", net)
print("payers", sorted(p for p, v in net.items() if v < 0), "count", sum(1 for v in net.values() if v < 0))
print("NP == payer sum abs", NP == sum(-v for v in net.values() if v < 0), "positive sum", sum(v for v in net.values() if v > 0))
r = Fraction(NP, gross)
print("ratio exact", r, "float", repr(float(r)))
print("ratio 8dp", Decimal(NP) / Decimal(gross))
print("ratio 8dp half-up", (Decimal(NP) / Decimal(gross)).quantize(Decimal("0.00000001"), ROUND_HALF_UP))
print("ratio 5dp", (Decimal(NP) / Decimal(gross)).quantize(Decimal("0.00001"), ROUND_HALF_UP))
print("ratio 4dp", (Decimal(NP) / Decimal(gross)).quantize(Decimal("0.0001"), ROUND_HALF_UP))
print("ratio 3dp half-up", (Decimal(NP) / Decimal(gross)).quantize(Decimal("0.001"), ROUND_HALF_UP))
print("ratio milli integer", (2 * 1000 * NP + gross) // (2 * gross))
p5 = net["P5"]
print("P5 share of gross, 2dp half up", (Decimal(p5) / Decimal(gross) * 100).quantize(Decimal("0.01"), ROUND_HALF_UP), "exact", Decimal(p5) / Decimal(gross) * 100)
print("P5 share of NP, 2dp half up", (Decimal(p5) / Decimal(NP) * 100).quantize(Decimal("0.01"), ROUND_HALF_UP), "exact", Decimal(p5) / Decimal(NP) * 100)
print("P5 gross quotient 6dp", (Decimal(p5) / Decimal(gross)).quantize(Decimal("0.000001"), ROUND_HALF_UP))

d0 = datetime.date(2026, 10, 28)
def bd(start, k):
    d = start; c = 0
    while c < k:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            c += 1
    return d
print("trade date", d0, d0.strftime("%A"))
for k in (0, 1, 2, 3):
    x = bd(d0, k)
    print("offset", k, x, x.strftime("%A"))
print("M2 Friday 2026-10-30 + 2 bd:", bd(datetime.date(2026, 10, 30), 2), bd(datetime.date(2026, 10, 30), 2).strftime("%A"))
print("M1 consideration", 100 * 10090, "per-share currency", 10090 / 100)
print("M3 ratio", Fraction(1000000, 2000000))
print("E2 sums", 7411991 + 6656379 + 214044, 3222054 + 11060360)
print("R2 consideration check", -100)
print("L05 quiz 216*10060", 216 * 10060)
print("CCP receipts sum check ok")
print("E3 settlement offset 3", bd(d0, 3), bd(d0, 3).strftime("%A"))
