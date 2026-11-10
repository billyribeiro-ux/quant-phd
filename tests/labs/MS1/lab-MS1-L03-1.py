"""Lab MS1-L03-1: Discrete inventory control and optimal quote skewing.

Dynamic programming by backward induction on a finite inventory grid.
Solves the dealer quote-setting problem with quadratic inventory penalties in exact Fraction arithmetic.
Demonstrates that optimal quote shift is negatively related to inventory level (grade C finite enumeration).
"""

from __future__ import annotations

from fractions import Fraction


def solve_inventory_dp() -> tuple[dict[int, Fraction], dict[int, Fraction], dict[int, Fraction], dict[int, Fraction]]:
    """Solve 2-period inventory DP on grid I in {-2, -1, 0, 1, 2}."""
    inventories = [-2, -1, 0, 1, 2]
    shifts = [Fraction(-1, 1), Fraction(-1, 2), Fraction(0, 1), Fraction(1, 2), Fraction(1, 1)]
    c0 = Fraction(1, 2)  # baseline half-spread

    # Terminal penalty: V_2(I) = I^2
    v_terminal = {i: Fraction(i**2, 1) for i in inventories}

    v_current = v_terminal
    policy_period1: dict[int, Fraction] = {}
    v_period1: dict[int, Fraction] = {}
    policy_period0: dict[int, Fraction] = {}
    v_period0: dict[int, Fraction] = {}

    for t in [1, 0]:
        next_v: dict[int, Fraction] = {}
        opt_shift: dict[int, Fraction] = {}
        for inv in inventories:
            best_cost: Fraction | None = None
            best_delta: Fraction | None = None
            for delta in shifts:
                # Order arrival probabilities linear in quote shift
                p_buy = Fraction(1, 2) - Fraction(1, 4) * delta
                p_sell = Fraction(1, 2) + Fraction(1, 4) * delta

                # Clamped transitions
                inv_after_buy = max(-2, inv - 1)
                inv_after_sell = min(2, inv + 1)

                # Expected spread revenue
                revenue = p_buy * (c0 + delta) + p_sell * (c0 - delta)

                # Period holding cost + expected net continuation cost
                holding = Fraction(1, 2) * Fraction(inv**2, 1)
                expected_continuation = p_buy * v_current[inv_after_buy] + p_sell * v_current[inv_after_sell]
                total_cost = holding - revenue + expected_continuation

                if best_cost is None or total_cost < best_cost:
                    best_cost = total_cost
                    best_delta = delta

            assert best_cost is not None and best_delta is not None
            next_v[inv] = best_cost
            opt_shift[inv] = best_delta

        v_current = next_v
        if t == 1:
            policy_period1 = opt_shift
            v_period1 = next_v
        else:
            policy_period0 = opt_shift
            v_period0 = next_v

    return policy_period0, v_period0, policy_period1, v_period1


def main() -> None:
    pol0, v0, pol1, v1 = solve_inventory_dp()

    print("Inventory model: quadratic holding penalty and finite grid backward induction")
    print("Period 1 value function and optimal quote shift:")
    for inv in sorted(pol1):
        print(f"  I = {inv:+d}: V_1(I) = {v1[inv]} ({float(v1[inv]):.4f}), delta*_1(I) = {float(pol1[inv]):+.2f}")

    print("Period 0 value function and optimal quote shift:")
    for inv in sorted(pol0):
        print(f"  I = {inv:+d}: V_0(I) = {v0[inv]} ({float(v0[inv]):.4f}), delta*_0(I) = {float(pol0[inv]):+.2f}")

    print("Symmetry and monotonicity checks:")
    sym_shift = all(pol0[i] == -pol0[-i] for i in [1, 2])
    sym_val = all(v0[i] == v0[-i] for i in [1, 2])
    print(f"  Quote skew anti-symmetry delta*(I) == -delta*(-I): {sym_shift}")
    print(f"  Value function symmetry V(I) == V(-I): {sym_val}")
    print(f"  Quote shift at zero inventory: {pol0[0]}")


main()
