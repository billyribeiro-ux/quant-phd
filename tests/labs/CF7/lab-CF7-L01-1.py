"""Lab CF7-L01-1: Model Architecture & Separation of Concerns.

Demonstrates topological dependency ordering and strict separation of input parameters,
calculation schedules, and output presentation in a corporate financial model.
"""

from __future__ import annotations

from typing import Any


def run_model_dag(inputs: dict[str, Any]) -> dict[str, list[float]]:
    """Evaluate financial model schedules in strict topological dependency order."""
    base_rev = float(inputs["base_revenue"])
    growth_rates: list[float] = [float(g) for g in inputs["revenue_growth"]]
    gross_margin = float(inputs["gross_margin"])
    sga_rate = float(inputs["sga_rate"])
    tax_rate = float(inputs["tax_rate"])

    revenues: list[float] = []
    gross_profits: list[float] = []
    ebitdas: list[float] = []
    net_incomes: list[float] = []

    current_rev = base_rev
    for g in growth_rates:
        # Step 1: Revenue calculation
        current_rev = current_rev * (1.0 + g)
        # Step 2: Gross profit calculation
        gp = current_rev * gross_margin
        # Step 3: Operating expense & EBITDA
        sga = current_rev * sga_rate
        ebitda = gp - sga
        # Step 4: Tax and Net Income (unlevered)
        tax = ebitda * tax_rate
        ni = ebitda - tax

        revenues.append(current_rev)
        gross_profits.append(gp)
        ebitdas.append(ebitda)
        net_incomes.append(ni)

    return {
        "revenue": revenues,
        "gross_profit": gross_profits,
        "ebitda": ebitdas,
        "net_income": net_incomes,
    }


def main() -> None:
    inputs: dict[str, Any] = {
        "base_revenue": 500.0,
        "revenue_growth": [0.08, 0.07, 0.06],
        "gross_margin": 0.45,
        "sga_rate": 0.20,
        "tax_rate": 0.25,
    }

    results = run_model_dag(inputs)
    print("Period 1 Revenue:", f"{results['revenue'][0]:.4f}")
    print("Period 3 Revenue:", f"{results['revenue'][2]:.4f}")
    print("Period 1 EBITDA:", f"{results['ebitda'][0]:.4f}")
    print("Period 3 EBITDA:", f"{results['ebitda'][2]:.4f}")
    print("Period 1 Net Income:", f"{results['net_income'][0]:.4f}")
    print("Period 3 Net Income:", f"{results['net_income'][2]:.4f}")


main()
