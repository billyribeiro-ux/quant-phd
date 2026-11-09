"""Round-15 verifier: independent re-derivation of every number on the project page (Decimal, 60 digits).

Usage: python -I rederive_r15.py <checkout_root>. Does not import the lab code."""
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal, localcontext
from pathlib import Path

root = Path(sys.argv[1]).resolve()
Q2 = Decimal("0.01")
Q4 = Decimal("0.0001")
Q6 = Decimal("0.000001")


def r(x, q=Q2):
    return x.quantize(q, rounding=ROUND_HALF_UP)


with localcontext() as ctx:
    ctx.prec = 60
    fall = [Decimal(p) / 100 for p in (100, 97, 94, 91, 88, 85)]
    rise = [Decimal(p) / 100 for p in (100, 103, 106, 109, 112, 115)]
    D1 = Decimal(100000)
    print("LAB1 real debt falling:", [str(r(D1 / p)) for p in fall])
    print("LAB1 real debt rising :", [str(r(D1 / p)) for p in rise])
    print("LAB1 burden falling %:", r(100 * (fall[0] / fall[-1] - 1)), " rising %:", r(100 * (rise[0] / rise[-1] - 1)))
    print("LAB1 part C difference:", r(D1 / fall[-1] - D1 / rise[-1]), " exact:", D1 / fall[-1] - D1 / rise[-1])
    p2 = [Decimal(p) / 100 for p in (100, 99, 98, 96, 95, 93)]
    D2 = Decimal(40000)
    print("LAB2 real debt:", [str(r(D2 / p)) for p in p2], " burden %:", r(100 * (p2[0] / p2[-1] - 1)), " exact:", 100 * (p2[0] / p2[-1] - 1))
    print("LAB2 burden with end-value base %:", r(100 * (D2 / p2[-1] - D2 / p2[0]) / (D2 / p2[-1])))
    print("LAB2 burden ratio inverted %:", r(100 * (p2[-1] / p2[0] - 1)))
    with (root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="") as fh:
        rows = [(row["month"], Decimal(row["GBP"])) for row in csv.DictReader(fh)]
    print("LAB3 months:", len(rows), rows[0][0], rows[-1][0])
    logs = [(m, (v / pv).ln()) for (_, pv), (m, v) in zip(rows, rows[1:])]

    def sd(vals):
        n = len(vals)
        mean = sum(vals) / n
        return (sum((x - mean) ** 2 for x in vals) / (n - 1)).sqrt()

    w1 = [x for _, x in logs]
    w2 = [x for m, x in logs if m >= "2000-01"]
    w3 = [x for m, x in logs if m >= "2025-10"]
    s1, s2, s3 = sd(w1), sd(w2), sd(w3)
    print("LAB3 counts:", len(w1), len(w2), len(w3))
    print("LAB3 exact zeros:", sum(1 for x in w1 if x == 0), sum(1 for x in w2 if x == 0), sum(1 for x in w3 if x == 0))
    print("LAB3 sd percent per month two decimals:", r(100 * s1), r(100 * s2), r(100 * s3))
    print("LAB3 sd percent unrounded (8 dp):", r(100 * s1, Decimal("0.00000001")), r(100 * s2, Decimal("0.00000001")), r(100 * s3, Decimal("0.00000001")))
    print("LAB3 ratio w2/w1 unrounded:", r(s2 / s1, Decimal("0.000000001")), " two decimals:", r(s2 / s1))
    print("LAB3 difference w1-w2 percent unrounded:", r(100 * (s1 - s2), Decimal("0.000000001")), " two decimals:", r(100 * (s1 - s2)))
    big = max(logs, key=lambda it: abs(it[1]))
    print("LAB3 largest by size all of window one:", r(100 * big[1]), big[0], " signed:", 100 * big[1])
    big2 = max([it for it in logs if it[0] >= "2000-01"], key=lambda it: abs(it[1]))
    big3 = max([it for it in logs if it[0] >= "2025-10"], key=lambda it: abs(it[1]))
    print("LAB3 largest w2:", r(100 * big2[1]), big2[0], " largest w3:", r(100 * big3[1]), big3[0])
    print("L4 cross-check sd decimals (6 dp):", r(s1, Q6), r(s2, Q6))
    print("exemplar A 2.47/2.79 =", r(Decimal("2.47") / Decimal("2.79"), Q4), " fell by percent:", r(100 * (1 - Decimal("2.47") / Decimal("2.79")), Q2))
    print("LAB2 burden exact 100*(1/0.93-1) =", r(100 * (Decimal(1) / Decimal("0.93") - 1), Q6))
