"""LX1 project lab 2 (rung 2, completion problem) alternative correct implementation (verifier round 15): Decimal arithmetic.

Same printed contract as the page: real debt = nominal / price (half up to the cent at print time); burden change
= 100 * (P_0 / P_5 - 1) rounded half up to two decimals, from unrounded values.
"""
from decimal import ROUND_HALF_UP, Decimal, localcontext

NOMINAL = Decimal(40000)  # dollars, fixed (A1)
PRICES = ["1.00", "0.99", "0.98", "0.96", "0.95", "0.93"]


def half_up(value, places):
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def main():
    with localcontext() as ctx:
        ctx.prec = 50
        print("SIMULATED price path, P_0 = 1.00; nominal debt 40000.00 dollars, fixed (A1)")
        print("Part A, real debt in dollars by period:")
        for t, p in enumerate(PRICES):
            print(f"  t={t} price={p} real debt={half_up(NOMINAL / Decimal(p), 2)}")
        change = 100 * (Decimal(PRICES[0]) / Decimal(PRICES[-1]) - 1)
        print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
        print(f"  change: {half_up(change, 2)}")


main()
