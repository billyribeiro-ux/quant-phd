"""Lab PM4-L05-1: Commercial Real Estate Cash Flows, Cap Rates, and REIT NAV Valuation.

SIMULATED: Models commercial property NOI, capitalization rate valuation sensitivity,
and the public REIT balance-sheet bridge from Gross Asset Value to NAV per share and FFO/AFFO.
"""

from __future__ import annotations


def compute_property_noi(
    gross_potential_rent: float,
    expense_reimbursements: float,
    vacancy_credit_loss_rate: float,
    property_management_rate: float,
    real_estate_taxes: float,
    insurance_utilities_maintenance: float,
) -> dict[str, float]:
    """Compute property Net Operating Income (NOI)."""
    pgi = gross_potential_rent + expense_reimbursements
    vacancy_loss = pgi * vacancy_credit_loss_rate
    egi = pgi - vacancy_loss
    management_fee = egi * property_management_rate
    opex = real_estate_taxes + insurance_utilities_maintenance + management_fee
    noi = egi - opex
    return {
        "pgi": pgi,
        "vacancy_loss": vacancy_loss,
        "egi": egi,
        "opex": opex,
        "noi": noi,
    }


def compute_reit_nav(
    sector_nois: dict[str, float],
    sector_cap_rates: dict[str, float],
    cash_and_equivalents: float,
    total_debt: float,
    preferred_equity: float,
    shares_outstanding: float,
) -> dict[str, float]:
    """Compute REIT Gross Asset Value and Net Asset Value (NAV) per share."""
    gross_real_estate_value = 0.0
    for sector, noi in sector_nois.items():
        cap_rate = sector_cap_rates[sector]
        gross_real_estate_value += noi / cap_rate

    gross_asset_value = gross_real_estate_value + cash_and_equivalents
    total_obligations = total_debt + preferred_equity
    net_asset_value = gross_asset_value - total_obligations
    nav_per_share = net_asset_value / shares_outstanding

    return {
        "gross_real_estate_value": gross_real_estate_value,
        "gross_asset_value": gross_asset_value,
        "net_asset_value": net_asset_value,
        "nav_per_share": nav_per_share,
    }


def reconcile_ffo_affo(
    gaap_net_income: float,
    depreciation_amortization: float,
    gain_on_property_sales: float,
    recurring_capex: float,
    straight_line_rent_adj: float,
) -> dict[str, float]:
    """Reconcile GAAP Net Income to NAREIT FFO and AFFO."""
    ffo = gaap_net_income + depreciation_amortization - gain_on_property_sales
    affo = ffo - recurring_capex - straight_line_rent_adj
    return {
        "gaap_net_income": gaap_net_income,
        "ffo": ffo,
        "affo": affo,
    }


def main() -> None:
    # 1. Commercial Property Cash Flow
    prop = compute_property_noi(
        gross_potential_rent=12_000_000.0,
        expense_reimbursements=1_500_000.0,
        vacancy_credit_loss_rate=0.07,
        property_management_rate=0.035,
        real_estate_taxes=1_400_000.0,
        insurance_utilities_maintenance=1_800_000.0,
    )

    cap_rate = 0.0625  # 6.25% market cap rate
    prop_val = prop["noi"] / cap_rate
    expected_growth = 0.0225  # 2.25% annual NOI growth
    cost_of_capital = cap_rate + expected_growth

    print("Commercial Property Operating Performance:")
    print(f"Potential Gross Income (PGI):   {prop['pgi']:12.2f}")
    print(f"Effective Gross Income (EGI):   {prop['egi']:12.2f}")
    print(f"Total Operating Expenses:       {prop['opex']:12.2f}")
    print(f"Net Operating Income (NOI):     {prop['noi']:12.2f}")
    print(f"Market Capitalization Rate:     {cap_rate * 100:12.2f} %")
    print(f"Capitalized Property Value:     {prop_val:12.2f}")
    print(f"Implied Required Return (r):    {cost_of_capital * 100:12.2f} %")

    # 2. REIT Multi-Sector NAV Bridge
    sector_nois = {
        "Industrial": 45_000_000.0,
        "Multifamily": 55_000_000.0,
        "Retail": 25_000_000.0,
    }
    sector_caps = {
        "Industrial": 0.0525,
        "Multifamily": 0.0575,
        "Retail": 0.0675,
    }
    nav_data = compute_reit_nav(
        sector_nois=sector_nois,
        sector_cap_rates=sector_caps,
        cash_and_equivalents=85_000_000.0,
        total_debt=820_000_000.0,
        preferred_equity=100_000_000.0,
        shares_outstanding=40_000_000.0,
    )

    print("\nREIT NAV Balance-Sheet Bridge:")
    print(f"Gross Real Estate Value:        {nav_data['gross_real_estate_value']:12.2f}")
    print(f"Total Gross Asset Value:        {nav_data['gross_asset_value']:12.2f}")
    print(f"Total Net Asset Value (NAV):    {nav_data['net_asset_value']:12.2f}")
    print(f"NAV Per Share:                  {nav_data['nav_per_share']:12.2f}")

    # 3. FFO and AFFO Cash Flow Reconciliation
    cash_metrics = reconcile_ffo_affo(
        gaap_net_income=32_000_000.0,
        depreciation_amortization=68_000_000.0,
        gain_on_property_sales=5_000_000.0,
        recurring_capex=14_000_000.0,
        straight_line_rent_adj=2_500_000.0,
    )

    print("\nREIT Earnings Quality Reconciliation:")
    print(f"GAAP Net Income:                {cash_metrics['gaap_net_income']:12.2f}")
    print(f"Funds From Operations (FFO):    {cash_metrics['ffo']:12.2f}")
    print(f"Adjusted FFO (AFFO):            {cash_metrics['affo']:12.2f}")

    assert prop["noi"] > 0.0
    assert nav_data["nav_per_share"] > 0.0
    assert cash_metrics["affo"] > cash_metrics["gaap_net_income"]


main()
