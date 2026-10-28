"""Rung 2 completion: the worked example, with its two blanks filled in."""

from fractions import Fraction


def half_away(x: Fraction) -> int:
    """The nearest whole cent of an exact amount; an exact half goes away from zero."""
    magnitude = abs(x)
    whole = (2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator)
    return whole if x >= 0 else -whole


def main() -> None:
    face_cents = 100_000  # SIMULATED face of 1,000.00, not market data
    coupon_bps = 500  # the coupon in each period, in basis points of face: 5.00 % of face
    periods = 3
    yield_bps = 400  # the per-period yield, in basis points: 4.00 % per period
    # Step 1. The coupon is face * coupon_bps / 10000, rounded once to the nearest cent, a half going away from zero.
    coupon = half_away(Fraction(face_cents * coupon_bps, 10_000))
    # Step 2. Periods run from 1 to periods. Every period pays the coupon; the last period also pays the face.
    events = [(t, coupon) for t in range(1, periods + 1)]
    events[-1] = (periods, events[-1][1] + face_cents)
    print("bond events (period, cents):", events)
    # Step 3. Each event is discounted by (1 + y) ** -t, where y = yield_bps / 10000 is the per-period yield.
    # The sum is kept exact as a Fraction; nothing is rounded yet.
    y = Fraction(yield_bps, 10_000)
    exact_price = sum((Fraction(amount) / (1 + y) ** period for period, amount in events), Fraction(0))
    print("exact present value (cents):", f"{float(exact_price):.6f}")
    # Step 4. The price is rounded once, at the end, to the nearest cent. Rounding each term first is not the rule.
    print("bond price (cents):", half_away(exact_price))
    # Step 5. A trade: buy 10 units at 9850 cents per unit, settling in period 2. The buyer pays cash, so the amount is
    # negative in the holder's terms; the trade has one settlement event and no other cash flow.
    quantity, price_cents, side, settlement_day = 10, 9_850, 1, 2
    trade_event = (settlement_day, -side * quantity * price_cents)
    print("trade event (period, cents):", trade_event)


main()
