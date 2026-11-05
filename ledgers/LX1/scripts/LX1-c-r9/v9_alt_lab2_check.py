"""Alternative correct lab 2 (verifier round 9): completed solution using the float ratio form of the burden,
100 * (start / end - 1), and Decimal half-up printing. Must print the lab 2 expected block exactly."""
from decimal import Decimal, ROUND_HALF_UP

def q(x, p):
    return str(Decimal(repr(x)).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP))

NOMINAL = 40000.0
PATH = [1.00, 0.99, 0.98, 0.96, 0.95, 0.93]
print("SIMULATED price path, P_0 = 1.00; nominal debt 40000.00 dollars, fixed (A1)")
print("Part A, real debt in dollars by period:")
for t, p in enumerate(PATH):
    print(f"  t={t} price={q(p, 2)} real debt={q(NOMINAL / p, 2)}")
print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
print(f"  change: {q(100 * (PATH[0] / PATH[-1] - 1), 2)}")
