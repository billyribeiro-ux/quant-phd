"""Lab FC4-project-3: Rung 3 autograder verification for seed 0 (self-contained)."""

from fractions import Fraction


def gordon_val(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    return d1 / (r - g)


def ddm_val(dividends: tuple[Fraction, ...], r: Fraction, g: Fraction) -> Fraction:
    factor = Fraction(1) + r
    pv = Fraction(0)
    disc = Fraction(1)
    for d in dividends:
        disc *= factor
        pv += d / disc
    n = len(dividends)
    tv = (dividends[-1] * (Fraction(1) + g)) / (r - g)
    return pv + tv / (factor**n)


def fcfe_val(fcfe: tuple[Fraction, ...], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    factor = Fraction(1) + r
    pv = Fraction(0)
    disc = Fraction(1)
    for f in fcfe:
        disc *= factor
        pv += f / disc
    n = len(fcfe)
    tv = (fcfe[-1] * (Fraction(1) + g)) / (r - g)
    return (pv + tv / (factor**n)) / shares


def ri_val(b0: Fraction, earnings: tuple[Fraction, ...], dividends: tuple[Fraction, ...], r: Fraction) -> Fraction:
    factor = Fraction(1) + r
    disc = Fraction(1)
    pv_ri = Fraction(0)
    b = b0
    for ni, d in zip(earnings, dividends, strict=True):
        ri = ni - r * b
        disc *= factor
        pv_ri += ri / disc
        b = b + ni - d
    return b0 + pv_ri


def target_cents(scenarios: tuple[tuple[Fraction, int], ...]) -> int:
    ev = sum(p * v for p, v in scenarios)
    num = 2 * ev.numerator + ev.denominator
    den = 2 * ev.denominator
    return num // den


def main() -> None:
    # Seed 0 parameters (SIMULATED)
    r = Fraction(1, 10)  # 10%
    g = Fraction(1, 25)  # 4%
    d1 = Fraction(73, 20)  # $3.65
    dividends = (Fraction(11, 10), Fraction(131, 100), Fraction(3, 2), Fraction(161, 100), Fraction(83, 50))
    earnings = (Fraction(91, 25), Fraction(-7, 25), Fraction(209, 50), Fraction(231, 100), Fraction(189, 50))
    fcfe = (Fraction(-18, 25), Fraction(56, 25), Fraction(151, 100), Fraction(32, 25), Fraction(99, 25))
    b0 = Fraction(1263, 50)
    shares = Fraction(35902)
    scenarios = (
        (Fraction(1, 5), 2568),
        (Fraction(9, 20), 3703),
        (Fraction(7, 20), 4605),
    )

    gordon = gordon_val(d1, r, g)
    ddm = ddm_val(dividends, r, g)
    fcfe_sh = fcfe_val(fcfe, shares, r, g)
    ri = ri_val(b0, earnings, dividends, r)
    target = target_cents(scenarios)

    print("Rung 3 Seed-0 Independent Verification (SIMULATED)")
    print("-" * 75)
    print(f"{'Valuation Function':<35} {'Result':>16} {'Exact Fraction':>22}")
    print("-" * 75)
    print(f"{'gordon_value':<35} ${float(gordon):15.2f} {gordon!s:>22}")
    print(f"{'ddm_value':<35} ${float(ddm):15.2f} {ddm!s:>22}")
    print(f"{'fcfe_value_per_share':<35} ${float(fcfe_sh):15.6f} {fcfe_sh!s:>22}")
    print(f"{'residual_income_value':<35} ${float(ri):15.2f} {ri!s:>22}")
    print(f"{'scenario_price_target_cents':<35} {target:15d} {'3792 cents':>22}")
    print("-" * 75)
    print("Seed 0 reference check: all 5 functions evaluated successfully.")


main()
