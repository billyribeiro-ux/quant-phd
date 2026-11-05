"""Alternative correct labs 1 and 2 (verifier round 9): float arithmetic and Decimal half-up printing instead of
Fraction, burden change as 100 * (P0 / P5 - 1) in floats. Both must print the page expected blocks exactly."""
from decimal import Decimal, ROUND_HALF_UP

def q(x, p):
    return str(Decimal(repr(x)).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP))

NOMINAL = 100000.0
paths = {"falling": [1.00, 0.97, 0.94, 0.91, 0.88, 0.85], "rising": [1.00, 1.03, 1.06, 1.09, 1.12, 1.15]}
print("SIMULATED price paths, P_0 = 1.00; nominal debt 100000.00 dollars, fixed (A1)")
for name, path in paths.items():
    print(f"Part A, path {name}, real debt in dollars by period:")
    for t, p in enumerate(path):
        print(f"  t={t} price={q(p, 2)} real debt={q(NOMINAL / p, 2)}")
print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
for name, path in paths.items():
    print(f"  path {name}: {q(100 * (path[0] / path[-1] - 1), 2)}")
print("Part C, period 5, falling path minus rising path, real debt in dollars:")
print(f"  difference: {q(NOMINAL / paths['falling'][-1] - NOMINAL / paths['rising'][-1], 2)}")
