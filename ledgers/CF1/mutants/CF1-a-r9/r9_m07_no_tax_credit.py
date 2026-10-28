"""CF1 lab L02: after-tax incremental cash flows of a SIMULATED machine project.

SIMULATED: revenues and cash costs are generated from a seeded random number generator. The machine, the tax rate
and every figure are invented for this lab and are not a real company's. Money is entered in integer cents;
EBITDA is exact integer cents; tax and operating cash flow are floating point cents, and the flows are held and
discounted in dollars and printed to two decimals. Standard library only; no network; every number
printed in the table and the results is computed by the code below; the capex line restates typed-in inputs.

Conventions applied: straight-line depreciation over the life, with no salvage; tax at one rate on taxable income,
with a negative tax (a credit) when taxable income is negative, which assumes the firm uses the loss in the same
year; working capital is 10 percent of the year's revenue, held at the end of years 1 to 3 and fully recovered at
the end of year 4; the sunk study cost is excluded from the incremental flows.
"""

from __future__ import annotations

import random

SEED = 20261028
TAX_RATE = 0.25
RATE = 0.08
LIFE_YEARS = 4
CAPEX_CENTS = 1_200_000
SUNK_STUDY_CENTS = 200_000
TOLERANCE = 1e-6


def npv_dollars(flows_dollars: list[float], rate: float) -> float:
    """Net present value in dollars of flows_dollars[t], received at the end of period t, at a rate per period."""
    return sum(flow / (1.0 + rate) ** t for t, flow in enumerate(flows_dollars))


def main() -> None:
    rng = random.Random(SEED)
    depreciation_cents = CAPEX_CENTS // LIFE_YEARS
    revenue_cents = [0]
    cost_cents = [0]
    for _ in range(LIFE_YEARS):
        revenue_cents.append(rng.randrange(50, 71) * 10_000)
        cost_cents.append(rng.randrange(20, 31) * 10_000)
    # Working capital is 10 percent of revenue at the end of years 1 to 3, zero at the start and at the end.
    nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]

    print("SIMULATED machine: capex 12,000.00 dollars, four-year life, straight-line depreciation, tax rate 25 percent")
    print(f"depreciation per year, in dollars: {depreciation_cents / 100:.2f}")
    print(f"sunk study cost, excluded from the incremental flows, in dollars: {SUNK_STUDY_CENTS / 100:.2f}")
    print()
    print("year  revenue  cash_cost  ebitda      tax     after_tax_ocf  nwc_flow     total")

    flows: list[float] = [-CAPEX_CENTS / 100]
    nwc_flows: list[float] = []
    identity_ok = True
    shield_ok = True
    for t in range(1, LIFE_YEARS + 1):
        ebitda = revenue_cents[t] - cost_cents[t]
        ebit = ebitda - depreciation_cents
        tax = TAX_RATE * max(ebit, 0)
        ocf = ebit - tax + depreciation_cents
        shield = TAX_RATE * depreciation_cents
        # The identity: after-tax operating cash flow = EBITDA x (1 - tax rate) + depreciation x tax rate.
        identity_ok = identity_ok and abs(ocf - (ebitda * (1 - TAX_RATE) + shield)) < TOLERANCE
        # The shield, measured as the difference between the operating cash flow with depreciation and the one
        # without it (EBIT equal to EBITDA, no add-back), must equal depreciation x tax rate.
        ocf_without = ebitda - TAX_RATE * ebitda
        shield_ok = shield_ok and abs((ocf - ocf_without) - depreciation_cents * TAX_RATE) < TOLERANCE
        nwc_flow = -(nwc_cents[t] - nwc_cents[t - 1]) / 100
        nwc_flows.append(nwc_flow)
        total = ocf / 100 + nwc_flow
        flows.append(total)
        print(
            f"{t:>4}  {revenue_cents[t] / 100:>7.2f}  {cost_cents[t] / 100:>9.2f}  {ebitda / 100:>7.2f}"
            f"  {tax / 100:>7.2f}  {ocf / 100:>13.2f}  {nwc_flow:>8.2f}  {total:>8.2f}"
        )

    print()
    print(
        "after-tax operating cash flow equals EBITDA times (1 - tax rate) plus the shield, in every year:", identity_ok
    )
    print("depreciation shield equals depreciation times the tax rate, in every year:", shield_ok)
    print(f"depreciation shield per year, in dollars: {TAX_RATE * depreciation_cents / 100:.2f}")
    print(f"working-capital investment and recovery sum to zero: {sum(nwc_flows) == 0.0}")
    print(f"sum of working-capital flows, in dollars: {sum(nwc_flows):.2f}")
    print()
    npv = npv_dollars(flows, RATE)
    print(f"NPV at {RATE:.2f} of the incremental flows, in dollars: {npv:.2f}")
    with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100, *flows[1:]], RATE)
    print(f"NPV if the sunk study cost is charged to the project, in dollars: {with_sunk:.2f}")
    print(f"difference, in dollars: {npv - with_sunk:.2f}")


main()
