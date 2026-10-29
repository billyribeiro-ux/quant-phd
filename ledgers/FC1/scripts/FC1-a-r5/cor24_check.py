import random
rng = random.Random(11)
hits = 0; total = 0
for _ in range(5000):
    h = rng.randint(1, 5); mid = rng.randint(9000, 11000)
    buys = [rng.randint(1, 40) for _ in range(3)]
    tot = sum(buys)
    cut = rng.randint(1, tot - 1)
    sells = [cut, tot - cut]
    trades = [(1, b) for b in buys] + [(-1, s) for s in sells]
    C = sum(sg * q * (mid + sg * h) for sg, q in trades)
    Q = sum(q for sg, q in trades if sg == 1)
    total += 1
    hits += (C == (2 * h) * Q)
print("closed one-mid sequences with P = C = sQ (s = 2h, Q = buy volume):", hits, "of", total)
