"""M7 L07 lab 1: backward recursion for a finite-horizon toy problem, checked against brute-force enumeration.

SIMULATED: a fixed toy problem with integer inputs. It is not market data and it uses no random draws. Wealth and
consumption are whole cents. Period rewards and the bequest are integers in utils, so every value is
exact and no floating-point error enters.

The problem has H = 4 periods, t = 0 to 3. The state at time t is wealth W in {0, 100, 200, 300, 400} cents. The
action is consumption c, a multiple of 100 cents with c <= W. Next wealth is W - c. The period reward is u(c) from the
table below. The reward at time H = 4 is the bequest W // 100 utils.

Part A prints the value table V_t(W) from the backward recursion, for t = 0 to 4.
Part B enumerates every consumption sequence of length H - t from each state, takes the best total, and compares it
with the recursion. It prints the number of feasible sequences checked from (0, 400).
Part C prints the optimal plan from (0, 400), checks that each continuation of it (the printed names say tail)
is optimal from the state it reaches, and compares the greedy plan (the largest period reward at each step)
with the optimum.
"""

from __future__ import annotations

from itertools import product

HORIZON = 4
GRID = (0, 100, 200, 300, 400)
REWARD = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}


def period_reward(c: int) -> int:
    """Utility in utils of consuming c cents in one period."""
    return REWARD[c]


def bequest(w: int) -> int:
    """Reward in utils for the wealth w cents left at time H, counted in whole hundreds."""
    return w // 100


def feasible(w: int) -> tuple[int, ...]:
    """Consumption choices from wealth w cents: every grid amount c with c <= w."""
    return tuple(c for c in GRID if c <= w)


def backward_recursion() -> list[dict[int, int]]:
    """values[t][w] is V_t(w) in utils. V_H is the bequest; each earlier value is the maximum of the recursion."""
    values: list[dict[int, int]] = [{} for _ in range(HORIZON + 1)]
    values[HORIZON] = {w: bequest(w) for w in GRID}
    for t in range(HORIZON - 1, -1, -1):
        for w in GRID:
            values[t][w] = max(period_reward(c) + values[t + 1][w - c] for c in feasible(w))
    return values


def brute_force(t: int, w: int) -> tuple[int, int]:
    """Best total reward from (t, w) over every consumption sequence, and how many feasible sequences were checked."""
    best: int | None = None
    checked = 0
    for plan in product(GRID, repeat=HORIZON - t):
        wealth = w
        total = 0
        feasible_plan = True
        for c in plan:
            if c > wealth:
                feasible_plan = False
                break
            total += period_reward(c)
            wealth -= c
        if not feasible_plan:
            continue
        total += bequest(wealth)
        checked += 1
        if best is None or total > best:
            best = total
    if best is None:
        raise RuntimeError("no feasible plan")
    return best, checked


def optimal_plan(values: list[dict[int, int]], w0: int) -> tuple[list[int], list[int]]:
    """Follow the recursion's maximising consumption from (0, w0). Returns the plan and the wealth path."""
    plan: list[int] = []
    path = [w0]
    w = w0
    for t in range(HORIZON):
        c = max(feasible(w), key=lambda x: period_reward(x) + values[t + 1][w - x])
        plan.append(c)
        w -= c
        path.append(w)
    return plan, path


def greedy_plan(w0: int) -> tuple[list[int], list[int]]:
    """Take the largest period reward available at each step, ignoring the future. Returns the plan and wealth path."""
    plan: list[int] = []
    path = [w0]
    w = w0
    for _ in range(HORIZON):
        c = max(feasible(w), key=period_reward)
        plan.append(c)
        w -= c
        path.append(w)
    return plan, path


def plan_total(consumptions: list[int], w0: int) -> int:
    """Total reward in utils of a consumption sequence started at wealth w0, including the bequest."""
    total = 0
    w = w0
    for c in consumptions:
        total += period_reward(c)
        w -= c
    return total + bequest(w)


def main() -> None:
    """Print Parts A, B and C. Every value is an integer, so every line of the output is exact."""
    values = backward_recursion()
    print("Part A: value table V_t(W) in utils, from the backward recursion")
    for t in range(HORIZON + 1):
        cells = " ".join(f"W{w}={values[t][w]}" for w in GRID)
        print(f"t {t} {cells}")

    print("Part B: brute force over every consumption sequence")
    all_match = True
    for t in range(HORIZON):
        for w in GRID:
            best, _ = brute_force(t, w)
            all_match = all_match and best == values[t][w]
    _, checked = brute_force(0, 400)
    print(f"plans_checked_from_0_400 {checked}")
    print(f"recursion_matches_brute_force {all_match}")

    print("Part C: optimal plan from (0, 400), its continuations, and the greedy plan")
    plan, path = optimal_plan(values, 400)
    print("optimal_consumption " + " ".join(str(c) for c in plan))
    print("optimal_wealth_path " + " ".join(str(w) for w in path))
    print(f"optimal_total {plan_total(plan, 400)}")
    tails_optimal = all(plan_total(plan[k:], path[k]) == values[0][path[k]] for k in range(HORIZON))
    print(f"optimal_plan_every_tail_optimal {tails_optimal}")

    greedy, greedy_path = greedy_plan(400)
    print("greedy_consumption " + " ".join(str(c) for c in greedy))
    print(f"greedy_total {plan_total(greedy, 400)}")
    for k in range(1, HORIZON):
        tail_optimal = plan_total(greedy[k:], greedy_path[k]) == values[k][greedy_path[k]]
        print(f"greedy_tail_from_t {k} wealth {greedy_path[k]} optimal {tail_optimal}")
    print(f"greedy_plan_optimal {plan_total(greedy, 400) == values[0][400]}")


main()
