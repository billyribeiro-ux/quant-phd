"""Lab FC4-L05-1: Free cash flow to equity (FCFE) identity and equity valuation."""

from fractions import Fraction


def main() -> None:
    # 5-year illustrative path for a company (SIMULATED)
    # FCFE_t = NetIncome_t + D&A_t - Capex_t - DeltaNWC_t + NetBorrowing_t
    years = [1, 2, 3, 4, 5]
    net_income = [Fraction(100), Fraction(115), Fraction(130), Fraction(145), Fraction(160)]
    da = [Fraction(30), Fraction(35), Fraction(40), Fraction(45), Fraction(50)]
    capex = [Fraction(45), Fraction(50), Fraction(55), Fraction(60), Fraction(65)]
    delta_nwc = [Fraction(10), Fraction(12), Fraction(15), Fraction(14), Fraction(15)]
    net_borrowing = [Fraction(15), Fraction(18), Fraction(20), Fraction(22), Fraction(25)]

    ke = Fraction(95, 1000)  # Cost of equity k_e = 9.5%
    g = Fraction(30, 1000)  # Terminal growth rate g = 3.0%
    shares = Fraction(10)  # 10M shares outstanding

    fcfe_list: list[Fraction] = []
    for ni, d_a, cap, nwc, nb in zip(net_income, da, capex, delta_nwc, net_borrowing, strict=True):
        fcfe = ni + d_a - cap - nwc + nb
        fcfe_list.append(fcfe)

    print("SIMULATED 5-Year FCFE Statement (Million USD)")
    print("-" * 75)
    print(f"{'Year':>5} {'Net Income':>12} {'D&A':>8} {'Capex':>8} {'DeltaNWC':>10} {'Net Borrow':>12} {'FCFE':>10}")
    print("-" * 75)
    for y, ni, d_a, cap, nwc, nb, f in zip(
        years, net_income, da, capex, delta_nwc, net_borrowing, fcfe_list, strict=True
    ):
        print(
            f"{y:>5d} {float(ni):12.2f} {float(d_a):8.2f} {float(cap):8.2f} "
            f"{float(nwc):10.2f} {float(nb):12.2f} {float(f):10.2f}"
        )
    print("-" * 75)

    # Discount explicit FCFE at cost of equity k_e
    one_plus_k = Fraction(1) + ke
    pv_fcfe = Fraction(0)
    disc = Fraction(1)
    for f in fcfe_list:
        disc *= one_plus_k
        pv_fcfe += f / disc

    # Terminal value of equity at N = 5
    terminal_fcfe = fcfe_list[-1] * (Fraction(1) + g)
    tv = terminal_fcfe / (ke - g)
    pv_tv = tv / (one_plus_k ** len(fcfe_list))
    total_equity_val = pv_fcfe + pv_tv
    val_per_share = total_equity_val / shares

    print(f"Cost of Equity k_e:              {float(ke):.2%}")
    print(f"Terminal Growth g:               {float(g):.2%}")
    print(f"PV of explicit 5-yr FCFE:        ${float(pv_fcfe):.2f}M")
    print(f"Discounted Terminal Value:       ${float(pv_tv):.2f}M")
    print(f"Total Equity Value:              ${float(total_equity_val):.2f}M")
    print(f"Value Per Share ({shares}M shares):    ${float(val_per_share):.2f}")


main()
