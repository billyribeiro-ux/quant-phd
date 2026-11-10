"""Lab L05-1: Sequence-of-returns risk in accumulation versus decumulation.

Compares two identical return paths with inverted ordering under pure accumulation
(zero cash flows) versus retirement decumulation (annual withdrawals).
Standard library only. All inputs are SIMULATED.
"""


def main() -> None:
    initial_wealth = 1_000_000.0  # dollars
    annual_withdrawal = 55_000.0  # $55k constant real withdrawal (5.5% initial rate)

    # 25-year return sequences
    # Sequence A: Bear market early, bull market late
    early_bear = [-0.18, -0.12, -0.06, 0.02, 0.04]
    mid_and_late = [
        0.07,
        0.09,
        0.12,
        0.08,
        0.11,
        0.14,
        0.06,
        0.10,
        0.13,
        0.09,
        0.08,
        0.12,
        0.15,
        0.07,
        0.11,
        0.10,
        0.13,
        0.08,
        0.14,
        0.12,
    ]
    returns_a = early_bear + mid_and_late
    # Sequence B: Bull market early, bear market late (exact reversal)
    returns_b = list(reversed(returns_a))

    assert len(returns_a) == len(returns_b) == 25

    # -------------------------------------------------------------
    # Case 1: Accumulation (zero withdrawals)
    # -------------------------------------------------------------
    wealth_acc_a = initial_wealth
    for r in returns_a:
        wealth_acc_a *= 1.0 + r

    wealth_acc_b = initial_wealth
    for r in returns_b:
        wealth_acc_b *= 1.0 + r

    # -------------------------------------------------------------
    # Case 2: Decumulation ($55,000 withdrawal at beginning of year)
    # -------------------------------------------------------------
    wealth_dec_a = initial_wealth
    ruin_year_a = 0
    for t, r in enumerate(returns_a, start=1):
        wealth_dec_a -= annual_withdrawal
        if wealth_dec_a <= 0.0:
            ruin_year_a = t
            wealth_dec_a = 0.0
            break
        wealth_dec_a *= 1.0 + r
        if wealth_dec_a <= 0.0:
            ruin_year_a = t
            wealth_dec_a = 0.0
            break

    wealth_dec_b = initial_wealth
    ruin_year_b = 0
    for t, r in enumerate(returns_b, start=1):
        wealth_dec_b -= annual_withdrawal
        if wealth_dec_b <= 0.0:
            ruin_year_b = t
            wealth_dec_b = 0.0
            break
        wealth_dec_b *= 1.0 + r
        if wealth_dec_b <= 0.0:
            ruin_year_b = t
            wealth_dec_b = 0.0
            break

    print("Accumulation Phase (No withdrawals):")
    print(f"  Sequence A (Bear First): ${round(wealth_acc_a):,}")
    print(f"  Sequence B (Bull First): ${round(wealth_acc_b):,}")
    print(f"  Difference: ${round(wealth_acc_a - wealth_acc_b):,}")

    print("\nDecumulation Phase ($55k annual withdrawals):")
    status_a = f"RUINED in Year {ruin_year_a}" if ruin_year_a > 0 else f"${round(wealth_dec_a):,}"
    status_b = f"RUINED in Year {ruin_year_b}" if ruin_year_b > 0 else f"${round(wealth_dec_b):,}"
    print(f"  Sequence A (Bear First): {status_a}")
    print(f"  Sequence B (Bull First): {status_b}")


main()
