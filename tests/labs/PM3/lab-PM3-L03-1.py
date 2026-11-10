"""Lab PM3-L03-1: Infrastructure Concession Cash Flows, DSCR and LLCR Modeling.

SIMULATED: Evaluates project finance concession waterfalls under Availability Payment vs.
Merchant Demand risk regimes, calculating CFADS, DSCR, and LLCR covenant coverage.
"""

from __future__ import annotations

import numpy as np


def compute_annual_debt_service(principal: float, rate: float, tenor: int) -> float:
    """Compute constant annual debt service payment for fully amortizing project debt."""
    if rate == 0.0:
        return principal / tenor
    return float(principal * (rate / (1.0 - (1.0 + rate) ** (-tenor))))


def project_debt_waterfall(
    cfads: np.ndarray,
    debt_service: float,
    interest_rate: float,
    initial_debt: float,
    tenor: int,
) -> dict[str, np.ndarray]:
    """Calculate the debt repayment schedule, DSCR, LLCR, and equity distributions.

    Parameters
    ----------
    cfads : np.ndarray
        Array of Cash Flow Available for Debt Service across concession years.
    debt_service : float
        Constant annual debt service requirement during the debt tenor.
    interest_rate : float
        Annual debt interest rate (decimal).
    initial_debt : float
        Initial debt principal balance ($).
    tenor : int
        Contractual debt repayment tenor in years.

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary with balances, principal, interest, dscr, llcr, and equity_cf.
    """
    n_years = len(cfads)
    balances = np.zeros(n_years + 1)
    interest_pmts = np.zeros(n_years)
    principal_pmts = np.zeros(n_years)
    dscr = np.zeros(n_years)
    llcr = np.zeros(n_years)
    equity_cf = np.zeros(n_years)

    balances[0] = initial_debt

    for t in range(n_years):
        bal = balances[t]
        if t < tenor and bal > 1e-4:
            interest = bal * interest_rate
            principal = min(bal, debt_service - interest)
            tot_ds = interest + principal
            dscr[t] = cfads[t] / tot_ds if tot_ds > 0 else np.nan

            # LLCR: NPV of remaining CFADS through loan life / current debt balance
            rem_cfads = cfads[t:tenor]
            discount_factors = (1.0 + interest_rate) ** (-np.arange(len(rem_cfads)))
            npv_rem = float(np.sum(rem_cfads * discount_factors))
            llcr[t] = npv_rem / bal if bal > 0 else np.nan

            balances[t + 1] = max(0.0, bal - principal)
            interest_pmts[t] = interest
            principal_pmts[t] = principal
            equity_cf[t] = max(0.0, cfads[t] - tot_ds)
        else:
            balances[t + 1] = 0.0
            dscr[t] = np.nan
            llcr[t] = np.nan
            equity_cf[t] = cfads[t]

    return {
        "balances": balances,
        "principal": principal_pmts,
        "interest": interest_pmts,
        "dscr": dscr,
        "llcr": llcr,
        "equity_cf": equity_cf,
    }


def main() -> None:
    initial_debt = 150_000_000.0  # $150M debt (75% of $200M CapEx)
    tenor = 15
    interest_rate = 0.05
    n_years = 20

    debt_service = compute_annual_debt_service(initial_debt, interest_rate, tenor)

    # 1. Availability Payment Concession: stable contracted CFADS = $18M/yr
    cfads_avail = np.full(n_years, 18_000_000.0)
    res_avail = project_debt_waterfall(cfads_avail, debt_service, interest_rate, initial_debt, tenor)

    # 2. Merchant Volume Concession: demand risk with severe recession in years 4-5
    cfads_merchant = np.full(n_years, 19_500_000.0)
    cfads_merchant[3] = 11_000_000.0  # Year 4 traffic drop (-43%)
    cfads_merchant[4] = 12_500_000.0  # Year 5 partial recovery
    res_merchant = project_debt_waterfall(cfads_merchant, debt_service, interest_rate, initial_debt, tenor)

    print("Project Finance Infrastructure Concession Modeling:")
    print(f"Initial Senior Debt:           ${initial_debt / 1e6:8.2f}M")
    print(f"Contractual Tenor:              {tenor:8d} years")
    print(f"Annual Debt Service:           ${debt_service / 1e6:8.2f}M / year\n")

    print("Year | Availability DSCR | Availability LLCR | Merchant DSCR | Merchant LLCR")
    print("-" * 75)

    test_years = [1, 2, 3, 4, 5, 8, 10, 12, 15]
    for yr in test_years:
        idx = yr - 1
        d_av = res_avail["dscr"][idx]
        l_av = res_avail["llcr"][idx]
        d_me = res_merchant["dscr"][idx]
        l_me = res_merchant["llcr"][idx]
        print(f"{yr:4d} | {d_av:17.3f} | {l_av:17.3f} | {d_me:13.3f} | {l_me:13.3f}")

    min_dscr_avail = float(np.nanmin(res_avail["dscr"]))
    min_dscr_merchant = float(np.nanmin(res_merchant["dscr"]))

    print(f"\nMinimum Availability DSCR: {min_dscr_avail:.4f}x (passes 1.20x covenant threshold)")
    print(f"Minimum Merchant DSCR:     {min_dscr_merchant:.4f}x (BREACHES 1.20x covenant in year 4)")

    # Assertions
    assert min_dscr_avail >= 1.20
    assert min_dscr_merchant < 1.00  # Default or covenant breach under severe volume drop
    assert np.isclose(res_avail["balances"][tenor], 0.0, atol=1e-2)

    print("Covenant & Amortization Assertion: Verified non-recourse debt amortization and volume risk sensitivity.")


main()
