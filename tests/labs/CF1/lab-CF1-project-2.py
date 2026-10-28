"""CF1 project lab 2 (rung 2, completion): the after-tax cash-flow line of the rung-1 project.

SIMULATED: the same three-year machine project as the worked example, not any company's project. Money is in integer
cents; flows are floats in cents, printed in dollars. Standard library only, no randomness, no network.

This file is the completed version. On the page, the three lines that assign tax, operating and working_capital are
blanked with ___; every other line of the page is the same as this file. The expected output below is this file's
output, so a completed page run matches it only when every blank is right.
"""

from __future__ import annotations

CAPEX = 900_000
LIFE = 3
REVENUE = [600_000, 650_000, 700_000]
CASH_COSTS = [200_000, 210_000, 220_000]
TAX_RATE = 0.25
RATE = 0.10
DEPRECIATION = CAPEX / LIFE
NWC = [0.0, 60_000.0, 65_000.0, 0.0]  # working capital at the end of years 0 to 3, given


def usd(cents: float) -> str:
    return f"{cents / 100:.2f}"


def main() -> None:
    flows = [-float(CAPEX)]
    for t in range(1, LIFE + 1):
        ebitda = REVENUE[t - 1] - CASH_COSTS[t - 1]
        tax = TAX_RATE * (ebitda - DEPRECIATION)
        operating = ebitda - tax
        working_capital = -(NWC[t] - NWC[t - 1])
        flows.append(operating + working_capital)
    print("flows at t = 0 to 3 (dollars):", ", ".join(usd(cf) for cf in flows))
    print("NPV at 0.10 (dollars):", usd(sum(cf / (1.0 + RATE) ** t for t, cf in enumerate(flows))))


main()
