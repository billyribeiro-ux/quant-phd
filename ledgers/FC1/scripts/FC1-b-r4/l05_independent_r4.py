"""Verifier re-derivation (FC1-b round 4) of every number printed by Lab 1 (L05) and quoted in L05.html.

Independent of tests/labs/FC1/lab-FC1-L05-1.py: exact Fraction arithmetic, a calendar walk written from scratch,
and the netting identities checked by hand-coded sums. The RNG call order follows the lab's stated order
(seeded_book: three resting sells, each price then quantity; incoming buy, offset then quantity; then the batch:
sample two participants, price, quantity), so the SIMULATED draws are the ones the lab prints.

Usage: python3 -I ledgers/FC1/scripts/FC1-b-r4/l05_independent_r4.py
"""

from __future__ import annotations

import datetime
import random
from fractions import Fraction

SEED = 2026
P = ["P1", "P2", "P3", "P4", "P5"]


def weekday_name(d: datetime.date) -> str:
    return d.strftime("%A")


def bd_after(d: datetime.date, n: int) -> datetime.date:
    """Business-day walk written independently: step by day, count only Mon-Fri."""
    cur, count = d, 0
    while count < n:
        cur = cur + datetime.timedelta(days=1)
        if cur.isoweekday() <= 5:
            count += 1
    return cur


def main() -> None:
    rng = random.Random(SEED)
    sells = []
    for k in range(3):
        price = 10000 + rng.randint(0, 400)
        qty = rng.randint(100, 500)
        sells.append({"owner": P[k + 1], "price": price, "qty": qty, "time": k})
    best = min(sells, key=lambda o: (o["price"], o["time"]))
    limit = best["price"] + rng.randint(0, 200)
    in_qty = rng.randint(1, best["qty"])
    print("resting", [(s["owner"], s["price"], s["qty"]) for s in sorted(sells, key=lambda o: o["price"])])
    print("incoming P1 limit", limit, "qty", in_qty, "best resting", best["owner"], best["price"], best["qty"])
    fill = min(in_qty, best["qty"])
    cons = fill * best["price"]
    print("fill", fill, "at", best["price"], "consideration", cons, "limit >= price", limit >= best["price"])
    td = datetime.date(2026, 10, 28)
    print("trade date", td, weekday_name(td))
    for name, off in [("clearing", 0), ("settlement", 2), ("settlement_lag3", 3)]:
        d = bd_after(td, off)
        print(name, off, d, weekday_name(d))
    print("M2 check: Fri 2026-10-30 +2 bd ->", bd_after(datetime.date(2026, 10, 30), 2), weekday_name(bd_after(datetime.date(2026, 10, 30), 2)))
    print("E3 check: +3 bd from 10-28 ->", bd_after(td, 3))

    batch = []
    for _ in range(20):
        buyer, seller = rng.sample(P, 2)
        price = rng.randint(5000, 20000)
        qty = rng.randint(1, 500)
        batch.append((buyer, seller, price, qty))
    gross = sum(p * q for _, _, p, q in batch)
    net = {x: 0 for x in P}
    for buyer, seller, p, q in batch:
        net[seller] += p * q
        net[buyer] -= p * q
    np_ = sum(-v for v in net.values() if v < 0)
    payers = [x for x in P if net[x] < 0]
    print("gross", gross, "NP", np_, "payers", payers, len(payers), "sum", sum(net.values()))
    print("net", net)
    r = Fraction(np_, gross)
    print("ratio exact", r, float(r))
    print("ratio 8dp", f"{float(r):.8f}", "5dp", f"{float(r):.5f}", "4dp", f"{float(r):.4f}")
    half_up_milli = (2000 * np_ + gross) // (2 * gross)
    print("3dp half-up milli", half_up_milli, f"{half_up_milli // 1000}.{half_up_milli % 1000:03d}")
    p5_gross = Fraction(net["P5"], gross) * 100
    p5_np = Fraction(net["P5"], np_) * 100
    print("P5 pct of gross", float(p5_gross), "P5 pct of NP", float(p5_np))
    print("E2 positives", net["P3"], net["P5"], net["P3"] + net["P5"], "negatives sum", -(net["P1"] + net["P2"] + net["P4"]))
    # Proposition 2.1 bounds
    assert 0 <= np_ <= gross
    assert sum(net.values()) == 0
    # Proposition 2.2 (novation): CCP net cash
    print("CCP net cash", gross - gross)


if __name__ == "__main__":
    main()
