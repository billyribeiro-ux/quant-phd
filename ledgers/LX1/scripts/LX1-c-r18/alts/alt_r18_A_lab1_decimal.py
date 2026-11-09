"""Alternative correct implementation (verifier, round 18): project lab 1 (rung 1, worked example) with Decimal arithmetic at 40 digits, one quantize at print time, ROUND_HALF_UP.

SIMULATED. Same two illustrative paths as the page; the output must equal the expected block.
"""
from decimal import ROUND_HALF_UP, Decimal, getcontext

getcontext().prec = 40
CENT = Decimal("0.01")
DEBT_DOLLARS = Decimal("100000.00")
PATHS = {
    "falling": [Decimal(p) / 100 for p in (100, 97, 94, 91, 88, 85)],
    "rising": [Decimal(p) / 100 for p in (100, 103, 106, 109, 112, 115)],
}


def dollars(x: Decimal) -> Decimal:
    return x.quantize(CENT, rounding=ROUND_HALF_UP)


print("SIMULATED price paths, P_0 = 1.00; nominal debt 100000.00 dollars, fixed (A1)")
for name, path in PATHS.items():
    print(f"Part A, path {name}, real debt in dollars by period:")
    for t, price in enumerate(path):
        print(f"  t={t} price={dollars(price)} real debt={dollars(DEBT_DOLLARS / price)}")
print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
for name, path in PATHS.items():
    print(f"  path {name}: {dollars(100 * (path[0] / path[-1] - 1))}")
print("Part C, period 5, falling path minus rising path, real debt in dollars:")
print(f"  difference: {dollars(DEBT_DOLLARS / PATHS['falling'][-1] - DEBT_DOLLARS / PATHS['rising'][-1])}")
