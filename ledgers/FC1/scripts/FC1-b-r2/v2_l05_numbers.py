# Round-2 independent re-derivation for L05 Lab 1 (own code; same RNG call order as the lesson's generator),
# the page's E1-E3, M1-M3, P1-P3, R2 arithmetic, and Proposition 2.1 / 2.2 property checks.
import datetime, random, sys
P = ("P1", "P2", "P3", "P4", "P5")
SEED = 2026
start = datetime.date(2026, 10, 28)

def add_business_days(d, n):
    while n > 0:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d

def draw_book(rng):
    rest = []
    for t in range(3):
        price = 10000 + rng.randint(0, 400)
        qty = rng.randint(100, 500)
        rest.append({"owner": P[t + 1], "price": price, "qty": qty, "t": t})
    best = min(rest, key=lambda o: (o["price"], o["t"]))
    inc_price = best["price"] + rng.randint(0, 200)
    inc_qty = rng.randint(1, best["qty"])
    return rest, {"owner": "P1", "price": inc_price, "qty": inc_qty}

def draw_batch(rng, n=20):
    trades = []
    for _ in range(n):
        b, s = rng.sample(P, 2)
        trades.append((b, s, rng.randint(5000, 20000), rng.randint(1, 500)))
    return trades

def positions(trades):
    x = {p: 0 for p in P}
    for b, s, pr, q in trades:
        c = pr * q
        x[s] += c
        x[b] -= c
    return x

rng = random.Random(SEED)
rest, inc = draw_book(rng)
eligible = sorted([o for o in rest if o["price"] <= inc["price"]], key=lambda o: (o["price"], o["t"]))
fills = []
rem = inc["qty"]
for o in eligible:
    if rem == 0: break
    f = min(rem, o["qty"]); fills.append((o, f)); rem -= f
print("resting", [(o["owner"], o["price"], o["qty"]) for o in sorted(rest, key=lambda o: (o["price"], o["t"]))])
print("incoming", inc)
print("fills", [(o["owner"], o["price"], f) for o, f in fills])
o, f = fills[0]
cons = f * o["price"]
print("consideration", cons, "= ", f, "x", o["price"], "; trade date", start, start.strftime("%A"))
for name, off in [("settlement lag 2", 2), ("clearing 0", 0)]:
    d = add_business_days(start, off)
    print(name, "->", d, d.strftime("%A"))
batch = draw_batch(rng)
gross = sum(pr * q for _, _, pr, q in batch)
x = positions(batch)
np_ = sum(max(-v, 0) for v in x.values())
payers = [p for p in P if x[p] < 0]
print("batch trades", len(batch), "gross", gross, "net payments", np_, "sum x", sum(x.values()), "net payers", payers)
print("net positions", x)
print("ratio exact", np_ / gross, "8dp", f"{np_/gross:.8f}", "5dp", f"{np_/gross:.5f}")
print("half-up 3dp via integers:", (2*1000*np_ + gross)//(2*gross), "-> 0.%03d" % ((2*1000*np_ + gross)//(2*gross)))
print("E1 P5 receipt / gross =", x["P5"] / gross, "(16.17 expected)", " / net =", x["P5"] / np_, "(77.44 expected)")
print("E2 sum of |negatives| =", sum(-v for v in x.values() if v < 0), "positives =", sum(v for v in x.values() if v > 0))
print("E2 explicit", 7411991 + 6656379 + 214044, "=", 3222054 + 11060360)
# Hand problems
print("M1 consideration", 100 * 10090, "= 1009000 (check)")
print("M3 net-to-gross", 1000000 / 2000000)
print("R2 bound 100 <= -100 ->", 100 <= -100)
print("weekday checks:", [(d.isoformat(), d.strftime('%A')) for d in [datetime.date(2026,10,30), datetime.date(2026,11,2), datetime.date(2026,11,3)]])
print("M2 Friday 2026-10-30 + 2 business days =", add_business_days(datetime.date(2026,10,30), 2))

# Property checks on random batches (Proposition 2.1: sum x = 0, 0 <= NP <= G under A1 positive integers)
bad = 0
for seed in range(2000):
    r = random.Random(seed)
    tr = draw_batch(r, n=r.randint(1, 30))
    xx = positions(tr)
    g = sum(pr * q for _, _, pr, q in tr)
    npp = sum(max(-v, 0) for v in xx.values())
    if sum(xx.values()) != 0 or not (0 <= npp <= g): bad += 1
print("Prop 2.1 property failures over 2000 random batches:", bad)

# P2 property: removing one trade changes NP by at most its consideration (|dNP| <= c_t), A1 batches
bad2 = 0
for seed in range(2000):
    r = random.Random(seed)
    tr = draw_batch(r, n=r.randint(2, 15))
    npA = sum(max(-v, 0) for v in positions(tr).values())
    k = r.randrange(len(tr))
    ct = tr[k][2] * tr[k][3]
    rest_tr = tr[:k] + tr[k+1:]
    npB = sum(max(-v, 0) for v in positions(rest_tr).values())
    if abs(npA - npB) > ct: bad2 += 1
print("P2 property failures over 2000 random batches:", bad2)
