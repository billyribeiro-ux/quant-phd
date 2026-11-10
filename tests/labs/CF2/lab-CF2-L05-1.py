"""CF2 lab L05-1: The interest tax shield and MM with corporate taxes.

Model: Exact closed-form capital structure calculations with corporate income taxes.
Uses fractions.Fraction for exact rational calculations.
Demonstrates:
  1. Annual tax shield equals tau_c * r_D * D.
  2. PV of permanent tax shield discounted at r_D equals exactly tau_c * D.
  3. Levered value V_L = V_U + tau_c * D.
  4. Cost of equity r_E = r_U + (1 - tau_c) * (r_U - r_D) * (D / E).
  5. WACC declines monotonically with leverage as r_WACC = r_U * (1 - tau_c * D / V_L).
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    print("CF2 Lab L05-1: Interest Tax Shield and MM with Corporate Taxes")
    print("-------------------------------------------------------------")

    ebit = Fraction(10_000_000, 1)  # $10M perpetual EBIT
    tau_c = Fraction(25, 100)  # 25% corporate tax rate
    r_u = Fraction(10, 100)  # 10% unlevered cost of capital
    r_d = Fraction(5, 100)  # 5% pre-tax cost of debt

    # Unlevered firm value: after-tax operating flow / r_U
    after_tax_ebit = ebit * (Fraction(1, 1) - tau_c)
    v_u = after_tax_ebit / r_u

    print(f"Perpetual EBIT:                     ${ebit:,.2f}")
    print(f"Corporate tax rate (tau_c):          {tau_c} = {float(tau_c):.1%}")
    print(f"After-tax unlevered flow:           ${after_tax_ebit:,.2f}")
    print(f"Unlevered cost of equity (r_U):     {r_u} = {float(r_u):.2%}")
    print(f"Unlevered firm value (V_U):         ${v_u:,.2f}")

    print("\nLeverage and Tax Shield Progression:")
    print(
        f"{'Debt ($M)':>10} | {'PV(Shield)':>11} | {'V_L ($M)':>10} | {'Equity ($M)':>11} | "
        f"{'D / V':>7} | {'r_E (%)':>8} | {'WACC (%)':>8}"
    )
    print("-" * 78)

    for debt_mil in [0, 10, 20, 30, 40, 50, 60]:
        d = Fraction(debt_mil * 1_000_000, 1)

        # 1. Tax shield per period and PV
        annual_shield = tau_c * r_d * d
        pv_shield = annual_shield / r_d  # Exact discount rate r_D => pv_shield = tau_c * D
        assert pv_shield == tau_c * d, "PV(Tax Shield) must equal tau_c * D"

        # 2. Levered value
        v_l = v_u + pv_shield
        e_val = v_l - d

        # 3. Cost of equity (MM Proposition II with tax)
        # r_E = r_U + (1 - tau_c) * (r_U - r_D) * (D / E)
        de_ratio = d / e_val if e_val > 0 else Fraction(0, 1)
        r_e = r_u + (Fraction(1, 1) - tau_c) * (r_u - r_d) * de_ratio

        # 4. WACC calculated via component weights
        w_e = e_val / v_l
        w_d = d / v_l
        r_wacc_components = w_e * r_e + w_d * r_d * (Fraction(1, 1) - tau_c)

        # 5. WACC direct formula: r_U * (1 - tau_c * D / V_L)
        r_wacc_direct = r_u * (Fraction(1, 1) - tau_c * (d / v_l))
        assert r_wacc_components == r_wacc_direct, "Component WACC must match direct MM formula"

        print(
            f"{debt_mil:10.1f} | {float(pv_shield) / 1e6:10.2f}M | {float(v_l) / 1e6:10.2f} | "
            f"{float(e_val) / 1e6:11.2f} | {float(w_d):7.4f} | {float(r_e) * 100:8.2f} | "
            f"{float(r_wacc_components) * 100:8.2f}"
        )

    print("-" * 78)
    print("Numerical confirmation: PV of permanent tax shield equals tau_c * D; WACC falls as D/V rises.")


main()
