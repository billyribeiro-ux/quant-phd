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


# SIMULATED pure noise: 100 configurations, 1000 days, 10 blocks. A log that loses its failures
# keeps only the 20 best full-sample results; compare it with the full log and with a random 20.
rng = np.random.default_rng(1001)
full_log, best_20, random_20 = [], [], []
for _ in range(50):
    m = rng.standard_normal((1000, 100)) * 0.01
    full_sharpe = m.mean(axis=0) / m.std(axis=0, ddof=1)
    full_log.append(pbo(m, 10))
    best_20.append(pbo(m[:, np.argsort(full_sharpe)[-20:]], 10))
    random_20.append(pbo(m[:, rng.choice(100, 20, replace=False)], 10))
for name, v in (("all 100 logged", full_log), ("20 best kept", best_20), ("random 20 kept", random_20)):
    print(f"{name}: mean PBO {np.mean(v):.3f}, standard error {np.std(v, ddof=1) / np.sqrt(len(v)):.3f}")
