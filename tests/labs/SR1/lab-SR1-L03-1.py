"""Lab SR1-L03-1: Uninsured Depositor Run Thresholds and Solvency Limits.

Calculates the exact fundamental run threshold theta*(mu, kappa, ell) across a grid
of uninsured deposit shares and asset liquidation recovery rates. Demonstrates that
high uninsured deposit concentration dramatically raises bank run vulnerability,
reducing tolerance for asset mark-to-market declines.
"""

from fractions import Fraction


def main() -> None:
    # Model parameters
    ell = Fraction(2, 10)  # Liquid reserve buffer = 0.20
    kappas = [Fraction(5, 10), Fraction(7, 10), Fraction(9, 10)]
    mus = [Fraction(2, 10), Fraction(4, 10), Fraction(6, 10), Fraction(8, 10), Fraction(9, 10)]

    print(f"Bank Liquid Reserve Buffer ell = {ell} ({float(ell):.2f})")
    print("Run Threshold theta*(mu, kappa, ell) Grid:")
    header = "mu \\ kappa  | " + " | ".join(f"kappa={float(k):.2f}" for k in kappas)
    print(header)
    print("-" * len(header))

    for mu in mus:
        row = []
        for k in kappas:
            if mu <= ell:
                th = Fraction(0, 1)
            else:
                raw = (mu - ell) / (k * (Fraction(1, 1) - ell))
                th = min(Fraction(1, 1), raw)
            row.append(f"{float(th):10.4f}")
        mu_str = f"mu={float(mu):.2f}"
        print(f"{mu_str:11} | " + " | ".join(row))

    print("\nCase Analysis:")
    # Retail bank profile: mu = 0.20 <= ell = 0.20
    print("1. Retail Bank (mu = 0.20): Liquid buffer covers all uninsured deposits. Threshold = 0.0000 (Immune).")
    # Regional bank profile (SVB-like): mu = 0.90, kappa = 0.70
    raw_svb = (Fraction(9, 10) - ell) / (Fraction(7, 10) * (Fraction(1, 1) - ell))
    th_svb = min(Fraction(1, 1), raw_svb)
    print(
        f"2. Regional Bank (mu = 0.90, kappa = 0.70): Run threshold = {th_svb} ({float(th_svb):.4f}). "
        f"Bank suffers a run whenever asset recovery drops below {float(th_svb) * 100:.2f}%."
    )


main()
