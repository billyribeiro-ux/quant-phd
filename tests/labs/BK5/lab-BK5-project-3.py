"""Rung 3 check: the reference instance, its asset location table, and safe withdrawal rate.

Standard library only. All inputs are SIMULATED illustrative values.
Self-contained implementation verifying end-to-end execution of the retirement planning engine.
"""

import random


def human_capital_value(earnings_cents: list[int], discount_rate_bps: int) -> int:
    """Calculate present value of earnings in integer cents."""
    r = discount_rate_bps / 10_000.0
    return round(sum(e / ((1.0 + r) ** t) for t, e in enumerate(earnings_cents, start=1)))


def optimal_asset_location(
    equity_target_cents: int,
    bond_target_cents: int,
    taxable_capacity_cents: int,
    tda_capacity_cents: int,
    roth_capacity_cents: int,
) -> dict[str, dict[str, int]]:
    """Allocate equity and bond targets across accounts to maximize tax efficiency."""
    tda_bond = min(bond_target_cents, tda_capacity_cents)
    rem_bond = bond_target_cents - tda_bond
    taxable_bond = min(rem_bond, taxable_capacity_cents)
    roth_bond = rem_bond - taxable_bond

    tda_equity = tda_capacity_cents - tda_bond
    taxable_equity = taxable_capacity_cents - taxable_bond
    roth_equity = roth_capacity_cents - roth_bond

    return {
        "taxable": {"equity": taxable_equity, "bond": taxable_bond},
        "tda": {"equity": tda_equity, "bond": tda_bond},
        "roth": {"equity": roth_equity, "bond": roth_bond},
    }


def moving_block_bootstrap(
    returns: list[float],
    block_length: int,
    horizon: int,
    n_paths: int,
    seed: int,
) -> list[list[float]]:
    """Generate synthetic return paths via moving-block bootstrap."""
    num_blocks = len(returns) - block_length + 1
    rng = random.Random(seed)
    paths: list[list[float]] = []
    for _ in range(n_paths):
        path: list[float] = []
        while len(path) < horizon:
            start_idx = rng.randint(0, num_blocks - 1)
            path.extend(returns[start_idx : start_idx + block_length])
        paths.append(path[:horizon])
    return paths


def simulate_withdrawals(
    initial_wealth_cents: int,
    initial_withdrawal_bps: int,
    return_paths: list[list[float]],
) -> tuple[float, int]:
    """Simulate decumulation and return (ruin_probability, median_terminal_wealth_cents)."""
    withdrawal_cents = (initial_wealth_cents * initial_withdrawal_bps) // 10_000
    n_paths = len(return_paths)
    ruin_count = 0
    terminal_wealths: list[int] = []

    for path in return_paths:
        w = float(initial_wealth_cents)
        ruined = False
        for r in path:
            w -= withdrawal_cents
            if w <= 0.0:
                ruined = True
                w = 0.0
                break
            w *= 1.0 + r
            if w <= 0.0:
                ruined = True
                w = 0.0
                break
        if ruined:
            ruin_count += 1
            terminal_wealths.append(0)
        else:
            terminal_wealths.append(round(w))

    ruin_prob = round(ruin_count / n_paths, 4)
    sorted_tw = sorted(terminal_wealths)
    med_tw = (
        sorted_tw[n_paths // 2] if n_paths % 2 == 1 else (sorted_tw[n_paths // 2 - 1] + sorted_tw[n_paths // 2]) // 2
    )
    return ruin_prob, med_tw


def safe_withdrawal_rate(
    initial_wealth_cents: int,
    return_paths: list[list[float]],
    max_ruin_prob: float = 0.05,
    step_bps: int = 10,
) -> int:
    """Find maximum withdrawal rate in bps whose ruin probability <= max_ruin_prob."""
    best_rate = 0
    current_rate = 100
    while current_rate <= 1000:
        ruin_prob, _ = simulate_withdrawals(initial_wealth_cents, current_rate, return_paths)
        if ruin_prob <= max_ruin_prob:
            best_rate = current_rate
        else:
            break
        current_rate += step_bps
    return best_rate


def main() -> None:
    # Deterministic reference scenario parameters
    earnings_cents = [10_000_000 + i * 150_000 for i in range(25)]
    discount_rate_bps = 350
    hc = human_capital_value(earnings_cents, discount_rate_bps)
    print(f"Human capital: ${hc / 100:,.2f} ({hc} cents)")

    total_wealth_cents = 100_000_000
    eq_target = 60_000_000
    bond_target = 40_000_000
    tax_cap = 40_000_000
    tda_cap = 40_000_000
    roth_cap = 20_000_000

    loc = optimal_asset_location(eq_target, bond_target, tax_cap, tda_cap, roth_cap)
    print("Asset location:")
    for acct in ("taxable", "tda", "roth"):
        eq = loc[acct]["equity"]
        bd = loc[acct]["bond"]
        print(f"  {acct.upper():7s} | Equity: ${eq / 100:10,.0f} | Bond: ${bd / 100:10,.0f}")

    rng_hist = random.Random(101)
    hist_returns: list[float] = []
    prev_r = 0.05
    for _ in range(50):
        shock = rng_hist.gauss(0.0, 0.11)
        ret = 0.05 + 0.15 * (prev_r - 0.05) + shock
        hist_returns.append(round(ret, 4))
        prev_r = ret

    paths = moving_block_bootstrap(hist_returns, block_length=5, horizon=30, n_paths=200, seed=42)
    swr_bps = safe_withdrawal_rate(total_wealth_cents, paths, max_ruin_prob=0.05, step_bps=10)
    ruin_prob, med_tw = simulate_withdrawals(total_wealth_cents, swr_bps, paths)

    print(f"Safe withdrawal rate (max ruin 5%): {swr_bps / 100:.2f}% ({swr_bps} bps)")
    print(f"Ruin probability at SWR: {ruin_prob * 100:.2f}%")
    print(f"Median terminal wealth at SWR: ${med_tw / 100:,.0f}")


main()
