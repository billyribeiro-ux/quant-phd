"""Lab 2: Sovereign default and willingness to pay (Eaton & Gersovitz 1981).

SIMULATED discrete-state endowment economy. Standard library only.
Computes default thresholds, endogenous bond price schedule q(b),
and the sovereign Debt Laffer curve with borrowing capacity limits.
"""

from __future__ import annotations


def default_threshold(debt_issued: float, sanction_penalty_fraction: float) -> float:
    """Compute output threshold y* below which default is optimal.

    Under linear default penalty y_def = y * (1 - delta):
    Repayment utility u(y - b) vs Default utility u(y * (1 - delta)).
    For any strictly increasing utility function u:
    Default iff y * (1 - delta) > y - b <=> delta * y < b <=> y < b / delta.
    """
    if sanction_penalty_fraction <= 0.0 or sanction_penalty_fraction > 1.0:
        msg = f"Sanction penalty fraction must be in (0, 1], got {sanction_penalty_fraction}"
        raise ValueError(msg)
    return debt_issued / sanction_penalty_fraction


def default_probability(
    debt_issued: float,
    states: list[float],
    probabilities: list[float],
    sanction_penalty_fraction: float,
) -> float:
    """Compute probability of sovereign default given debt issuance b'."""
    y_star = default_threshold(debt_issued, sanction_penalty_fraction)
    prob_default = sum(p for y, p in zip(states, probabilities, strict=True) if y < y_star)
    return prob_default


def bond_price(
    debt_issued: float,
    states: list[float],
    probabilities: list[float],
    sanction_penalty_fraction: float,
    risk_free_rate: float,
) -> float:
    """Compute competitive bond price schedule q(b') under risk neutrality.

    q(b') = (1 - p(b')) / (1 + r*)
    """
    p_def = default_probability(debt_issued, states, probabilities, sanction_penalty_fraction)
    return (1.0 - p_def) / (1.0 + risk_free_rate)


def main() -> None:
    # Endowment distribution: 10 discrete output states from 70 to 130
    states = [70.0, 76.67, 83.33, 90.0, 96.67, 103.33, 110.0, 116.67, 123.33, 130.0]
    n_states = len(states)
    probabilities = [1.0 / n_states] * n_states  # uniform discrete distribution

    delta = 0.20  # 20% output penalty upon default
    r_star = 0.04  # 4% risk-free world interest rate

    debt_levels = [0.0, 10.0, 15.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0]

    prices: list[float] = []
    revenues: list[float] = []
    probs: list[float] = []

    for b in debt_levels:
        p_def = default_probability(b, states, probabilities, delta)
        q = bond_price(b, states, probabilities, delta, r_star)
        rev = q * b
        probs.append(p_def)
        prices.append(q)
        revenues.append(rev)

    # Find peak of Debt Laffer curve
    max_rev = max(revenues)
    max_idx = revenues.index(max_rev)
    b_star_laffer = debt_levels[max_idx]

    print("=== Sovereign Default Schedule & Debt Laffer Curve ===")
    print(f"World Risk-Free Rate r*:        {r_star:.4f}")
    print(f"Sanction Penalty Fraction delta: {delta:.4f}")
    print(f"Endowment Support Range:         [{states[0]:.2f}, {states[-1]:.2f}]")
    print("\nDebt Issued | Default Prob | Bond Price q(b) | Total Revenue q*b")
    for b, p, q, rev in zip(debt_levels, probs, prices, revenues, strict=True):
        print(f"  {b:6.2f}    |    {p:6.4f}    |     {q:6.4f}    |    {rev:6.4f}")

    print("\n=== Debt Laffer Peak Analysis ===")
    print(f"Maximum Borrowing Revenue:       {max_rev:.4f}")
    print(f"Revenue-Maximizing Debt Level:   {b_star_laffer:.2f}")
    print(f"Default Risk at Laffer Peak:     {probs[max_idx]:.4f}")
    print(f"Bond Price at Laffer Peak:       {prices[max_idx]:.4f}")

    # Verify Laffer curve properties: non-monotonic revenue
    assert revenues[-1] < max_rev, "Revenue beyond peak must be lower than peak (Debt Laffer property)"
    assert prices[0] > prices[-1], "Bond price must decrease as default risk rises"


main()
