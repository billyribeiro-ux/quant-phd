"""CF6 Lesson 1 Inline Lab 1: Rock Winner's Curse Underpricing Simulation.

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
"""

from __future__ import annotations


def solve_rock_equilibrium(
    v_l: float,
    v_h: float,
    p: float,
    s_shares: int,
    informed_dem: int,
    uninformed_b: float,
) -> tuple[float, float, float]:
    """Compute Rock equilibrium price, rationing probability, and underpricing."""
    e_v = (1.0 - p) * v_l + p * v_h

    def expected_profit(p_test: float) -> float:
        d_u = uninformed_b / p_test
        alloc_l = min(d_u, float(s_shares))
        tot_dem_h = d_u + float(informed_dem)
        alloc_h = (float(s_shares) / tot_dem_h) * d_u if tot_dem_h > float(s_shares) else d_u
        return (1.0 - p) * alloc_l * (v_l - p_test) + p * alloc_h * (v_h - p_test)

    lo, hi = v_l, e_v
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if expected_profit(mid) > 0.0:
            lo = mid
        else:
            hi = mid

    p_star = 0.5 * (lo + hi)
    d_u_star = uninformed_b / p_star
    alpha_h = min(1.0, float(s_shares) / (d_u_star + float(informed_dem)))
    underpricing = (e_v - p_star) / p_star
    return p_star, alpha_h, underpricing


def main() -> None:
    # Offering parameters
    v_l = 12.00  # Lemon state value ($)
    v_h = 28.00  # Peach state value ($)
    prob_h = 0.60  # Probability of good state
    s_shares = 2_000_000  # Total shares offered
    informed_dem = 2_500_000  # Informed demand in high state
    uninformed_b = 50_000_000.0  # Uninformed capital budget ($)

    e_v = (1.0 - prob_h) * v_l + prob_h * v_h
    print(f"Unconditional Expected Value E[v]: ${e_v:.2f}")

    # Case 1: Naive pricing at unconditional expected value P0 = E[v]
    p_naive = e_v
    d_u_naive = uninformed_b / p_naive
    alloc_l_naive = min(d_u_naive, float(s_shares))
    alpha_h_naive = min(1.0, float(s_shares) / (d_u_naive + float(informed_dem)))
    alloc_h_naive = alpha_h_naive * d_u_naive

    exp_profit_naive = (1.0 - prob_h) * alloc_l_naive * (v_l - p_naive) + prob_h * alloc_h_naive * (v_h - p_naive)
    print("--- Case 1: Naive Pricing (P0 = E[v] = $21.60) ---")
    print(f"Offer Price:                     ${p_naive:.2f}")
    print(f"Uninformed Low State Alloc:      {alloc_l_naive:,.0f} shares (full allocation)")
    print(f"Uninformed High State Alloc:     {alloc_h_naive:,.0f} shares (rationed to {alpha_h_naive:.1%})")
    print(f"Uninformed Expected Net Profit:  ${exp_profit_naive:,.2f} (WINNER'S CURSE PENALTY)")

    # Case 2: Rock (1986) Equilibrium Pricing
    p_star, alpha_h, up = solve_rock_equilibrium(v_l, v_h, prob_h, s_shares, informed_dem, uninformed_b)
    d_u_star = uninformed_b / p_star
    alloc_l_star = min(d_u_star, float(s_shares))
    alloc_h_star = alpha_h * d_u_star
    exp_profit_star = (1.0 - prob_h) * alloc_l_star * (v_l - p_star) + prob_h * alloc_h_star * (v_h - p_star)
    if abs(exp_profit_star) < 1e-4:
        exp_profit_star = 0.0

    print("--- Case 2: Rock (1986) Equilibrium Pricing ---")
    print(f"Equilibrium Offer Price P*:      ${p_star:.2f}")
    print(f"Equilibrium Underpricing:        {up * 100:.2f}%")
    print(f"High State Rationing alpha_H:    {alpha_h:.4f}")
    print(f"Uninformed Expected Net Profit:  ${exp_profit_star:,.2f} (Zero-profit equilibrium)")


main()
