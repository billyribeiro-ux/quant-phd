"""Rung 1 worked example: price and yield sensitivities of one SIMULATED bond, analytic and by central difference.

The bond is SIMULATED, not market data: face value 1000000 cents (10000.00), an annual coupon of 5.00 %, ten annual
payments, and a yield of 4.00 % compounded once a year. The program prints the unrounded price in cents, the rounded
price, the first and second derivatives in the yield by their cash-flow formulas and by central differences with
step 1e-5, the differences between each formula and its central difference, and the duration -P'/P in years.
Standard library only.
"""

Flow = tuple[int, float]


def price_cents(flows: list[Flow], y: float) -> float:
    """The unrounded price in cents at the annual yield y: the sum of cash_t / (1 + y)**t over the flows."""
    v = 1 / (1 + y)
    return sum(cash * v**t for t, cash in flows)


def main() -> None:
    face_cents = 1_000_000  # SIMULATED face value, 10000.00 in cents
    coupon = face_cents * 0.05  # cents paid at the end of each year
    years = 10
    y = 0.04
    # Step 1. The cash flow of year t: the coupon, and the face value added in the last year.
    flows = [(t, coupon + (face_cents if t == years else 0)) for t in range(1, years + 1)]
    # Step 2. The discount factor of year t is v**t with v = 1 / (1 + y); the price is the sum of the discounted flows.
    price = price_cents(flows, y)
    v = 1 / (1 + y)
    # Step 3. The derivative of v**t in y is -t * v**(t+1), so dP/dy = -sum t * cash * v**(t+1). The second derivative
    # of v**t is t(t+1) * v**(t+2), so d2P/dy2 = sum t(t+1) * cash * v**(t+2).
    first = -sum(t * cash * v ** (t + 1) for t, cash in flows)
    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)
    # Step 4. The same two derivatives by central differences of the unrounded price, with step h = 1e-5.
    h = 1e-5
    up, down = price_cents(flows, y + h), price_cents(flows, y - h)
    first_numeric = (up - down) / (2 * h)
    second_numeric = (up - 2 * price + down) / (h * h)
    print("unrounded price (cents):", f"{price:.4f}")
    print("rounded price (cents, half to even):", round(price))
    print("dP/dy analytic (cents per unit yield):", f"{first:.4f}")
    print("dP/dy central difference:", f"{first_numeric:.4f}")
    print("difference:", f"{abs(first - first_numeric):.2e}")
    print("d2P/dy2 analytic (cents per squared unit yield):", f"{second:.4f}")
    print("d2P/dy2 central difference:", f"{second_numeric:.4f}")
    print("difference:", f"{abs(second - second_numeric):.2e}")
    print("duration -P'/P (years):", f"{-first / price:.6f}")


main()
