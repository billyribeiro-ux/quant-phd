"""CF1 L04 lab 1: the NPV profile of a project with two sign changes, and an IRR-versus-NPV ranking conflict.

SIMULATED: every cash flow is a fixed input written here. None is any firm's cash flow.
Units: money in cents, with t = 0 first and one period per year. Rates are decimals per year.
The root search scans a grid of rates from -0.5 to 1.0 in steps of 0.0001 for sign changes of the NPV profile,
then bisects each bracket, so it finds every sign change on the grid. The closed form uses x = 1 / (1 + r) and
the factorization of the two-sign-change project shown on the page. The lab draws no random numbers.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

PROJECT_P: tuple[int, ...] = (-10_000_000, 23_000_000, -13_100_000)  # outlay, inflow, then a cost at t = 2
PROJECT_A: tuple[int, ...] = (-10_000_000, 13_000_000)  # mutually exclusive with B
PROJECT_B: tuple[int, ...] = (-20_000_000, 25_000_000)
COST_OF_CAPITAL = 0.10
GRID_LOW = -0.5
GRID_HIGH = 1.0
GRID_STEP = 0.0001


def npv(flows: Sequence[float], rate: float) -> float:
    """Net present value in cents: the sum of flows[t] / (1 + rate)**t; rate is per year and must exceed -1."""
    if rate <= -1.0:
        raise ValueError(f"rate {rate} must exceed -1")
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))


def bisect(f: Callable[[float], float], low: float, high: float) -> float:
    """A root of f in [low, high], given that f(low) and f(high) have opposite signs; the bracket narrows to 1e-12."""
    f_low = f(low)
    for _ in range(200):
        mid = 0.5 * (low + high)
        f_mid = f(mid)
        if f_mid == 0.0 or high - low < 1e-12:
            return mid
        if f_low * f_mid < 0.0:
            high = mid
        else:
            low, f_low = mid, f_mid
    return 0.5 * (low + high)


def all_roots(flows: Sequence[float]) -> list[float]:
    """Every sign change of the NPV profile on the grid, each bisected; duplicates within 1e-7 are merged."""

    def f(rate: float) -> float:
        return npv(flows, rate)

    steps = round((GRID_HIGH - GRID_LOW) / GRID_STEP)
    grid = [GRID_LOW + i * GRID_STEP for i in range(steps + 1)]
    values = [f(r) for r in grid]
    roots: list[float] = []
    for i in range(steps + 1):
        if values[i] == 0.0:
            candidate = grid[i]
        elif i < steps and values[i] * values[i + 1] < 0.0:
            candidate = bisect(f, grid[i], grid[i + 1])
        else:
            continue
        if not roots or abs(candidate - roots[-1]) > 1e-7:
            roots.append(candidate)
    return roots


def sign_label(value: float) -> str:
    """Text sign of an NPV in cents: '+' above 1e-6, '-' below -1e-6, else '0' (a root, to float precision)."""
    return "+" if value > 1e-6 else "-" if value < -1e-6 else "0"


def usd(cents: float) -> str:
    """Cents shown as dollars with two decimals and no thousands separator; a value within 1e-6 cents is zero."""
    dollars = 0.0 if abs(cents) < 1e-6 else cents / 100
    return f"{dollars:.2f}"


def closed_form_p(rate: float) -> float:
    """NPV of PROJECT_P in cents from the factorization -200000 * (11x - 10) * (6x - 5), with x = 1 / (1 + rate)."""
    x = 1.0 / (1.0 + rate)
    return -200_000.0 * (11.0 * x - 10.0) * (6.0 * x - 5.0)


def main() -> None:
    print("PROJECT_P cash flows in cents, t = 0, 1, 2:", ", ".join(str(cf) for cf in PROJECT_P))
    print("NPV profile of PROJECT_P (USD), sign on the profile")
    for rate in (0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
        value = npv(PROJECT_P, rate)
        print(f"rate {rate:.2f}  NPV {usd(value)}  sign {sign_label(value)}")

    roots_p = all_roots(PROJECT_P)
    print(f"sign changes of the NPV profile on the grid: {len(roots_p)}")
    for i, root in enumerate(roots_p, start=1):
        print(f"IRR root {i} by grid scan and bisection: {root:.6f}")
    closed = [1.0 / x - 1.0 for x in (10.0 / 11.0, 5.0 / 6.0)]
    print(f"closed-form roots, r = 1/x - 1 at x = 10/11 and x = 5/6: {closed[0]:.6f}, {closed[1]:.6f}")
    gap = max(abs(npv(PROJECT_P, r) - closed_form_p(r)) for r in (-0.4, 0.0, 0.05, 0.15, 0.5, 2.0))
    print(f"largest absolute gap, factorization against direct NPV, cents: {gap:.6f}")
    print(f"NPV of PROJECT_P at the cost of capital {COST_OF_CAPITAL:.2f}: {usd(npv(PROJECT_P, COST_OF_CAPITAL))} USD")

    print("IRR ranking against NPV ranking for mutually exclusive projects")
    roots_a = all_roots(PROJECT_A)
    roots_b = all_roots(PROJECT_B)
    print(f"IRR of A: {roots_a[0]:.6f}; IRR of B: {roots_b[0]:.6f}")
    higher_irr = "A" if roots_a[0] > roots_b[0] else "B"
    print(f"project with the higher IRR: {higher_irr}")
    npv_a = npv(PROJECT_A, COST_OF_CAPITAL)
    npv_b = npv(PROJECT_B, COST_OF_CAPITAL)
    print(f"NPV of A at {COST_OF_CAPITAL:.2f}: {usd(npv_a)} USD; NPV of B: {usd(npv_b)} USD")
    higher_npv = "A" if npv_a > npv_b else "B"
    print(f"project with the higher NPV at {COST_OF_CAPITAL:.2f}: {higher_npv}")

    difference = tuple(b - a for a, b in zip(PROJECT_A, PROJECT_B, strict=True))
    crossover = all_roots(difference)
    print(f"difference B minus A in cents: {', '.join(str(cf) for cf in difference)}")
    print(f"crossover rate, the IRR of the difference: {crossover[0]:.6f}")
    print("rate  NPV A (USD)  NPV B (USD)  higher NPV")
    for rate in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
        va = npv(PROJECT_A, rate)
        vb = npv(PROJECT_B, rate)
        leader = "tie" if abs(va - vb) <= 1e-6 else "A" if va > vb else "B"
        print(f"{rate:.2f}  {usd(va)}  {usd(vb)}  {leader}")


main()
