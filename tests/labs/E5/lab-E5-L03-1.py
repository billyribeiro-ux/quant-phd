"""E5 L03 lab 1: the Solow capital recursion, its steady state, and the comparative statics of the steady state.

Inputs are illustrative parameters, not data: output per worker y = k^alpha with alpha = 0.3, a saving rate
s = 0.2, a depreciation rate delta = 0.05 per period, a population growth rate n = 0.01 per period, and an
initial capital stock per worker k_0 = 1. Every quantity is a Decimal computed at 60 significant digits, so each
run prints the same lines. No random draws are used.

Part A: the closed-form steady state k* = (s/(n + delta))^(1/(1 - alpha)), and the residual of the recursion at k*.
Part B: the recursion k_{t+1} = (s k_t^alpha + (1 - delta) k_t)/(1 + n) iterated for 1000 periods, its gap to k*,
and the first period at which the gap is below 1e-12.
Part C: the sign of g(k) - k on a grid of 50 capital values, against the side of k* on which each value lies.
Part D: the derivatives dk*/ds and dk*/ddelta from the implicit-function theorem, against central differences
with step 1e-10.
Part E: the derivative of k* with respect to the population growth rate n, against its derivative with respect to
delta.
"""

from __future__ import annotations

from decimal import Decimal, getcontext

getcontext().prec = 60

ALPHA = Decimal("0.3")
SAVING = Decimal("0.2")
DEPRECIATION = Decimal("0.05")
GROWTH = Decimal("0.01")
K0 = Decimal(1)
PERIODS = 1000
STEP = Decimal("1e-10")
TOLERANCE = Decimal("1e-12")
REPORT_PERIODS = (0, 1, 2, 5, 10, 25, 50, 100, 200, 500, 1000)


def power(base: Decimal, exponent: Decimal) -> Decimal:
    """The positive number base^exponent, for base > 0."""
    return base**exponent


def steady_state(alpha: Decimal, saving: Decimal, depreciation: Decimal, growth: Decimal) -> Decimal:
    """The positive steady state k* = (s/(n + delta))^(1/(1 - alpha)) of the recursion, in capital per worker."""
    return power(saving / (growth + depreciation), 1 / (1 - alpha))


def step(k: Decimal, alpha: Decimal, saving: Decimal, depreciation: Decimal, growth: Decimal) -> Decimal:
    """One period of the recursion, g(k) = (s k^alpha + (1 - delta) k)/(1 + n), for capital per worker k > 0."""
    return (saving * power(k, alpha) + (1 - depreciation) * k) / (1 + growth)


def part_a(kstar: Decimal) -> None:
    """Print the closed-form steady state and the residual of the recursion at it."""
    print("Part A: closed-form steady state")
    print(f"steady_state_capital {kstar:.10f}")
    print(f"output_per_worker_at_steady_state {power(kstar, ALPHA):.10f}")
    residual = step(kstar, ALPHA, SAVING, DEPRECIATION, GROWTH) - kstar
    print(f"residual_at_steady_state {residual:.3e}")


def part_b(kstar: Decimal) -> None:
    """Iterate the recursion from k_0, print its gap to k*, and test the ordering of successive iterates."""
    print("Part B: recursion from k_0 against the steady state")
    k = K0
    ordered = True
    first_within = -1
    if abs(k - kstar) < TOLERANCE:
        first_within = 0
    print(f"period 0 capital {k:.10f} gap {kstar - k:.10f}")
    for t in range(1, PERIODS + 1):
        nxt = step(k, ALPHA, SAVING, DEPRECIATION, GROWTH)
        if k < kstar:
            ordered = ordered and k < nxt < kstar
        elif k > kstar:
            ordered = ordered and kstar < nxt < k
        k = nxt
        if first_within < 0 and abs(k - kstar) < TOLERANCE:
            first_within = t
        if t in REPORT_PERIODS:
            print(f"period {t} capital {k:.10f} gap {kstar - k:.10f}")
    print(f"iterates_move_toward_steady_state {ordered}")
    print(f"first_period_gap_below_tolerance {first_within}")


