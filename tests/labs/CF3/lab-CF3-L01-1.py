"""CF3 lab L01-1: Cash dividends vs share repurchases and payout irrelevance.

Model: Exact closed-form payout equivalence under perfect capital markets
and valuation wedge under differential personal taxation.
Standard library only; no external network access.
Demonstrates wealth conservation across cash dividends and repurchases,
ex-dividend price drop ratio, and the dividend tax penalty.
"""

from __future__ import annotations

from fractions import Fraction


def payout_comparison(
    shares_initial: int,
    price_initial: Fraction,
    earnings_payout: Fraction,
    tau_div: Fraction,
    tau_cg: Fraction,
) -> dict[str, Fraction]:
    """Compare cash dividend versus share repurchase under perfect markets and tax asymmetry."""
    # Pre-payout equity value
    v_pre = Fraction(shares_initial, 1) * price_initial

    # Policy 1: Cash dividend
    div_per_share = earnings_payout / Fraction(shares_initial, 1)
    # Under MM, ex-dividend price drops by exact cash dividend per share
    price_ex_div_mm = price_initial - div_per_share
    # After-tax cash received by an investor holding 1 share
    cash_net_div = div_per_share * (Fraction(1, 1) - tau_div)
    wealth_div_mm = price_ex_div_mm + cash_net_div

    # Policy 2: Share repurchase at fair market price (price_initial)
    # Number of shares repurchased
    shares_repurchased = earnings_payout / price_initial
    shares_remaining = Fraction(shares_initial, 1) - shares_repurchased
    # Total equity value remaining in firm after payout
    v_post_repurchase = v_pre - earnings_payout
    price_post_repurchase = v_post_repurchase / shares_remaining

    # Capital gains tax on selling shares in repurchase (assuming zero basis for clean benchmark)
    cash_net_repurchase = earnings_payout * (Fraction(1, 1) - tau_cg)

    return {
        "v_pre": v_pre,
        "div_per_share": div_per_share,
        "price_ex_div_mm": price_ex_div_mm,
        "wealth_div_mm": wealth_div_mm,
        "shares_repurchased": shares_repurchased,
        "shares_remaining": shares_remaining,
        "price_post_repurchase": price_post_repurchase,
        "cash_net_div": cash_net_div,
        "cash_net_repurchase": cash_net_repurchase,
    }


def main() -> None:
    print("CF3 Lab L01-1: Cash Dividends vs. Share Repurchases & Payout Irrelevance")
    print("======================================================================")

    # Initial firm: 1,000,000 shares at $50.00 each = $50,000,000 equity value
    shares_0 = 1_000_000
    p_0 = Fraction(50, 1)
    payout = Fraction(5_000_000, 1)  # $5,000,000 distributed (10% payout)

    # Scenario A: Zero taxes (Pure MM 1961 benchmark)
    res_mm = payout_comparison(shares_0, p_0, payout, Fraction(0, 1), Fraction(0, 1))

    print("Scenario A: Frictionless Markets (MM 1961 Payout Irrelevance)")
    print(f"  Pre-payout equity market value:  ${float(res_mm['v_pre']):,.2f}")
    print(f"  Total payout distributed:       ${float(payout):,.2f}")
    print(f"  Cash Dividend per share:         ${float(res_mm['div_per_share']):.2f}")
    print(f"  Ex-dividend share price:         ${float(res_mm['price_ex_div_mm']):.2f}")
    print(f"  Ex-dividend price drop:          ${float(p_0 - res_mm['price_ex_div_mm']):.2f} (exact match to dividend)")
    print(f"  Investor wealth per share (div): ${float(res_mm['wealth_div_mm']):.2f} (equals initial $50.00)")
    print(f"  Shares repurchased (buyback):    {float(res_mm['shares_repurchased']):,.0f}")
    print(f"  Post-repurchase share price:     ${float(res_mm['price_post_repurchase']):.2f} (remains $50.00)")
    print(f"  Total post-payout equity value:  ${float(res_mm['v_pre'] - payout):,.2f}")
    print(f"  Wealth conservation confirmed:   {res_mm['price_post_repurchase'] == p_0}")

    # Scenario B: Differential taxation (Dividend tax 25%, Capital gains tax 15%)
    tau_d = Fraction(25, 100)
    tau_cg = Fraction(15, 100)
    res_tax = payout_comparison(shares_0, p_0, payout, tau_d, tau_cg)

    print("\nScenario B: Differential Taxation (tau_d = 25%, tau_cg = 15%)")
    print(f"  After-tax cash from dividend:    ${float(res_tax['cash_net_div']):.2f} per share")
    print(f"  Total after-tax payout (div):    ${float(res_tax['cash_net_div'] * shares_0):,.2f}")
    print(f"  Total after-tax payout (buyback):${float(res_tax['cash_net_repurchase']):,.2f}")
    tax_wedge = res_tax["cash_net_repurchase"] - (res_tax["cash_net_div"] * Fraction(shares_0, 1))
    print(f"  Buyback tax savings wedge:       ${float(tax_wedge):,.2f} ({float(tax_wedge / payout):.2%} of payout)")


main()
