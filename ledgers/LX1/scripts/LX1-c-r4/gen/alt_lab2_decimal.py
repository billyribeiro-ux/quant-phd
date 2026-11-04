"""Alternative correct implementation of lab 2 (independent Decimal arithmetic), must print the expected block."""
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 60
PATH = [Decimal(p) / 100 for p in (100, 99, 98, 96, 95, 93)]
D = Decimal(4000000)
def q(x, places):
    return x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
print("SIMULATED price path, P_0 = 1.00; nominal debt 40000.00 dollars, fixed (A1)")
print("Part A, real debt in dollars by period:")
for t, p in enumerate(PATH):
    cents = q(D / p, 0)
    dollars = cents / 100
    print(f"  t={t} price={q(p, 2)} real debt={dollars:.2f}")
ch = (PATH[0] / PATH[-1] - 1) * 100
print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
print(f"  change: {q(ch, 2)}")
