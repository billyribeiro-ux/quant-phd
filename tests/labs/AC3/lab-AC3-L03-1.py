"""AC3 lab L03: Ohlson (1995) residual income valuation and earnings response coefficient.

SIMULATED: the valuation parameters, linear information dynamics coefficients, and firm
abnormal earnings paths are generated under the Ohlson (1995) framework. All calculations
use standard library float and math. No network; deterministic seed.
"""

from __future__ import annotations

SEED = 20261110


def ohlson_closed_form(
    book_value: float,
    abnormal_earnings: float,
    other_info: float,
    omega: float,
    gamma: float,
    cost_of_capital: float,
) -> tuple[float, float, float]:
    """Compute Ohlson (1995) closed-form price and valuation multipliers alpha_1, alpha_2.

    Returns (price, alpha_1, alpha_2).
    """
    r = cost_of_capital
    denom_1 = 1.0 + r - omega
    alpha_1 = omega / denom_1
    alpha_2 = (1.0 + r) / (denom_1 * (1.0 + r - gamma))
    price = book_value + alpha_1 * abnormal_earnings + alpha_2 * other_info
    return price, alpha_1, alpha_2


def ohlson_discounted_sum(
    book_value: float,
    abnormal_earnings: float,
    other_info: float,
    omega: float,
    gamma: float,
    cost_of_capital: float,
    horizon: int = 500,
) -> float:
    """Compute price by summing expected discounted abnormal earnings over horizon H.

    E_t[x_{t+tau}^a] is derived from the linear information dynamics:
    v_{t+k} = gamma^k * v_t
    x_{t+tau}^a = omega^tau * x_t^a + sum_{k=0}^{tau-1} omega^{tau-1-k} * gamma^k * v_t.
    """
    r = cost_of_capital
    cum_pv = 0.0

    # Current state expectations
    # E_t[x_{t+k}^a] and E_t[v_{t+k}]
    e_x = abnormal_earnings
    e_v = other_info

    for tau in range(1, horizon + 1):
        # Step forward one period:
        # E_t[x_{t+tau}^a] = omega * E_t[x_{t+tau-1}^a] + E_t[v_{t+tau-1}]
        next_x = omega * e_x + e_v
        next_v = gamma * e_v
        e_x = next_x
        e_v = next_v

        discount = (1.0 + r) ** (-tau)
        cum_pv += discount * e_x

    return book_value + cum_pv


def main() -> None:
    # Baseline parameters
    bv = 100.0
    x_a = 15.0
    v = 5.0
    r = 0.10
    gamma = 0.40

    print(f"seed {SEED} bv {bv:.1f} abnormal_earnings {x_a:.1f} other_info {v:.1f} r {r:.2f} gamma {gamma:.2f}")

    # 1. Numerical verification of closed-form against infinite-horizon sum
    omega_test = 0.60
    p_closed, a1, a2 = ohlson_closed_form(bv, x_a, v, omega_test, gamma, r)
    p_num = ohlson_discounted_sum(bv, x_a, v, omega_test, gamma, r, horizon=500)
    abs_err = abs(p_closed - p_num)

    print(f"omega {omega_test:.2f} : alpha_1 {a1:.4f} alpha_2 {a2:.4f}")
    print(f"closed_form_price {p_closed:.6f} numerical_price {p_num:.6f} abs_err {abs_err:.2e}")
    print(f"numerical_agreement_valid: {abs_err < 1e-9}")

    # 2. Monotonicity of ERC (alpha_1) with respect to persistence omega
    omegas = [0.0, 0.20, 0.40, 0.60, 0.80, 0.95]
    print("\nmonotonicity_across_persistence:")
    print(f"{'omega':6s} | {'alpha_1 (ERC)':13s} | {'alpha_2':8s} | {'Price':9s}")
    print("-" * 45)

    alpha_1_values: list[float] = []
    for om in omegas:
        p, a1_val, a2_val = ohlson_closed_form(bv, x_a, v, om, gamma, r)
        alpha_1_values.append(a1_val)
        print(f"{om:6.2f} | {a1_val:13.4f} | {a2_val:8.4f} | {p:9.2f}")

    # Check strict monotonicity: higher omega -> strictly higher alpha_1
    is_strictly_increasing = all(alpha_1_values[i] < alpha_1_values[i + 1] for i in range(len(alpha_1_values) - 1))
    print("-" * 45)
    print(f"erc_strictly_increasing_in_persistence: {is_strictly_increasing}")

    # Pure transitory shock (omega = 0) -> alpha_1 = 0 (abnormal earnings add zero future excess)
    print(f"transitory_alpha_1_zero: {alpha_1_values[0] == 0.0}")


main()