def part_c(kstar: Decimal) -> None:
    """Check the sign of g(k) - k on a grid of 50 capital values against the side of k* each value lies on."""
    print("Part C: sign of g(k) - k on a grid of 50 capital values")
    grid = [Decimal(i) / 5 for i in range(1, 51)]
    below = 0
    mismatches = 0
    for k in grid:
        nxt = step(k, ALPHA, SAVING, DEPRECIATION, GROWTH)
        if k < kstar:
            below += 1
        if (nxt > k) != (k < kstar):
            mismatches += 1
    print(f"grid_points_below_steady_state {below}")
    print(f"grid_points_above_steady_state {len(grid) - below}")
    print(f"sign_mismatches {mismatches}")


def part_d(kstar: Decimal) -> None:
    """Compare the implicit-function derivatives of k* with central differences in s and in delta."""
    print("Part D: comparative statics of k* against central differences")
    dk_ds = kstar / ((1 - ALPHA) * SAVING)
    dk_ddelta = -kstar / ((1 - ALPHA) * (GROWTH + DEPRECIATION))
    fd_ds = (
        steady_state(ALPHA, SAVING + STEP, DEPRECIATION, GROWTH)
        - steady_state(ALPHA, SAVING - STEP, DEPRECIATION, GROWTH)
    ) / (2 * STEP)
    fd_ddelta = (
        steady_state(ALPHA, SAVING, DEPRECIATION + STEP, GROWTH)
        - steady_state(ALPHA, SAVING, DEPRECIATION - STEP, GROWTH)
    ) / (2 * STEP)
    rel_s = abs(fd_ds - dk_ds) / abs(dk_ds)
    rel_delta = abs(fd_ddelta - dk_ddelta) / abs(dk_ddelta)
    print(f"ift_dk_ds {dk_ds:.10f}")
    print(f"finite_difference_dk_ds {fd_ds:.10f}")
    print(f"relative_error_dk_ds {rel_s:.3e}")
    print(f"ift_dk_ddelta {dk_ddelta:.10f}")
    print(f"finite_difference_dk_ddelta {fd_ddelta:.10f}")
    print(f"relative_error_dk_ddelta {rel_delta:.3e}")
    print(f"within_tolerance {rel_s < TOLERANCE and rel_delta < TOLERANCE}")
    elasticity = SAVING / kstar * dk_ds
    print(f"elasticity_of_k_with_respect_to_s {elasticity:.10f}")


def part_e() -> None:
    """Compare the derivative of k* with respect to n with its derivative with respect to delta."""
    print("Part E: population growth and depreciation act through n + delta")
    base = steady_state(ALPHA, SAVING, DEPRECIATION, GROWTH)
    dn = (
        steady_state(ALPHA, SAVING, DEPRECIATION, GROWTH + STEP)
        - steady_state(ALPHA, SAVING, DEPRECIATION, GROWTH - STEP)
    ) / (2 * STEP)
    ddelta = (
        steady_state(ALPHA, SAVING, DEPRECIATION + STEP, GROWTH)
        - steady_state(ALPHA, SAVING, DEPRECIATION - STEP, GROWTH)
    ) / (2 * STEP)
    print(f"finite_difference_dk_dn {dn:.10f}")
    print(f"finite_difference_dk_ddelta_again {ddelta:.10f}")
    print(f"difference_between_them {abs(dn - ddelta):.3e}")
    print(f"equal_within_tolerance {abs(dn - ddelta) < TOLERANCE * abs(base)}")


def main() -> None:
    """Print Parts A to E. Each line is a fixed string, a Decimal at a fixed precision, or a boolean."""
    kstar = steady_state(ALPHA, SAVING, DEPRECIATION, GROWTH)
    part_a(kstar)
    part_b(kstar)
    part_c(kstar)
    part_d(kstar)
    part_e()


main()
