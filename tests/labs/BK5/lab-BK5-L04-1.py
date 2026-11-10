"""Lab L04-1: Moving-block bootstrap versus i.i.d. bootstrap on retirement ruin probabilities.

Demonstrates that i.i.d. resampling understates retirement ruin risk compared to a
moving-block bootstrap (block length = 5) on persistent return data over a 30-year horizon.
Standard library only. Seeded RNG. All inputs are SIMULATED.
"""

import random


def generate_persistent_returns(n_years: int, seed: int) -> list[float]:
    """Generate persistent real return series with AR(1) dynamics."""
    rng = random.Random(seed)
    mean_ret = 0.05
    rho = 0.25
    vol = 0.12
    returns = [mean_ret]
    for _ in range(n_years - 1):
        shock = rng.gauss(0.0, vol)
        r = mean_ret + rho * (returns[-1] - mean_ret) + shock
        returns.append(round(r, 4))
    return returns


def run_bootstrap_simulation(
    returns: list[float],
    block_length: int,
    horizon: int,
    n_sims: int,
    initial_wealth: float,
    withdrawal_rate: float,
    seed: int,
) -> float:
    """Run Monte Carlo simulation and return ruin probability."""
    rng = random.Random(seed)
    n = len(returns)
    num_blocks = n - block_length + 1
    withdrawal = initial_wealth * withdrawal_rate
    ruin_count = 0

    for _ in range(n_sims):
        w = initial_wealth
        path: list[float] = []
        while len(path) < horizon:
            if block_length == 1:
                path.append(rng.choice(returns))
            else:
                idx = rng.randint(0, num_blocks - 1)
                path.extend(returns[idx : idx + block_length])

        path = path[:horizon]
        ruined = False
        for r in path:
            w -= withdrawal
            if w <= 0.0:
                ruined = True
                break
            w *= 1.0 + r
            if w <= 0.0:
                ruined = True
                break
        if ruined:
            ruin_count += 1

    return ruin_count / n_sims


def main() -> None:
    seed = 42
    history_years = 60
    horizon = 30
    n_sims = 1_000
    initial_wealth = 1_000_000.0  # dollars

    returns = generate_persistent_returns(history_years, seed=101)
    rates = [0.030, 0.035, 0.040, 0.045, 0.050, 0.055]

    print("Retirement Ruin Probabilities (30-Year Horizon, 1,000 Paths):")
    for rate in rates:
        prob_iid = run_bootstrap_simulation(returns, 1, horizon, n_sims, initial_wealth, rate, seed=seed)
        prob_mbb = run_bootstrap_simulation(returns, 5, horizon, n_sims, initial_wealth, rate, seed=seed)
        print(
            f"Withdrawal Rate {rate * 100:4.1f}% | "
            f"i.i.d. Ruin: {prob_iid * 100:5.1f}% | "
            f"MBB (b=5) Ruin: {prob_mbb * 100:5.1f}% | "
            f"Gap: {(prob_mbb - prob_iid) * 100:+5.1f}%"
        )


main()
