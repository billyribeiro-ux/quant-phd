"""Starter template for SR2 project: Leverage-cycle model.

Implement the Geanakoplos collateral-equilibrium solver and margin-shock simulation.
"""


def solve_geanakoplos_equilibrium(
    v_u: float,
    v_d: float,
    risk_free_rate: float = 1.0,
    max_loan_ratio: float = 1.0,
) -> dict[str, float]:
    """Calculate the collateral equilibrium for a two-state asset."""
    raise NotImplementedError("solve_geanakoplos_equilibrium not implemented")


def simulate_margin_shock(
    v_u: float,
    v_d: float,
    initial_loan_ratio: float,
    shocked_loan_ratio: float,
    risk_free_rate: float = 1.0,
) -> dict[str, float]:
    """Simulate the asset price and leverage response to an exogenous margin shock."""
    raise NotImplementedError("simulate_margin_shock not implemented")


def solve_three_period_cycle(
    v_uu: float,
    v_ud: float,
    v_du: float,
    v_dd: float,
    risk_free_rate: float = 1.0,
) -> dict[str, float]:
    """Solve a 3-period (t=0, 1, 2) leverage cycle tree."""
    raise NotImplementedError("solve_three_period_cycle not implemented")
