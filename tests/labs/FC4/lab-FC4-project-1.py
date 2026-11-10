"""Lab FC4-project-1: Rung 1 worked example: fully solved equity valuation (SIMULATED)."""

from fractions import Fraction


def gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    """Gordon growth perpetuity value D_1 / (r - g)."""
    assert r > g, "Discount rate must exceed perpetual growth rate"
    return d1 / (r - g)


def ddm_value(dividends: list[Fraction], r: Fraction, g: Fraction) -> Fraction:
    """Multistage dividend discount model value with terminal Gordon perpetuity."""
    factor = Fraction(1) + r
    pv_explicit = Fraction(0)
    disc = Fraction(1)
    for d in dividends:
        disc *= factor
        pv_explicit += d / disc

    n = len(dividends)
    terminal_d = dividends[-1] * (Fraction(1) + g)
    tv = gordon_value(terminal_d, r, g)
    pv_tv = tv / (factor**n)
    return pv_explicit + pv_tv


def fcfe_value_per_share(fcfe: list[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    """FCFE equity value per share with terminal Gordon perpetuity."""
    factor = Fraction(1) + r
    pv_explicit = Fraction(0)
    disc = Fraction(1)
    for f in fcfe:
        disc *= factor
        pv_explicit += f / disc

    n = len(fcfe)
    terminal_f = fcfe[-1] * (Fraction(1) + g)
    tv = gordon_value(terminal_f, r, g)
    pv_tv = tv / (factor**n)
    return (pv_explicit + pv_tv) / shares


def residual_income_value(
    book_value_0: Fraction, earnings: list[Fraction], dividends: list[Fraction], r: Fraction
) -> Fraction:
    """Residual income valuation under clean surplus: V_0 = B_0 + sum(RI_t / (1+r)^t)."""
    factor = Fraction(1) + r
    pv_ri = Fraction(0)
    b_prev = book_value_0
    disc = Fraction(1)

    for ni, d in zip(earnings, dividends, strict=True):
        ri = ni - r * b_prev
        disc *= factor
        pv_ri += ri / disc
        b_prev = b_prev + ni - d

    return book_value_0 + pv_ri


def scenario_price_target_cents(scenarios: list[tuple[Fraction, int]]) -> int:
    """Scenario-weighted target in integer cents rounded half-up: floor(E[V] + 1/2)."""
    tot_p = sum(p for p, _ in scenarios)
    assert tot_p == Fraction(1), "Probabilities must sum to 1"
    ev = sum(p * v for p, v in scenarios)
    num = 2 * ev.numerator + ev.denominator
    den = 2 * ev.denominator
    return num // den


def main() -> None:
    # Illustrative SIMULATED company fundamentals
    # 5-year explicit horizon
    r = Fraction(10, 100)  # Cost of equity r = 10%
    g = Fraction(3, 100)  # Perpetual growth g = 3%
    b0 = Fraction(2500, 100)  # Initial book value B_0 = $25.00 per share
    shares = Fraction(5000)  # 5,000 shares (or scaling factor)

    dividends = [Fraction(120, 100), Fraction(135, 100), Fraction(150, 100), Fraction(165, 100), Fraction(180, 100)]
    earnings = [Fraction(250, 100), Fraction(280, 100), Fraction(310, 100), Fraction(340, 100), Fraction(375, 100)]
    fcfe = [Fraction(140, 100), Fraction(160, 100), Fraction(180, 100), Fraction(205, 100), Fraction(230, 100)]
    # Scale FCFE to total equity for shares count
    fcfe_total = [f * shares for f in fcfe]

    # Scenarios for price target (Prob, Price in Cents)
    scenarios = [
        (Fraction(25, 100), 2200),  # Bear: 25% @ $22.00
        (Fraction(50, 100), 3100),  # Base: 50% @ $31.00
        (Fraction(25, 100), 4400),  # Bull: 25% @ $44.00
    ]

    # Execute valuation models
    val_gordon = gordon_value(dividends[0], r, g)
    val_ddm = ddm_value(dividends, r, g)
    val_fcfe_share = fcfe_value_per_share(fcfe_total, shares, r, g)
    val_ri = residual_income_value(b0, earnings, dividends, r)
    target_cents = scenario_price_target_cents(scenarios)

    print("SIMULATED Initiation-of-Coverage Valuation Model Output (Rung 1 Worked Example)")
    print(f"Cost of Equity r = {float(r):.2%}, Terminal Growth g = {float(g):.2%}")
    print("-" * 75)
    print(f"{'Valuation Model':<36} {'Per Share ($)':>16} {'Exact Fraction':>20}")
    print("-" * 75)
    print(f"{'1. Pure Gordon Growth (D1/(r-g))':<36} ${float(val_gordon):15.2f} {val_gordon!s:>20}")
    print(f"{'2. Multistage DDM (5-yr + TV)':<36} ${float(val_ddm):15.2f} {val_ddm!s:>20}")
    print(f"{'3. FCFE Model (5-yr + TV)':<36} ${float(val_fcfe_share):15.2f} {val_fcfe_share!s:>20}")
    print(f"{'4. Residual Income (5-yr clean roll)':<36} ${float(val_ri):15.2f} {val_ri!s:>20}")
    print(f"{'5. Scenario Target (Bull/Base/Bear)':<36} ${target_cents / 100:15.2f} {f'{target_cents} cents':>20}")
    print("-" * 75)
    print("Worked example completed successfully.")


main()
