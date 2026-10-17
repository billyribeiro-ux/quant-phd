import itertools
import math

import numpy as np
from numpy.typing import NDArray

# Toy backtest matrix (illustrative numbers, not market data): 8 periods, 3 configurations.
# Rows 1-2 form block A, rows 3-4 block B, rows 5-6 block C, rows 7-8 block D.
m = np.array(
    [
        [0.03, 0.01, -0.01],
        [0.01, 0.02, 0.02],
        [0.02, 0.00, 0.01],
        [0.04, 0.01, -0.02],
        [-0.03, 0.01, 0.00],
        [-0.01, 0.02, 0.03],
        [-0.02, 0.00, -0.01],
        [0.00, 0.01, 0.02],
    ]
)
n_blocks = 4
blocks = np.split(m, n_blocks)
n_strategies = m.shape[1]
names = "ABCD"


def sharpe(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Per-column Sharpe ratio of a block of per-period returns."""
    return np.asarray(x.mean(axis=0) / x.std(axis=0, ddof=1))


print("IS    OOS   winner  OOS_rank  omega  logit")
logits = []
for combo in itertools.combinations(range(n_blocks), n_blocks // 2):
    train = np.vstack([blocks[i] for i in combo])
    test = np.vstack([blocks[i] for i in range(n_blocks) if i not in combo])
    best = int(np.argmax(sharpe(train)))
    oos = sharpe(test)
    rank = 1 + np.sum(oos < oos[best]) + 0.5 * (np.sum(oos == oos[best]) - 1)
    omega = rank / (n_strategies + 1)
    logit = math.log(omega / (1 - omega))
    logits.append(logit)
    is_names = "".join(names[i] for i in combo)
    oos_names = "".join(names[i] for i in range(n_blocks) if i not in combo)
    print(f"{is_names}    {oos_names}    s{best + 1}      {rank:.1f}       {omega:.2f}   {logit:.4f}")

print(f"PBO = {np.mean(np.array(logits) <= 0):.4f}")
