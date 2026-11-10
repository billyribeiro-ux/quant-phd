"""Lab FC4-L06-1: Clean-surplus relation and book value roll."""

from fractions import Fraction


def main() -> None:
    # 5-year accounting roll under clean surplus (SIMULATED)
    # B_t = B_{t-1} + NetIncome_t - Dividends_t
    b0 = Fraction(500)  # Initial book value $500M
    net_income = [Fraction(100), Fraction(115), Fraction(130), Fraction(145), Fraction(160)]
    dividends = [Fraction(40), Fraction(45), Fraction(50), Fraction(55), Fraction(65)]

    book_values: list[Fraction] = [b0]
    retained_earnings: list[Fraction] = []

    for ni, d in zip(net_income, dividends, strict=True):
        retained = ni - d
        retained_earnings.append(retained)
        b_next = book_values[-1] + retained
        book_values.append(b_next)

    # Check cumulative clean surplus identity: B_N = B_0 + sum(NI) - sum(D)
    sum_ni = sum(net_income)
    sum_divs = sum(dividends)
    b_n_formula = b0 + sum_ni - sum_divs
    assert book_values[-1] == b_n_formula, "Cumulative clean surplus identity must hold exactly"

    print("SIMULATED Clean-Surplus Book Value Roll (Million USD)")
    print(f"Beginning Book Value B_0: ${float(b0):.2f}M")
    print("-" * 65)
    print(f"{'Year t':>8} {'Net Income':>14} {'Dividends':>12} {'Retained Earn':>14} {'Ending B_t':>13}")
    print("-" * 65)

    for t in range(1, len(net_income) + 1):
        ni = net_income[t - 1]
        d = dividends[t - 1]
        re = retained_earnings[t - 1]
        b_t = book_values[t]
        print(f"{t:>8d} {float(ni):14.2f} {float(d):12.2f} {float(re):14.2f} {float(b_t):13.2f}")

    print("-" * 65)
    print(f"Cumulative Net Income sum(NI_t):      ${float(sum_ni):.2f}M")
    print(f"Cumulative Dividends sum(D_t):        ${float(sum_divs):.2f}M")
    print(f"Cumulative Retained Earnings:         ${float(sum_ni - sum_divs):.2f}M")
    print(f"Final Book Value B_5 (Rolled):        ${float(book_values[-1]):.2f}M")
    print(f"Final Book Value B_5 (Cumulative Id): ${float(b_n_formula):.2f}M")
    print(f"Identity Difference:                  {book_values[-1] - b_n_formula}")


main()
