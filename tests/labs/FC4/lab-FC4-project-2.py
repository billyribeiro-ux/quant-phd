"""Lab FC4-project-2: Rung 2 completion problem: completed solution twin (SIMULATED)."""

from fractions import Fraction


def compute_ddm(dividends: list[Fraction], r: Fraction, g: Fraction) -> Fraction:
    factor = Fraction(1) + r
    pv = Fraction(0)
    disc = Fraction(1)
    for d in dividends:
        disc *= factor
        pv += d / disc

    n = len(dividends)
    terminal_d = dividends[-1] * (Fraction(1) + g)
    tv = terminal_d / (r - g)
    return pv + tv / (factor**n)


def compute_fcfe_share(fcfe: list[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    factor = Fraction(1) + r
    pv = Fraction(0)
    disc = Fraction(1)
    for f in fcfe:
        disc *= factor
        pv += f / disc

    n = len(fcfe)
    terminal_fcfe = fcfe[-1] * (Fraction(1) + g)
    tv = terminal_fcfe / (r - g)
    return (pv + tv / (factor**n)) / shares


def compute_target_cents(scenarios: list[tuple[Fraction, int]]) -> int:
    ev = sum(p * v for p, v in scenarios)
    num = 2 * ev.numerator + ev.denominator
    den = 2 * ev.denominator
    return num // den


def main() -> None:
    r = Fraction(10, 100)
    g = Fraction(3, 100)
    dividends = [Fraction(120, 100), Fraction(140, 100), Fraction(160, 100)]
    fcfe_total = [Fraction(6000), Fraction(7000), Fraction(8000)]
    shares = Fraction(5000)
    scenarios = [(Fraction(1, 4), 2000), (Fraction(1, 2), 3000), (Fraction(1, 4), 4000)]

    val_ddm = compute_ddm(dividends, r, g)
    val_fcfe = compute_fcfe_share(fcfe_total, shares, r, g)
    target = compute_target_cents(scenarios)

    print("Rung 2 Completion Problem Check (SIMULATED)")
    print(f"1. DDM Value per share:     ${float(val_ddm):.2f} ({val_ddm})")
    print(f"2. FCFE Value per share:    ${float(val_fcfe):.2f} ({val_fcfe})")
    print(f"3. Scenario Price Target:   ${target / 100:.2f} ({target} cents)")
    print("Completion verification: all three outputs evaluate cleanly.")


main()
