"""CF6 Lesson 5 Inline Lab 1: Corporate Debt Pricing and Syndicate Economics.

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal


def syndicate_fee_waterfall(
    gross_proceeds_cents: int,
    spread_bps: int = 700,
    lead_manager_share: float = 0.60,
    co_manager_share: float = 0.30,
    selling_group_share: float = 0.10,
) -> dict[str, int]:
    spread_dec = Decimal(spread_bps) / Decimal(10000)
    total_spread = int((Decimal(gross_proceeds_cents) * spread_dec).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    net_proceeds = gross_proceeds_cents - total_spread

    lead_dec = Decimal(str(lead_manager_share))
    co_dec = Decimal(str(co_manager_share))
    lead_cents = int((Decimal(total_spread) * lead_dec).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    co_cents = int((Decimal(total_spread) * co_dec).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    selling_cents = total_spread - lead_cents - co_cents

    mgmt_fee = int((Decimal(total_spread) * Decimal("0.20")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    uw_fee = int((Decimal(total_spread) * Decimal("0.20")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    selling_concession = total_spread - mgmt_fee - uw_fee

    return {
        "gross_proceeds_cents": gross_proceeds_cents,
        "total_spread_cents": total_spread,
        "net_proceeds_cents": net_proceeds,
        "lead_manager_cents": lead_cents,
        "co_manager_cents": co_cents,
        "selling_group_cents": selling_cents,
        "management_fee_cents": mgmt_fee,
        "underwriting_fee_cents": uw_fee,
        "selling_concession_cents": selling_concession,
    }


def main() -> None:
    # 5-Year Investment-Grade Corporate Debt Offering
    principal_offering = 500_000_000_00  # $500M in cents
    benchmark_treasury_yield = 0.0425  # 5-Year UST at 4.25%
    credit_spread_bps = 135  # 135 bps BBB corporate credit spread
    coupon_rate = benchmark_treasury_yield + (credit_spread_bps / 10000.0)
    underwriting_gross_spread_bps = 65  # 65 bps (0.65%) for IG corporate bond

    print("=== Corporate Debt Issuance: 5-Year Senior Unsecured BBB Notes ===")
    print(f"Principal Offering:       ${principal_offering / 100:,.2f}")
    print(f"5-Year Benchmark Treasury: {benchmark_treasury_yield * 100:.2f}%")
    print(f"BBB Credit Spread:         {credit_spread_bps} bps (+{credit_spread_bps / 100:.2f}%)")
    print(f"Final Reoffer Yield/Coupon:{coupon_rate * 100:.2f}%\n")

    res = syndicate_fee_waterfall(
        principal_offering,
        spread_bps=underwriting_gross_spread_bps,
        lead_manager_share=0.60,
        co_manager_share=0.30,
        selling_group_share=0.10,
    )

    print("=== Syndicate Fee Allocation & Proceeds Waterfall ===")
    print(f"Gross Proceeds:           ${res['gross_proceeds_cents'] / 100:,.2f}")
    print(f"Total Underwriting Spread:${res['total_spread_cents'] / 100:,.2f} ({underwriting_gross_spread_bps} bps)")
    print(f"Net Proceeds to Issuer:   ${res['net_proceeds_cents'] / 100:,.2f}\n")

    print("--- Syndicate Compensation Breakdown ---")
    print(f"  Lead Bookrunner (60%):  ${res['lead_manager_cents'] / 100:,.2f}")
    print(f"  Co-Managers (30%):      ${res['co_manager_cents'] / 100:,.2f}")
    print(f"  Selling Group (10%):    ${res['selling_group_cents'] / 100:,.2f}")
    syn_sum = res["lead_manager_cents"] + res["co_manager_cents"] + res["selling_group_cents"]
    matches_syn = syn_sum == res["total_spread_cents"]
    print(f"  Syndicate Sum:          ${syn_sum / 100:,.2f} (Matches total spread exactly: {matches_syn})\n")

    print("--- Functional Fee Component Decomposition ---")
    print(f"  Management Fee (20%):   ${res['management_fee_cents'] / 100:,.2f}")
    print(f"  Underwriting Fee (20%): ${res['underwriting_fee_cents'] / 100:,.2f}")
    print(f"  Selling Concession (60%):${res['selling_concession_cents'] / 100:,.2f}")
    func_sum = res["management_fee_cents"] + res["underwriting_fee_cents"] + res["selling_concession_cents"]
    matches_func = func_sum == res["total_spread_cents"]
    print(f"  Functional Sum:         ${func_sum / 100:,.2f} (Matches total spread exactly: {matches_func})")


main()
