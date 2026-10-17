import itertools
import math

import numpy as np
from numpy.typing import NDArray


def sharpe(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Per-column Sharpe ratio of per-period returns."""
    return np.asarray(x.mean(axis=0) / x.std(axis=0, ddof=1))


def pbo(m: NDArray[np.float64], n_blocks: int) -> float:
    """CSCV estimate of the probability of backtest overfitting (Sharpe ratio as the metric)."""
    m = m[m.shape[0] % n_blocks :]
    blocks = np.split(m, n_blocks)
    n = m.shape[1]
    logits = []
    for combo in itertools.combinations(range(n_blocks), n_blocks // 2):
        train = np.vstack([blocks[i] for i in combo])
        test = np.vstack([blocks[i] for i in range(n_blocks) if i not in combo])
        best = int(np.argmax(sharpe(train)))
        oos = sharpe(test)
        rank = 1 + np.sum(oos < oos[best]) + 0.5 * (np.sum(oos == oos[best]) - 1)
        omega = rank / (n + 1)
        logits.append(math.log(omega / (1 - omega)))
    return float(np.mean(np.array(logits) <= 0))


# SIMULATED: one configuration with a true daily Sharpe ratio of 0.10 (about 1.6 annualized)
# competes against a growing number of skill-free configurations; 1000 days, 8 blocks.
rng = np.random.default_rng(88)
print("trials  mean_PBO")
for n_trials in (2, 20, 200):
    values = []
    for _ in range(16):
        m = rng.standard_normal((1000, n_trials)) * 0.01
        m[:, 0] += 0.001
        values.append(pbo(m, 8))
    print(f"{n_trials} {np.mean(values):.4f}")
