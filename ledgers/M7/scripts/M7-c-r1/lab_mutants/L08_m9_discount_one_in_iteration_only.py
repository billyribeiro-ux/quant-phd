"""M7 L08 lab 1: the Bellman equation for a finite-horizon, discounted, finite-state problem, and value iteration.

SIMULATED: a fixed toy maintenance problem. It is not market data and it uses no random draws. A machine is in one of
three condition states, 0 (good), 1 (worn) or 2 (worn out). Each period it either runs or is repaired. Running earns
the profit PROFIT[s] in utils and moves the condition one step toward 2 (2 stays 2). Repair costs 4 utils, and the
condition is 0 in the next period. The discount factor is 9/10, the horizon is H = 6 periods, and the terminal reward
is 0. All arithmetic is exact in fractions.Fraction, so the printed decimals are display only.

Part A: the backward Bellman recursion from the terminal reward 0. It prints V_t(s) for t = 0 to 6, and the optimal
action at each (t, s) for t = 0 to 5. It also counts the (t, s) pairs with a tie between the two actions, t = 0 to 5.
Part B: brute force. For each t and s it takes the best discounted total over every action sequence of length H - t, and
compares it exactly with the recursion.
Part C: value iteration. Start from U^0 = 0 and apply the Bellman operator n times. It prints the largest change
max_s |U^(n+1)(s) - U^n(s)| for n = 0 to 5, and checks that U^n equals V_(H-n) from Part A. It does not show that the
iteration converges as n grows.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

HORIZON = 6
DISCOUNT = Fraction(9, 10)
STATES = (0, 1, 2)
ACTIONS = ("run", "repair")
PROFIT = {0: 6, 1: 4, 2: 1}
REPAIR_COST = 4


def reward(state: int, action: str) -> Fraction:
    """Period reward in utils: the profit when running, minus the repair cost when repairing."""
    if action == "run":
        return Fraction(PROFIT[state])
    return Fraction(-REPAIR_COST)


def next_state(state: int, action: str) -> int:
    """Condition in the next period: running moves one step toward 2, repair resets it to 0."""
    if action == "run":
        return min(state + 1, 2)
    return 0


def bellman_step(u: dict[int, Fraction]) -> tuple[dict[int, Fraction], dict[int, str], int]:
    """Apply the Bellman operator to u: at each state, the largest of reward + DISCOUNT * u(next state).

    Returns the new function, the first action that attains the maximum at each state, and the number of states
    where both actions attain it. Values are exact fractions in utils.
    """
    new: dict[int, Fraction] = {}
    best: dict[int, str] = {}
    ties = 0
    for s in STATES:
        candidates = {a: reward(s, a) + DISCOUNT * u[next_state(s, a)] for a in ACTIONS}
        top = max(candidates.values())
        winners = [a for a in ACTIONS if candidates[a] == top]
        if len(winners) > 1:
            ties += 1
        new[s] = top
        best[s] = winners[0]
    return new, best, ties


def backward_recursion(horizon: int, terminal: dict[int, Fraction]) -> list[dict[int, Fraction]]:
    """values[t][s] is V_t(s). V_horizon is the terminal reward; each earlier value applies the Bellman step."""
    values: list[dict[int, Fraction]] = [{} for _ in range(horizon + 1)]
    values[horizon] = dict(terminal)
    for t in range(horizon - 1, -1, -1):
        values[t], _, _ = bellman_step(values[t + 1])
    return values


def brute_force(t: int, s: int, horizon: int) -> tuple[Fraction, int]:
    """Best discounted total from (t, s) over every action sequence of length horizon - t, and the count enumerated."""
    best: Fraction | None = None
    checked = 0
    for plan in product(ACTIONS, repeat=horizon - t):
        checked += 1
        state = s
        total = Fraction(0)
        weight = Fraction(1)
        for action in plan:
            total += weight * reward(state, action)
            weight *= DISCOUNT
            state = next_state(state, action)
        total += weight * Fraction(0)
        if best is None or total > best:
            best = total
    if best is None:
        raise RuntimeError("no action sequence")
    return best, checked


def main() -> None:
    """Print Parts A, B and C. Each value is an exact fraction; the printed decimals are display only."""
    terminal = {s: Fraction(0) for s in STATES}
    values = backward_recursion(HORIZON, terminal)

    print("Part A: Bellman recursion, discount 9/10, horizon 6, terminal reward 0")
    for t in range(HORIZON + 1):
        cells = " ".join(f"V{s}={float(values[t][s]):.6f}" for s in STATES)
        print(f"t {t} {cells}")
    total_ties = 0
    for t in range(HORIZON):
        _, best, ties = bellman_step(values[t + 1])
        total_ties += ties
        actions = " ".join(f"s{s}={best[s]}" for s in STATES)
        print(f"policy t {t} {actions}")
    print(f"tied_pairs_t0_to_5 {total_ties}")

    print("Part B: brute force over every action sequence")
    all_match = True
    plans = 0
    for t in range(HORIZON):
        for s in STATES:
            brute_best, checked = brute_force(t, s, HORIZON)
            all_match = all_match and brute_best == values[t][s]
            plans += checked
    print(f"plans_enumerated {plans}")
    print(f"recursion_matches_brute_force {all_match}")

    print("Part C: value iteration from U^0 = 0")
    iterates = [dict(terminal)]
    for _ in range(6):
        new = {s: max(reward(s, a) + u for a in ACTIONS for u in [iterates[-1][next_state(s, a)]]) for s in STATES}
        iterates.append(new)
    for n in range(6):
        change = max(abs(iterates[n + 1][s] - iterates[n][s]) for s in STATES)
        print(f"n {n} change {float(change):.10f}")
    matches = all(iterates[n][s] == values[HORIZON - n][s] for n in range(7) for s in STATES)
    print(f"iterate_equals_n_period_recursion {matches}")


main()
