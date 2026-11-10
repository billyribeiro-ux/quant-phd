"""Lab 3: Currency crises: First-generation timing and second-generation escape clauses.

SIMULATED crisis models. Standard library only.
Verifies Krugman (1979) speculative attack timing and reserve run,
and Obstfeld (1996) second-generation multiple equilibria zones.
"""

from __future__ import annotations


def krugman_attack_time(
    log_peg: float,
    initial_log_credit: float,
    credit_growth_rate: float,
    interest_semi_elasticity: float,
) -> float:
    """Compute exact time T of speculative attack under Krugman (1979).

    Shadow exchange rate: s_tilde(t) = d_0 + mu * t + alpha * mu
    Attack occurs when s_tilde(T) = s_bar:
    T = (s_bar - d_0 - alpha * mu) / mu
    """
    if credit_growth_rate <= 0.0:
        msg = f"Credit growth rate must be positive: {credit_growth_rate}"
        raise ValueError(msg)
    t_attack = (log_peg - initial_log_credit - interest_semi_elasticity * credit_growth_rate) / credit_growth_rate
    if t_attack < 0.0:
        msg = f"Initial credit already exceeds speculative threshold: T={t_attack:.4f}"
        raise ValueError(msg)
    return t_attack


def shadow_exchange_rate(
    t: float,
    initial_log_credit: float,
    credit_growth_rate: float,
    interest_semi_elasticity: float,
) -> float:
    """Compute shadow exchange rate at time t."""
    return initial_log_credit + credit_growth_rate * t + interest_semi_elasticity * credit_growth_rate


def obstfeld_defense_cost(
    fundamental_shock: float,
    attack_fraction: float,
    sensitivity: float,
) -> float:
    """Compute government economic loss from defending the peg under Obstfeld (1996).

    Cost = (theta + sensitivity * pi_e)^2
    where theta is the fundamental unemployment shock and pi_e is attack fraction.
    """
    return (fundamental_shock + sensitivity * attack_fraction) ** 2


def obstfeld_zones(
    realign_fixed_cost: float,
    sensitivity: float,
) -> tuple[float, float]:
    """Compute lower (theta_L) and upper (theta_H) fundamental thresholds for multiple equilibria.

    Devaluation occurs if Cost_defense > realign_fixed_cost.
    When no one attacks (pi_e = 0): Cost = theta^2. Devalues if theta > sqrt(C) => theta_H = sqrt(C).
    When everyone attacks (pi_e = 1): Cost = (theta + sensitivity)^2.
    Defends if (theta + sensitivity) < sqrt(C) => theta_L = sqrt(C) - sensitivity.
    Zone [theta_L, theta_H] exhibits self-fulfilling runs.
    """
    c_sqrt = realign_fixed_cost**0.5
    theta_h = c_sqrt
    theta_l = max(0.0, c_sqrt - sensitivity)
    return theta_l, theta_h


def main() -> None:
    # 1. Krugman (1979) parameters
    s_bar = 2.0  # Log peg
    d0 = 1.0  # Initial log domestic credit
    mu = 0.10  # Credit growth rate per year (10%)
    alpha = 2.0  # Money demand semi-elasticity

    t_collapse = krugman_attack_time(s_bar, d0, mu, alpha)
    s_shadow_0 = shadow_exchange_rate(0.0, d0, mu, alpha)
    s_shadow_t = shadow_exchange_rate(t_collapse, d0, mu, alpha)

    # 2. Obstfeld (1996) parameters
    fixed_cost_c = 16.0  # Cost of devaluation C (sqrt(C) = 4.0)
    beta_attack = 1.5  # Speculative feedback parameter

    theta_l, theta_h = obstfeld_zones(fixed_cost_c, beta_attack)

    # Evaluate 3 representative fundamentals
    theta_sound = 2.0  # Sound: theta < theta_L
    theta_vulnerable = 3.0  # Vulnerable: theta_L <= theta <= theta_H
    theta_hopeless = 4.5  # Hopeless: theta > theta_H

    cost_sound_no_attack = obstfeld_defense_cost(theta_sound, 0.0, beta_attack)
    cost_sound_attack = obstfeld_defense_cost(theta_sound, 1.0, beta_attack)

    cost_vuln_no_attack = obstfeld_defense_cost(theta_vulnerable, 0.0, beta_attack)
    cost_vuln_attack = obstfeld_defense_cost(theta_vulnerable, 1.0, beta_attack)

    cost_hope_no_attack = obstfeld_defense_cost(theta_hopeless, 0.0, beta_attack)

    print("=== Krugman (1979) First-Generation Attack Timing ===")
    print(f"Log Exchange Rate Peg s_bar:     {s_bar:.4f}")
    print(f"Initial Log Credit d0:           {d0:.4f}")
    print(f"Credit Growth Rate mu:           {mu:.4f}")
    print(f"Money Semi-Elasticity alpha:     {alpha:.4f}")
    print(f"Shadow Exchange Rate at t=0:     {s_shadow_0:.4f}")
    print(f"Exact Speculative Attack Time T: {t_collapse:.4f} years")
    print(f"Shadow Exchange Rate at Attack:  {s_shadow_t:.4f}")

    print("\n=== Obstfeld (1996) Second-Generation Multiple Equilibria ===")
    print(f"Fixed Cost of Devaluation C:     {fixed_cost_c:.4f}")
    print(f"Attack Sensitivity Parameter:    {beta_attack:.4f}")
    print(f"Sound Threshold theta_L:         {theta_l:.4f}")
    print(f"Hopeless Threshold theta_H:      {theta_h:.4f}")
    print(f"Vulnerable Intermediate Window:  [{theta_l:.4f}, {theta_h:.4f}]")
    print(f"Sound State (theta=2.0) Defense Cost (No Attack):    {cost_sound_no_attack:.4f} (Defends)")
    print(f"Sound State (theta=2.0) Defense Cost (Attack):       {cost_sound_attack:.4f} (Defends)")
    print(f"Vulnerable State (theta=3.0) Defense Cost (No Attack): {cost_vuln_no_attack:.4f} (Defends)")
    print(f"Vulnerable State (theta=3.0) Defense Cost (Attack):    {cost_vuln_attack:.4f} (Devalues)")
    print(f"Hopeless State (theta=4.5) Defense Cost (No Attack):   {cost_hope_no_attack:.4f} (Devalues)")

    assert abs(s_shadow_t - s_bar) < 1e-9, "Shadow exchange rate must equal peg at attack time T"
    assert t_collapse == 8.0, "Krugman attack time should be exactly (2.0 - 1.0 - 0.2) / 0.1 = 8.0 years"
    assert theta_l == 2.5 and theta_h == 4.0, "Obstfeld thresholds must match sqrt(16) - 1.5 = 2.5 and 4.0"
    assert cost_sound_attack < fixed_cost_c, "In sound state, defense cost is below C even under attack"
    assert cost_hope_no_attack > fixed_cost_c, "In hopeless state, defense cost exceeds C even without attack"
    assert cost_vuln_no_attack < fixed_cost_c < cost_vuln_attack, (
        "In vulnerable state, cost must be below C without attack and above C with attack"
    )


main()
