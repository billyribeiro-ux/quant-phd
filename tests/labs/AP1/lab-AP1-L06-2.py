import numpy as np

# SIMULATED doubling strategy on a fair coin (Lesson 4, Section 5): stake 1, double after every loss, stop at
# the first win or at the horizon n. Exactly: P(win by n) = 1 - 2^-n; gain +1 on a win, -(2^n - 1) otherwise.
rng = np.random.default_rng(404)
n_paths = 400_000
print("horizon  P(win) sim  P(win) exact  mean gain sim  exact mean gain  E[worst loss] sim  exact")
for horizon in (4, 8, 12):
    flips = rng.random((n_paths, horizon)) < 0.5  # True = win
    first_win = np.where(flips.any(axis=1), flips.argmax(axis=1), horizon)  # losses before the first win
    won = first_win < horizon
    gain = np.where(won, 1.0, -(2.0**horizon - 1.0))
    worst = 2.0**first_win - 1.0  # deepest cumulative loss reached on the path
    exact_worst = sum(0.5 ** (k + 1) * (2.0**k - 1.0) for k in range(horizon)) + 0.5**horizon * (2.0**horizon - 1.0)
    print(
        f"{horizon:7d}  {won.mean():.6f}    {1 - 0.5**horizon:.6f}      {gain.mean():+.4f}        +0.0000"
        f"           {worst.mean():8.4f}          {exact_worst:.4f}"
    )
