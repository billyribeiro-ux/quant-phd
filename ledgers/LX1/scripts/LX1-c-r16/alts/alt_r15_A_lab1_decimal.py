"""LX1 project lab 1 (rung 1) alternative correct implementation (verifier round 15): Decimal arithmetic at 60 digits.

Same printed contract as the page: real debt = nominal / price, rounded half up to the cent once at print time;
burden change = 100 * (P_0 / P_5 - 1) rounded half up to two decimals; Part C from unrounded values.
"""
from decimal import ROUND_HALF_UP, Decimal, localcontext

NOMINAL = Decimal(100000)  # dollars, fixed (A1)
PATHS = {
    "falling": ["1.00", "0.97", "0.94", "0.91", "0.88", "0.85"],
    "rising": ["1.00", "1.03", "1.06", "1.09", "1.12", "1.15"],
}


def half_up(value, places):
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def main():
    with localcontext() as ctx:
        ctx.prec = 60
        print("SIMULATED price paths, P_0 = 1.00; nominal debt 100000.00 dollars, fixed (A1)")
        for name, prices in PATHS.items():
            print(f"Part A, path {name}, real debt in dollars by period:")
            for t, p in enumerate(prices):
                price = Decimal(p)
                print(f"  t={t} price={p} real debt={half_up(NOMINAL / price, 2)}")
        print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
        for name, prices in PATHS.items():
            change = 100 * (Decimal(prices[0]) / Decimal(prices[-1]) - 1)
            print(f"  path {name}: {half_up(change, 2)}")
        diff = NOMINAL / Decimal(PATHS["falling"][-1]) - NOMINAL / Decimal(PATHS["rising"][-1])
        print("Part C, period 5, falling path minus rising path, real debt in dollars:")
        print(f"  difference: {half_up(diff, 2)}")


main()
