"""CF9 lab L04-1: FX Translation Exposure - Current Rate Method vs. Temporal Method.

Compares balance sheet translation under ASC 830 / IAS 21:
1. Current Rate Method: All assets and liabilities at current rate;
   translation adjustment sits in Cumulative Translation Adjustment (CTA) in equity (OCI).
2. Temporal (Monetary/Non-Monetary) Method: Non-monetary assets at historical rates;
   translation gain/loss flows directly through consolidated Net Income.
3. Quantifies accounting exposure polarity reversal: net asset exposed (Current Rate)
   versus net monetary liability exposed (Temporal Method).
4. Demonstrates why hedging translation exposure creates real cash flow volatility.
Standard library only; deterministic execution.
"""

from __future__ import annotations


def translate_financial_statements(
    monetary_assets_gbp: float = 2_000_000.0,
    inventory_gbp: float = 3_000_000.0,
    ppe_net_gbp: float = 5_000_000.0,
    monetary_liab_gbp: float = 7_000_000.0,
    equity_gbp: float = 3_000_000.0,
    net_income_gbp: float = 500_000.0,
    s_hist: float = 1.30,
    s_end: float = 1.15,
    s_avg: float = 1.22,
) -> dict[str, float]:
    """Compute consolidated USD balance sheet and translation adjustment under both accounting methods."""
    total_assets_gbp = monetary_assets_gbp + inventory_gbp + ppe_net_gbp

    # ==========================================
    # METHOD 1: Current Rate Method (Functional = GBP)
    # ==========================================
    assets_crm = total_assets_gbp * s_end
    liab_crm = monetary_liab_gbp * s_end
    equity_hist_usd = equity_gbp * s_hist
    net_income_crm_usd = net_income_gbp * s_avg

    # Assets_crm = Liab_crm + Equity_hist_usd + Net_income_crm_usd + CTA
    cta_plug = assets_crm - (liab_crm + equity_hist_usd + net_income_crm_usd)
    net_exposure_crm_gbp = total_assets_gbp - monetary_liab_gbp

    # ==========================================
    # METHOD 2: Temporal Method (Functional = USD)
    # ==========================================
    monetary_assets_usd = monetary_assets_gbp * s_end
    inventory_usd = inventory_gbp * s_hist
    ppe_usd = ppe_net_gbp * s_hist
    assets_temporal = monetary_assets_usd + inventory_usd + ppe_usd
    liab_temporal = monetary_liab_gbp * s_end

    net_monetary_exposure_gbp = monetary_assets_gbp - monetary_liab_gbp
    operating_income_usd = net_income_gbp * s_avg

    # Assets_temporal = Liab_temporal + Equity_hist_usd + operating_income_usd + fx_gain_loss
    fx_gain_loss_temporal = assets_temporal - (liab_temporal + equity_hist_usd + operating_income_usd)
    total_net_income_temporal = operating_income_usd + fx_gain_loss_temporal

    return {
        "s_hist": s_hist,
        "s_end": s_end,
        "total_assets_gbp": total_assets_gbp,
        "net_exposure_crm_gbp": net_exposure_crm_gbp,
        "assets_crm_usd": assets_crm,
        "liab_crm_usd": liab_crm,
        "net_income_crm_usd": net_income_crm_usd,
        "cta_plug_usd": cta_plug,
        "net_monetary_exposure_gbp": net_monetary_exposure_gbp,
        "assets_temporal_usd": assets_temporal,
        "liab_temporal_usd": liab_temporal,
        "fx_gain_loss_temporal": fx_gain_loss_temporal,
        "total_net_income_temporal": total_net_income_temporal,
    }


def main() -> None:
    print("CF9 Lab L04-1: FX Translation Exposure Analysis")
    print("===============================================")

    # UK subsidiary with £10M assets, £7M debt, £3M equity
    # Spot depreciates from $1.30 to $1.15 (-11.5%)
    res = translate_financial_statements()

    print("1. Balance Sheet Profile (in Local Currency GBP):")
    print(f"   Total Subsidiary Assets:         £{res['total_assets_gbp']:,.2f}")
    print("   - Monetary Assets (Cash/Rec):    £2,000,000.00")
    print("   - Non-Monetary Assets (PP&E/Inv):£8,000,000.00")
    print("   - Monetary Liabilities (Debt):   £7,000,000.00")
    print("   - Shareholder Equity:            £3,000,000.00")

    print("\n2. Method 1: Current Rate Method (ASC 830 / IAS 21):")
    print(f"   Net Accounting Exposure:         £{res['net_exposure_crm_gbp']:,.2f} (Net Asset Position)")
    print(f"   Consolidated Assets (at $1.15):  ${res['assets_crm_usd']:,.2f}")
    print(f"   Consolidated Debt (at $1.15):    ${res['liab_crm_usd']:,.2f}")
    print(f"   Reported Net Income (avg $1.22): ${res['net_income_crm_usd']:,.2f}")
    print(f"   Cumulative Translation Adj (CTA):${res['cta_plug_usd']:,.2f} (OCI Equity Loss)")
    print("   Net Income Impact:               $0.00 (Zero impact on P&L earnings)")

    print("\n3. Method 2: Temporal Method (Monetary/Non-Monetary):")
    print(f"   Net Accounting Exposure:         £{res['net_monetary_exposure_gbp']:,.2f} (Net Liability Position)")
    print(f"   Consolidated Assets:             ${res['assets_temporal_usd']:,.2f}")
    print(f"   Consolidated Debt (at $1.15):    ${res['liab_temporal_usd']:,.2f}")
    print(f"   FX Translation Gain/Loss to P&L: ${res['fx_gain_loss_temporal']:,.2f} (Gain in Net Income!)")
    print(f"   Consolidated Net Income:         ${res['total_net_income_temporal']:,.2f}")

    print("\n4. Theoretical & Practical Implications:")
    print(f"   Polarity Paradox: Currency depreciation created an equity OCI loss (${res['cta_plug_usd']:,.2f})")
    print(
        f"   under Current Rate, but a reported net income gain (+${res['fx_gain_loss_temporal']:,.2f}) "
        "under Temporal Method!"
    )
    print("   Cash Flow Reality: Actual operational cash flows in GBP are unaffected by translation.")


main()
