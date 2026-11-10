"""Lab FC4-L08-1: Valuation multiples: P/E and EV/EBITDA bridge to equity."""

from fractions import Fraction


def main() -> None:
    # Illustrative target firm and peer multiples (SIMULATED)
    # Target fundamentals
    shares = Fraction(20)  # 20M shares
    net_income = Fraction(100)  # $100M NI -> EPS = $5.00
    ebitda = Fraction(240)  # $240M EBITDA
    total_debt = Fraction(300)  # $300M debt
    cash = Fraction(60)  # $60M cash
    net_debt = total_debt - cash  # $240M net debt

    eps = net_income / shares

    # Peer group multiple benchmarks
    peer_pe = Fraction(18)  # 18.0x P/E
    peer_ev_ebitda = Fraction(10)  # 10.0x EV/EBITDA

    # 1. P/E Implied Valuation (Equity level direct)
    implied_equity_from_pe = net_income * peer_pe
    implied_price_from_pe = implied_equity_from_pe / shares
    assert implied_price_from_pe == eps * peer_pe

    # 2. EV/EBITDA Implied Valuation (Enterprise level -> Net Debt Bridge -> Equity level)
    implied_ev = ebitda * peer_ev_ebitda
    implied_equity_from_ev = implied_ev - net_debt
    implied_price_from_ev = implied_equity_from_ev / shares

    print("SIMULATED Multiples-Based Valuation & Enterprise-to-Equity Bridge")
    print(f"Target Fundamentals: Net Income=${net_income}M, EBITDA=${ebitda}M")
    print(f"Shares={shares}M (EPS=${float(eps):.2f})")
    print(f"Capital Structure: Total Debt=${total_debt}M, Cash=${cash}M, Net Debt=${net_debt}M")
    print("-" * 72)
    print(f"{'Method / Benchmark':<24} {'Metric':>12} {'Multiple':>10} {'Implied Val':>14} {'Per Share':>10}")
    print("-" * 72)
    pe_row = (
        f"{'P/E Direct (Equity)':<24} {float(net_income):11.1f}M {float(peer_pe):9.1f}x "
        f"${float(implied_equity_from_pe):12.2f}M ${float(implied_price_from_pe):8.2f}"
    )
    print(pe_row)
    ev_row = (
        f"{'EV/EBITDA (Enterprise)':<24} {float(ebitda):11.1f}M {float(peer_ev_ebitda):9.1f}x "
        f"${float(implied_ev):12.2f}M {'N/A':>10}"
    )
    print(ev_row)
    debt_row = f"{'Less Net Debt Bridge':<24} {float(-net_debt):11.1f}M {'-':>10} ${float(-net_debt):12.2f}M {'-':>10}"
    print(debt_row)
    eq_row = (
        f"{'Implied Equity via EV':<24} {'-':>12} {'-':>10} "
        f"${float(implied_equity_from_ev):12.2f}M ${float(implied_price_from_ev):8.2f}"
    )
    print(eq_row)
    print("-" * 72)
    spread = float(implied_price_from_ev - implied_price_from_pe)
    print(f"Valuation Spread (EV bridge price vs P/E price): ${spread:.2f}")


main()
