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


# SIMULATED daily returns: 1000 days, 20 configurations, 10 blocks (252 splits each).
rng = np.random.default_rng(808)
null_pbo = np.array([pbo(rng.standard_normal((1000, 20)) * 0.01, 10) for _ in range(20)])
spread = null_pbo.std(ddof=1)
print(f"20 skill-free configurations, 20 samples: mean PBO {null_pbo.mean():.4f}")
print(f"  standard deviation {spread:.4f}, standard error of the mean {spread / np.sqrt(20):.4f}")
print(f"  smallest {null_pbo.min():.4f}, largest {null_pbo.max():.4f}")

genuine_pbo = []
for _ in range(20):
    m = rng.standard_normal((1000, 20)) * 0.01
    m[:, 0] += 0.0015  # configuration 1 has a true daily Sharpe ratio of 0.15
    genuine_pbo.append(pbo(m, 10))
print(f"one genuine configuration among 20, 20 samples: mean PBO {np.mean(genuine_pbo):.4f}")
