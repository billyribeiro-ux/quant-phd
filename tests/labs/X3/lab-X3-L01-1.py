"""Lab X3-L01-1: Kaldor-Working-Brennan Theory of Storage and Supply-of-Storage Curve.

Simulates the non-linear relationship between aggregate physical inventory levels,
marginal convenience yields, physical storage costs, and the forward basis spread.
"""

from __future__ import annotations

import math


def marginal_convenience_yield(inventory: float, gamma: float = 1.0, epsilon: float = 2.0) -> float:
    """Compute marginal convenience yield delta(I) as embedded stockout option value.

    delta(I) = gamma / (I + epsilon)
    """
    return gamma / (inventory + epsilon)


def marginal_storage_cost(inventory: float, c0: float = 0.02, c1: float = 0.0004) -> float:
    """Compute physical marginal warehouse and degradation cost c(I) = c0 + c1 * I."""
    return c0 + c1 * inventory


def net_cost_of_carry(inventory: float, risk_free_rate: float = 0.04) -> tuple[float, float, float]:
    """Compute (delta, c, psi) where psi = r + c - delta is net cost of carry."""
    delta = marginal_convenience_yield(inventory)
    cost = marginal_storage_cost(inventory)
    psi = risk_free_rate + cost - delta
    return delta, cost, psi


def forward_price(spot: float, net_carry: float, tenor_years: float = 0.5) -> float:
    """Compute forward price F = S * exp(psi * T)."""
    return spot * math.exp(net_carry * tenor_years)


def main() -> None:
    print("Lab X3-L01-1 | Kaldor-Working-Brennan Theory of Storage & Supply-of-Storage")
    print("-" * 75)
    hdr = (
        f"{'Inventory':>10} {'Conv Yield':>12} {'Storage Cost':>14} "
        f"{'Net Carry':>12} {'6M Forward':>12} {'Basis %':>10}"
    )
    print(hdr)
    print("-" * 75)

    spot_price = 80.0  # $80 per barrel / unit
    tenor = 0.5  # 6 months (0.5 year)
    inventory_levels = [2.0, 5.0, 10.0, 20.0, 50.0, 100.0]

    for inv in inventory_levels:
        delta, cost, psi = net_cost_of_carry(inv, risk_free_rate=0.04)
        f_price = forward_price(spot_price, psi, tenor)
        basis_pct = ((f_price - spot_price) / spot_price) * 100.0

        print(f"{inv:10.1f} {delta:12.4f} {cost:14.4f} {psi:12.4f} {f_price:12.2f} {basis_pct:9.2f}%")

    print("-" * 75)
    delta_low, _, psi_low = net_cost_of_carry(2.0)
    delta_high, _, psi_high = net_cost_of_carry(100.0)
    print(f"Low inventory (I=2.0):   delta={delta_low:.4f} > r+c => Backwardation (psi={psi_low:.4f})")
    print(f"High inventory (I=100.0): delta={delta_high:.4f} < r+c => Contango      (psi={psi_high:.4f})")


main()
