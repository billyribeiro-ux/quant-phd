"""Lab 7: Dominant-Currency Paradigm (DCP) Trade Passthrough and Volume Elasticity.

Exact calculation. Standard library only.
Compares Producer Currency Pricing (PCP), Local Currency Pricing (LCP), and DCP (Gopinath et al. 2020).
Shows that under DCP, a non-US currency depreciation fails to stimulate export volumes to third countries
while driving 100% passthrough into domestic import prices.
"""


def compute_trade_responses(
    deprec_vs_usd: float,  # Depreciation of Home currency vs USD (e.g. +0.10 = 10%)
    deprec_vs_third: float,  # Depreciation of Home currency vs Third Country (e.g. +0.10)
    price_elasticity: float = 1.0,  # Trade volume price elasticity
) -> dict[str, dict[str, float]]:
    """Compute passthrough to export prices in buyer currency, import prices in home currency, and volume responses."""
    # 1. Producer Currency Pricing (PCP): prices preset in exporter's currency
    # Home exports to Third Country: price in Third Country currency falls by deprec_vs_third
    pcp_export_price_buyer = -deprec_vs_third
    pcp_export_volume = -price_elasticity * pcp_export_price_buyer  # Increases
    # Home imports from Third Country: price in Home currency rises by deprec_vs_third
    pcp_import_price_home = deprec_vs_third
    pcp_import_volume = -price_elasticity * pcp_import_price_home  # Decreases

    # 2. Local Currency Pricing (LCP): prices preset in buyer's currency
    # Home exports to Third Country: price in Third Country currency is fixed (0)
    lcp_export_price_buyer = 0.0
    lcp_export_volume = 0.0
    # Home imports from Third Country: price in Home currency is fixed (0)
    lcp_import_price_home = 0.0
    lcp_import_volume = 0.0

    # 3. Dominant Currency Paradigm (DCP): all trade invoiced in USD
    # Home exports to Third Country: priced in USD.
    # Third Country did not depreciate against USD, so buyer price is unchanged.
    dcp_export_price_buyer = 0.0
    dcp_export_volume = 0.0
    # Home imports from Third Country: invoiced in USD. Price in Home currency rises by deprec_vs_usd.
    dcp_import_price_home = deprec_vs_usd
    dcp_import_volume = -price_elasticity * dcp_import_price_home

    return {
        "PCP": {
            "export_price_buyer": pcp_export_price_buyer,
            "export_volume": pcp_export_volume,
            "import_price_home": pcp_import_price_home,
            "import_volume": pcp_import_volume,
            "net_trade_stimulus": pcp_export_volume - pcp_import_volume,
        },
        "LCP": {
            "export_price_buyer": lcp_export_price_buyer,
            "export_volume": lcp_export_volume,
            "import_price_home": lcp_import_price_home,
            "import_volume": lcp_import_volume,
            "net_trade_stimulus": lcp_export_volume - lcp_import_volume,
        },
        "DCP": {
            "export_price_buyer": dcp_export_price_buyer,
            "export_volume": dcp_export_volume,
            "import_price_home": dcp_import_price_home,
            "import_volume": dcp_import_volume,
            "net_trade_stimulus": dcp_export_volume - dcp_import_volume,
        },
    }


def main() -> None:
    deprec = 0.10  # 10% Home currency depreciation
    results = compute_trade_responses(deprec_vs_usd=deprec, deprec_vs_third=deprec, price_elasticity=1.0)

    print("=== Dominant-Currency Paradigm vs Traditional Pricing ===")
    print(f"Shock: Home currency depreciates by {deprec * 100:.1f}% against USD and third countries.\n")

    hdr = f"{'Regime':<8} | {'Export Price':<14} | {'Export Volume':<14} | {'Import Price':<14} | {'Import Volume':<14}"
    print(hdr)
    print("-" * 72)
    for regime in ("PCP", "LCP", "DCP"):
        r = results[regime]
        ep = r["export_price_buyer"] * 100
        ev = r["export_volume"] * 100
        ip = r["import_price_home"] * 100
        iv = r["import_volume"] * 100
        print(f"{regime:<8} | {ep:+13.1f}% | {ev:+13.1f}% | {ip:+13.1f}% | {iv:+13.1f}%")

    print("\nKey Takeaway (Gopinath et al. 2020):")
    print("Under DCP (dollar invoicing), bilateral depreciation provides NO export volume boost")
    dcp_ev = results["DCP"]["export_volume"] * 100
    print(f"(Export volume change = {dcp_ev:.1f}%), while import prices surge by 100% of the shock.")

    assert results["PCP"]["export_volume"] > 0, "PCP should boost export volume"
    assert results["DCP"]["export_volume"] == 0.0, "DCP exports to third countries should not expand"
    assert results["DCP"]["import_price_home"] == deprec, "DCP import prices must rise by full depreciation"


main()
