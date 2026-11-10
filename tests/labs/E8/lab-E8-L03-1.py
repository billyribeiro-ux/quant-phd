"""Lab 3: Covered Interest Parity (CIP) and the Cross-Currency Basis.

SIMULATED numbers. Standard library only.
Computes the CIP forward rate and the cross-currency basis in basis points.
Sign convention: basis = (usd_rate - implied_usd_rate) * 10,000.
Negative basis indicates dollar funding shortage (synthetic borrowing costs > cash borrowing).
"""

from fractions import Fraction


def compute_cip_forward(
    spot: Fraction,
    usd_rate: Fraction,
    foreign_rate: Fraction,
    tau_usd: Fraction,
    tau_foreign: Fraction,
) -> Fraction:
    """Compute frictionless CIP theoretical forward exchange rate (USD per unit foreign)."""
    num = spot * (Fraction(1, 1) + foreign_rate * tau_foreign)
    den = Fraction(1, 1) + usd_rate * tau_usd
    return num / den


def compute_cross_currency_basis_bp(
    spot: float,
    forward: float,
    usd_rate: float,
    foreign_rate: float,
    tau_usd: float,
    tau_foreign: float,
) -> tuple[float, float]:
    """Compute implied USD rate and cross-currency basis in basis points.

    Convention:
    implied_usd_rate = (1 / tau_usd) * [ (spot / forward) * (1 + foreign_rate * tau_foreign) - 1 ]
    basis_bp = (usd_rate - implied_usd_rate) * 10,000
    """
    if spot <= 0 or forward <= 0 or tau_usd <= 0 or tau_foreign <= 0:
        msg = "Quotes and accrual fractions must be strictly positive"
        raise ValueError(msg)

    foreign_accrual = 1.0 + foreign_rate * tau_foreign
    implied_usd = (1.0 / tau_usd) * ((spot / forward) * foreign_accrual - 1.0)
    basis_bp = (usd_rate - implied_usd) * 10000.0
    return implied_usd, basis_bp


def main() -> None:
    # 3-month tenor (90 days on actual/360)
    tau_usd = Fraction(90, 360)
    tau_eur = Fraction(90, 360)
    tau_jpy = Fraction(90, 360)

    # Base rates: USD 5.0%, EUR 3.0%, JPY -0.1%
    i_usd_frac = Fraction(5, 100)
    i_eur_frac = Fraction(3, 100)
    i_jpy_frac = Fraction(-1, 1000)

    # 1. CIP theoretical parity check (EUR/USD, spot = 1.10)
    s_eur = Fraction(11, 10)
    f_cip_eur = compute_cip_forward(s_eur, i_usd_frac, i_eur_frac, tau_usd, tau_eur)

    implied_cip, basis_cip = compute_cross_currency_basis_bp(
        float(s_eur), float(f_cip_eur), float(i_usd_frac), float(i_eur_frac), float(tau_usd), float(tau_eur)
    )

    # 2. Observed EUR/USD with negative basis (dollar shortage post-2008)
    # Observed forward is lower than CIP forward (synthetic USD borrowing rate is higher than cash rate)
    f_obs_eur = 1.0938
    implied_eur, basis_eur = compute_cross_currency_basis_bp(
        float(s_eur), f_obs_eur, float(i_usd_frac), float(i_eur_frac), float(tau_usd), float(tau_eur)
    )

    # 3. Observed JPY/USD with pronounced negative basis (Japanese institutional dollar demand)
    # Spot quote: 150.0 JPY per USD => Direct quote = 1/150 USD per JPY
    s_jpy = 1.0 / 150.0
    # CIP forward would be (1/150) * (1 - 0.001*0.25)/(1 + 0.05*0.25) ~= 0.0065827
    # Observed forward: 0.0065748 (dollar forward is expensive)
    f_obs_jpy = 0.0065748
    implied_jpy, basis_jpy = compute_cross_currency_basis_bp(
        s_jpy, f_obs_jpy, float(i_usd_frac), float(i_jpy_frac), float(tau_usd), float(tau_jpy)
    )

    print("=== Covered Interest Parity and Basis (SIMULATED) ===")
    print(f"Theoretical CIP Forward (EUR/USD): {float(f_cip_eur):.6f}")
    print(f"Frictionless CIP Basis:            {basis_cip:+.2f} bp (Implied USD: {implied_cip * 100:.3f}%)")
    print(f"\nEUR/USD Observed Forward:          {f_obs_eur:.6f}")
    print(f"EUR/USD Implied USD Rate:          {implied_eur * 100:.3f}% (Cash: {float(i_usd_frac) * 100:.2f}%)")
    print(f"EUR/USD Cross-Currency Basis:      {basis_eur:+.1f} bp")
    print(f"\nJPY/USD Observed Forward:          {f_obs_jpy:.8f} (Spot: {s_jpy:.8f})")
    print(f"JPY/USD Implied USD Rate:          {implied_jpy * 100:.3f}% (Cash: {float(i_usd_frac) * 100:.2f}%)")
    print(f"JPY/USD Cross-Currency Basis:      {basis_jpy:+.1f} bp")

    assert abs(basis_cip) < 1e-9, f"CIP forward must yield zero basis, got {basis_cip}"
    assert basis_eur < 0, f"Observed EUR basis must be negative, got {basis_eur}"
    assert basis_jpy < 0, f"Observed JPY basis must be negative, got {basis_jpy}"


main()
