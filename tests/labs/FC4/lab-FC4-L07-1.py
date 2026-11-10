"""Lab FC4-L07-1: Residual-income valuation vs DDM equivalence."""

from fractions import Fraction


def main() -> None:
    # Illustrative path from L06 (SIMULATED)
    b0 = Fraction(500)
    net_income = [Fraction(100), Fraction(115), Fraction(130), Fraction(145), Fraction(160)]
    dividends = [Fraction(40), Fraction(45), Fraction(50), Fraction(55), Fraction(65)]
    r = Fraction(10, 100)  # 10% cost of equity

    factor = Fraction(1) + r

    # 1. DDM Value with terminal book value B_N
    # V_0^DDM = sum_{t=1}^N D_t / (1+r)^t + B_N / (1+r)^N
    b = b0
    pv_divs = Fraction(0)
    disc = Fraction(1)
    for ni, d in zip(net_income, dividends, strict=True):
        disc *= factor
        pv_divs += d / disc
        b = b + ni - d
    b_n = b
    pv_bn = b_n / (factor ** len(dividends))
    v0_ddm = pv_divs + pv_bn

    # 2. Residual Income Valuation
    # RI_t = NetIncome_t - r * B_{t-1}
    # V_0^RI = B_0 + sum_{t=1}^N RI_t / (1+r)^t
    b_track = b0
    pv_ri = Fraction(0)
    disc = Fraction(1)
    ri_list: list[Fraction] = []
    charge_list: list[Fraction] = []

    for ni, d in zip(net_income, dividends, strict=True):
        charge = r * b_track
        ri = ni - charge
        disc *= factor
        pv_ri += ri / disc
        charge_list.append(charge)
        ri_list.append(ri)
        b_track = b_track + ni - d

    v0_ri = b0 + pv_ri

    print("SIMULATED Residual Income vs DDM Equivalence Under Clean Surplus")
    print(f"Cost of Equity r = {float(r):.2%}, Initial Book Value B_0 = ${float(b0):.2f}M")
    print("-" * 72)
    print(f"{'Year t':>8} {'Net Income':>12} {'Beg Book B_{t-1}':>18} {'Equity Charge':>16} {'Residual Income':>16}")
    print("-" * 72)

    b_disp = b0
    for t in range(1, len(net_income) + 1):
        ni = net_income[t - 1]
        chg = charge_list[t - 1]
        ri = ri_list[t - 1]
        print(f"{t:>8d} {float(ni):12.2f} {float(b_disp):18.2f} {float(chg):16.2f} {float(ri):16.2f}")
        b_disp = b_disp + ni - dividends[t - 1]

    print("-" * 72)
    print(f"DDM Sum of Discounted Dividends:     ${float(pv_divs):.4f}M ({pv_divs})")
    print(f"Discounted Terminal Book Value B_5:   ${float(pv_bn):.4f}M ({pv_bn})")
    print(f"Total DDM Equity Value V_0:          ${float(v0_ddm):.4f}M ({v0_ddm})")
    print(f"Initial Book Value B_0:              ${float(b0):.4f}M ({b0})")
    print(f"Sum of Discounted Residual Income:   ${float(pv_ri):.4f}M ({pv_ri})")
    print(f"Total Residual Income Value V_0:     ${float(v0_ri):.4f}M ({v0_ri})")
    print(f"Exact Difference (V_0^RI - V_0^DDM): {v0_ri - v0_ddm}")
    assert v0_ri == v0_ddm, "Preinreich-Lücke-Wallis identity must hold exactly"


main()
