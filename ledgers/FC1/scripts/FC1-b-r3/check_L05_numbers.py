"""Independent checks for L05 (FC1-b round 3): re-derives the lab's seeded numbers, the page's derived figures,
the lag-3 variant (E3), Proposition 2.1 and P2 bounds on random batches, and R2. Run:
.venv/bin/python -I ledgers/FC1/scripts/FC1-b-r3/check_L05_numbers.py <twin path>
"""

from __future__ import annotations

import datetime
import random
import sys
import types
from fractions import Fraction

twin_path = sys.argv[1]
src = open(twin_path, encoding="utf-8").read().replace("\nmain()\n", "\n")


def run_twin(lag: int | None = None) -> str:
    import contextlib
    import io

    text = src if lag is None else src.replace("SETTLEMENT_LAG = 2 ", f"SETTLEMENT_LAG = {lag} ")
    assert lag is None or f"SETTLEMENT_LAG = {lag} " in text
    mod = types.ModuleType("twin")
    sys.modules["twin"] = mod
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(text + "\nmain()\n", twin_path, "exec"), mod.__dict__)
    return buf.getvalue()


base = run_twin()
lag3 = run_twin(3)
print("E3 changed lines (lag 2 -> 3):")
for a, b in zip(base.splitlines(), lag3.splitlines(), strict=True):
    if a != b:
        print("  -", a)
        print("  +", b)

# Independent calendar
def bday(start: datetime.date, k: int) -> datetime.date:
    d, c = start, 0
    while c < k:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            c += 1
    return d


td = datetime.date(2026, 10, 28)
print("trade date weekday", td.strftime("%A"), "offset2", bday(td, 2), bday(td, 2).strftime("%A"), "offset3", bday(td, 3))
assert bday(td, 2) == datetime.date(2026, 10, 30) and bday(td, 3) == datetime.date(2026, 11, 2)
assert datetime.date(2026, 10, 30).strftime("%A") == "Friday" and bday(datetime.date(2026, 10, 30), 2) == datetime.date(2026, 11, 3)

# Lab 1 trade by hand
print("trade consideration 216*10060 =", 216 * 10060)
assert 216 * 10060 == 2172960

# Batch: re-derive from the lab's documented generator (seed 2026; the draws after the book draws)
PART = ("P1", "P2", "P3", "P4", "P5")
rng = random.Random(2026)
for _ in range(3):
    rng.randint(0, 400)
    rng.randint(100, 500)
best_price = None
# replicate seeded_book exactly as documented (3 resting sells, then incoming) using the same call order
rng = random.Random(2026)
res = []
for t in range(3):
    res.append((10000 + rng.randint(0, 400), rng.randint(100, 500), t))
best = min(res, key=lambda r: (r[0], r[2]))
inc_price = best[0] + rng.randint(0, 200)
inc_qty = rng.randint(1, best[1])
print("resting", res, "incoming", inc_price, inc_qty)
assert (inc_price, inc_qty) == (10117, 216) and best[0] == 10060 and best[1] == 263
gross = 0
net = {p: 0 for p in PART}
for _ in range(20):
    buyer, seller = rng.sample(PART, 2)
    price = rng.randint(5000, 20000)
    qty = rng.randint(1, 500)
    c = price * qty
    gross += c
    net[seller] += c
    net[buyer] -= c
netpay = sum(max(-v, 0) for v in net.values())
q = Fraction(netpay, gross)
print("gross", gross, "net_payments", netpay, "quotient", float(q), "net", net, "payers", sum(v < 0 for v in net.values()))
assert gross == 68398886 and netpay == 14282414 and sum(net.values()) == 0
assert round(float(q), 5) == 0.20881
assert (q * 1000 + Fraction(1, 2)).__floor__() == 209
print("E1 P5 share of gross", float(Fraction(11060360, 68398886)) * 100, "% ; of net", float(Fraction(11060360, 14282414)) * 100, "%")
print("E2 sums", 7411991 + 6656379 + 214044, 3222054 + 11060360)
assert 7411991 + 6656379 + 214044 == 14282414 == 3222054 + 11060360

# Random checks of Proposition 2.1 and P2 bound, with arbitrary batches (A1: positive integers, distinct parties)
rnd = random.Random(7)
for trial in range(2000):
    parties = list(range(5))
    trades = []
    for _ in range(rnd.randint(1, 25)):
        b_, s_ = rnd.sample(parties, 2)
        trades.append((b_, s_, rnd.randint(1, 10**6) * rnd.randint(1, 500)))

    def netp(ts: list[tuple[int, int, int]]) -> tuple[dict[int, int], int, int]:
        x = {p: 0 for p in parties}
        g = 0
        for b_, s_, c in ts:
            x[s_] += c
            x[b_] -= c
            g += c
        return x, sum(max(-v, 0) for v in x.values()), g

    x, npay, g = netp(trades)
    assert sum(x.values()) == 0 and 0 <= npay <= g
    if trades:
        t = rnd.randrange(len(trades))
        rest = trades[:t] + trades[t + 1 :]
        _, npay2, _ = netp(rest)
        ct = trades[t][2]
        assert abs(npay - npay2) <= ct, (trial, npay, npay2, ct)
print("Prop 2.1 (i),(ii) and P2 bound: 2000 random batches PASS")

# R2: negative consideration example from the page
c = -100
xA, xB = -c, c
print("R2 xA", xA, "xB", xB, "NP", max(-xB, 0), "G", c, "bound 100 <= -100 ->", max(-xB, 0) <= c)
assert max(-xB, 0) == 100 and c == -100

# M1-M3
print("M1", 100 * 10090, "M3 G", 2 * 100 * 10000, "ratio", Fraction(1000000, 2000000))
print("L05 numbers: PASS")
