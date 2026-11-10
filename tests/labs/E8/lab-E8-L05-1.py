"""Lab 5: The Mundell-Fleming Linear Model Multiplier Verification.

Exact Fraction arithmetic. Standard library only.
Solves the IS-LM-BoP open economy system under perfect capital mobility (i = i*).
Compares fiscal and monetary policy effectiveness under Fixed vs. Floating exchange rates.
"""

from fractions import Fraction


class MundellFlemingModel:
    def __init__(
        self,
        c1: Fraction,  # Marginal propensity to consume
        m1: Fraction,  # Marginal propensity to import
        eta: Fraction,  # Marshall-Lerner sensitivity of net exports to exchange rate
        k: Fraction,  # Money demand sensitivity to output
        h: Fraction,  # Money demand sensitivity to interest rate
        p: Fraction,  # Price level (fixed in short run)
    ) -> None:
        self.c1 = c1
        self.m1 = m1
        self.eta = eta
        self.k = k
        self.h = h
        self.p = p

    def solve_floating(
        self,
        m_supply: Fraction,
        g_spending: Fraction,
        i_world: Fraction,
        a0: Fraction,
    ) -> tuple[Fraction, Fraction]:
        """Under Floating FX: Money market pins Y; Goods market pins exchange rate e.

        Y = (M/P + h * i*) / k
        e = [ Y * (1 - c1 + m1) - (A0 - b*i* + G) ] / eta
        """
        # LM determines Y
        real_balances = m_supply / self.p
        y = (real_balances + self.h * i_world) / self.k

        # IS determines equilibrium exchange rate e
        autonomous_exp = a0 + g_spending
        numerator = y * (Fraction(1, 1) - self.c1 + self.m1) - autonomous_exp
        e = numerator / self.eta
        return y, e

    def solve_fixed(
        self,
        e_target: Fraction,
        g_spending: Fraction,
        i_world: Fraction,
        a0: Fraction,
    ) -> tuple[Fraction, Fraction]:
        """Under Fixed FX: Goods market pins Y; Money supply M adjusts endogenously to clear LM.

        Y = (A0 - b*i* + G + eta * e_target) / (1 - c1 + m1)
        M = P * (k * Y - h * i*)
        """
        multiplier = Fraction(1, 1) / (Fraction(1, 1) - self.c1 + self.m1)
        autonomous_exp = a0 + g_spending + self.eta * e_target
        y = multiplier * autonomous_exp

        # Endogenous money supply required to maintain i = i*
        m_endogenous = self.p * (self.k * y - self.h * i_world)
        return y, m_endogenous

    def multipliers(self) -> dict[str, Fraction]:
        """Compute analytical multipliers dY/dG and dY/dM under both regimes."""
        # Floating
        dy_dg_float = Fraction(0, 1)
        dy_dm_float = Fraction(1, 1) / (self.k * self.p)

        # Fixed
        dy_dg_fixed = Fraction(1, 1) / (Fraction(1, 1) - self.c1 + self.m1)
        dy_dm_fixed = Fraction(0, 1)

        return {
            "dy_dg_floating": dy_dg_float,
            "dy_dm_floating": dy_dm_float,
            "dy_dg_fixed": dy_dg_fixed,
            "dy_dm_fixed": dy_dm_fixed,
        }


def main() -> None:
    # Model parameters: c1 = 0.6, m1 = 0.2, eta = 500, k = 0.5, h = 1000, P = 1.0
    model = MundellFlemingModel(
        c1=Fraction(6, 10),
        m1=Fraction(2, 10),
        eta=Fraction(500, 1),
        k=Fraction(1, 2),
        h=Fraction(1000, 1),
        p=Fraction(1, 1),
    )

    i_world = Fraction(3, 100)  # 3.0%
    a0 = Fraction(200, 1)  # Autonomous expenditure baseline
    g_base = Fraction(100, 1)  # Baseline government spending
    m_base = Fraction(400, 1)  # Baseline money supply

    # Baseline floating
    y_float_base, e_float_base = model.solve_floating(m_base, g_base, i_world, a0)

    # Fiscal expansion under floating (Delta G = +50)
    g_expanded = g_base + Fraction(50, 1)
    y_float_fiscal, e_float_fiscal = model.solve_floating(m_base, g_expanded, i_world, a0)

    # Monetary expansion under floating (Delta M = +50)
    m_expanded = m_base + Fraction(50, 1)
    y_float_monetary, e_float_monetary = model.solve_floating(m_expanded, g_base, i_world, a0)

    # Fixed regime targeting e = e_float_base
    y_fixed_base, m_fixed_base = model.solve_fixed(e_float_base, g_base, i_world, a0)
    y_fixed_fiscal, m_fixed_fiscal = model.solve_fixed(e_float_base, g_expanded, i_world, a0)

    mults = model.multipliers()

    print("=== Mundell–Fleming Analytical Multipliers ===")
    print(f"Floating Regime: dY/dG = {mults['dy_dg_floating']} (Fiscal policy ineffective)")
    print(f"Floating Regime: dY/dM = {float(mults['dy_dm_floating']):.2f} (Monetary policy maximum effectiveness)")
    print(f"Fixed Regime:    dY/dG = {float(mults['dy_dg_fixed']):.2f} (Fiscal policy maximum effectiveness)")
    print(f"Fixed Regime:    dY/dM = {mults['dy_dm_fixed']} (Monetary policy ineffective)\n")

    print("=== Policy Shock Responses (Exact) ===")
    print(f"Base Output (Y): {float(y_float_base):.2f}, Base Exchange Rate (e): {float(e_float_base):.4f}")
    delta_y_fiscal = float(y_float_fiscal - y_float_base)
    delta_e_fiscal = float(e_float_fiscal - e_float_base)
    print(f"Floating Fiscal (+50 G): Delta Y = {delta_y_fiscal:.2f}, FX change = {delta_e_fiscal:+.4f}")
    delta_y_mon = float(y_float_monetary - y_float_base)
    delta_e_mon = float(e_float_monetary - e_float_base)
    print(f"Floating Monetary (+50 M): Delta Y = {delta_y_mon:.2f}, FX change = {delta_e_mon:+.4f}")
    delta_y_fixed = float(y_fixed_fiscal - y_fixed_base)
    delta_m_fixed = float(m_fixed_fiscal - m_fixed_base)
    print(f"Fixed Fiscal (+50 G): Delta Y = {delta_y_fixed:.2f}, Money expansion = {delta_m_fixed:.2f}")

    assert mults["dy_dg_floating"] == Fraction(0, 1), "Floating fiscal multiplier must be 0"
    assert mults["dy_dm_fixed"] == Fraction(0, 1), "Fixed monetary multiplier must be 0"
    assert y_float_fiscal == y_float_base, "Fiscal policy under floating must not change output"
    assert y_fixed_fiscal > y_fixed_base, "Fiscal policy under fixed must expand output"


main()
