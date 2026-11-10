"""Lab FC4-L03-1: Finite-horizon DDM with terminal value vs backward recursion."""

from fractions import Fraction


def main() -> None:
    # SIMULATED dividend path for an illustrative equity
    dividends = [Fraction(200, 100), Fraction(220, 100), Fraction(240, 100), Fraction(260, 100)]
    terminal_value = Fraction(4500, 100)  # TV_4 = $45.00
    r = Fraction(10, 100)  # 10% discount rate

    factor = Fraction(1) + r

    # 1. Direct forward discounting: V_0 = sum_{t=1}^N D_t / (1+r)^t + TV_N / (1+r)^N
    pv_divs = Fraction(0)
    disc = Fraction(1)
    for _t, d in enumerate(dividends, 1):
        disc *= factor
        pv_d = d / disc
        pv_divs += pv_d

    pv_tv = terminal_value / (factor ** len(dividends))
    direct_v0 = pv_divs + pv_tv

    # 2. Backward recursion: V_{t-1} = (D_t + V_t) / (1 + r)
    v_curr = terminal_value
    steps: list[tuple[int, Fraction, Fraction]] = []
    for t in reversed(range(1, len(dividends) + 1)):
        d = dividends[t - 1]
        v_prev = (d + v_curr) / factor
        steps.append((t - 1, d, v_prev))
        v_curr = v_prev

    recursive_v0 = v_curr
    assert direct_v0 == recursive_v0, "Direct PV must equal backward recursion exactly"

    print("SIMULATED Finite-Horizon DDM vs Backward Recursion")
    print(f"Discount rate r = {float(r):.2%}, Horizon N = {len(dividends)} years, TV_N = ${float(terminal_value):.2f}")
    print("-" * 65)
    print(f"{'Year t':>8} {'Dividend D_t':>16} {'Discounted D_t':>18} {'V_t (Backward)':>18}")
    print("-" * 65)

    disc_track = Fraction(1)
    for t, d in enumerate(dividends, 1):
        disc_track *= factor
        pv_step = d / disc_track
        # Lookup backward value at t
        b_val = next(v for step_t, _, v in steps if step_t == t) if t < len(dividends) else terminal_value
        print(f"{t:>8d} {float(d):16.2f} {float(pv_step):18.4f} {float(b_val):18.4f}")

    print("-" * 65)
    print(f"Direct PV of explicit dividends: ${float(pv_divs):.4f} ({pv_divs})")
    print(f"Discounted terminal value:       ${float(pv_tv):.4f} ({pv_tv})")
    print(f"Direct total equity value V_0:   ${float(direct_v0):.4f} ({direct_v0})")
    print(f"Backward recursive value V_0:    ${float(recursive_v0):.4f} ({recursive_v0})")
    print(f"Exact difference:                {direct_v0 - recursive_v0}")


main()
