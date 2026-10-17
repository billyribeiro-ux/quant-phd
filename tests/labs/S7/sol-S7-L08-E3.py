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


# SIMULATED: 20 skill-free configurations plus one with a daily Sharpe ratio of +0.2 on days 1-500
# and -0.2 on days 501-1000; 1000 days, 10 blocks, 200 histories.
rng = np.random.default_rng(2026)
estimates, picked_dying, oos_sharpe = [], [], []
for _ in range(200):
    m = rng.standard_normal((1000, 21)) * 0.01
    m[:500, 20] += 0.002
    m[500:, 20] -= 0.002
    estimates.append(pbo(m, 10))
    early, late = m[:500], m[500:]
    pick = int(np.argmax(early.mean(axis=0) / early.std(axis=0, ddof=1)))
    picked_dying.append(pick == 20)
    oos_sharpe.append(late[:, pick].mean() / late[:, pick].std(ddof=1))
v = np.array(estimates)
se = v.std(ddof=1) / np.sqrt(v.size)
print(f"mean PBO {v.mean():.3f}, standard error {se:.3f}, share >= 0.5: {np.mean(v >= 0.5):.2f}")
print(f"chronological split: picks the dying configuration {np.mean(picked_dying):.3f} of the time")
print(f"mean daily Sharpe ratio of the pick on days 501-1000: {np.mean(oos_sharpe):.3f}")
