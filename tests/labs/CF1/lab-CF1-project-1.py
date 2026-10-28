"""CF1 project lab 1 (rung 1, worked example): NPV with tax, depreciation and working capital.

SIMULATED: a three-year machine project written here for teaching. It is not any company's project.
Money is entered in integer cents; every flow is a float in cents, printed in dollars to two decimals. Standard
library only, no randomness, no network. The conventions are those of the specification on the project page:
straight-line depreciation with no salvage; tax at one rate on taxable income, with a negative tax (a credit) when
taxable income is negative; working capital is 10 percent of the year's revenue, held at the end of years 1 and 2
and recovered at the end of year 3.
"""

from __future__ import annotations

CAPEX = 900_000  # cents, paid at t = 0
LIFE = 3  # years
REVENUE = [600_000, 650_000, 700_000]  # cents, years 1 to 3
CASH_COSTS = [200_000, 210_000, 220_000]  # cents, years 1 to 3, entered as positives
TAX_RATE = 0.25
NWC_SHARE = 0.10
RATE = 0.10  # nominal, per year


def usd(cents: float) -> str:
    """Cents shown as dollars with two decimals."""
    return f"{cents / 100:.2f}"


def main() -> None:
    depreciation = CAPEX / LIFE
    print(f"step 1, depreciation: {usd(CAPEX)} / {LIFE} = {usd(depreciation)} dollars a year")
    print(f"step 2, working capital is {NWC_SHARE} of revenue at the end of years 1 and 2, zero at the start and end")
    nwc = [0.0] + [NWC_SHARE * REVENUE[t - 1] for t in range(1, LIFE)] + [0.0]
    print(f"        nwc_1 = {usd(nwc[1])}, nwc_2 = {usd(nwc[2])}")
    flows = [-float(CAPEX)]
    working_capital_flows: list[float] = []
    identity_holds = True
    print("step 3, year by year, in dollars: revenue, cash cost, EBITDA, tax, shield, working capital, flow")
    for t in range(1, LIFE + 1):
        ebitda = REVENUE[t - 1] - CASH_COSTS[t - 1]
        tax = TAX_RATE * (ebitda - depreciation)
        shield = TAX_RATE * depreciation
        working_capital = -(nwc[t] - nwc[t - 1])
        flow = ebitda - tax + working_capital
        flows.append(flow)
        working_capital_flows.append(working_capital)
        identity_holds = identity_holds and abs((ebitda - tax) - (ebitda * (1 - TAX_RATE) + shield)) < 1e-6
        print(
            f"  year {t}: {usd(REVENUE[t - 1])}  {usd(CASH_COSTS[t - 1])}  {usd(ebitda)}  {usd(tax)}  "
            f"{usd(shield)}  {usd(working_capital)}  {usd(flow)}"
        )
    print(
        f"step 4, EBITDA x (1 - tax rate) + shield equals after-tax operating cash flow in every year: {identity_holds}"
    )
    print(f"step 5, the working-capital flows sum to zero: {sum(working_capital_flows) == 0.0}")
    print("step 6, flows at t = 0 to 3, in dollars:", ", ".join(usd(cf) for cf in flows))
    npv = sum(cf / (1.0 + RATE) ** t for t, cf in enumerate(flows))
    print(f"step 7, NPV at {RATE:.2f}: {usd(npv)} dollars")
    shield_pv = sum(TAX_RATE * depreciation / (1.0 + RATE) ** t for t in range(1, LIFE + 1))
    print(f"step 8, present value of the depreciation shield at {RATE:.2f}: {usd(shield_pv)} dollars")
    print(f"step 9, NPV with no shield, npv minus the shield's present value: {usd(npv - shield_pv)} dollars")


main()
