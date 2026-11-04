"""Independent recount of the L09 lab numbers (verifier, round 1). Uses numpy only, not the twin's code."""

from __future__ import annotations

import itertools

import numpy as np

P1 = [[1, 2], [3], [4, 5, 6]]
P2 = [[1, 2, 3], [4, 5], [6]]
X = np.array(list(itertools.product([-2, -1, 0, 1, 2], repeat=6)), dtype=float)  # rows: bets, cols: states 1..6
n_bets = X.shape[0]


def cell_mean(part: list[list[int]], vals: np.ndarray) -> np.ndarray:
    """Posterior expected receipt at every state: mean of vals over the state's cell (uniform prior)."""
    out = np.empty_like(vals)
    for cell in part:
        idx = [c - 1 for c in cell]
        out[:, idx] = vals[:, idx].mean(axis=1, keepdims=True)
    return out


G1 = cell_mean(P1, X)
G2 = cell_mean(P2, -X)


def meet(state: int) -> list[int]:
    reached = {state}
    frontier = [state]
    while frontier:
        cur = frontier.pop()
        for part in (P1, P2):
            for cell in part:
                if cur in cell:
                    for w in cell:
                        if w not in reached:
                            reached.add(w)
                            frontier.append(w)
    return sorted(reached)


print("bets:", n_bets)
for state in (1, 4):
    m = [w - 1 for w in meet(state)]
    strict = (G1[:, state - 1] > 0) & (G2[:, state - 1] > 0)
    nonneg = np.all(G1[:, m] >= 0, axis=1) & np.all(G2[:, m] >= 0, axis=1)
    both = strict & np.all(G1[:, m] >= 0, axis=1) & np.all(G2[:, m] >= 0, axis=1)
    zero = nonneg & np.all(G1[:, m] == 0, axis=1) & np.all(G2[:, m] == 0, axis=1)
    print(f"state {state} meet {[w + 1 for w in m]}: strict-both {strict.sum()}, strict and nonneg-on-meet {both.sum()}, "
          f"nonneg-on-meet {nonneg.sum()}, nonneg but not zero on meet {(nonneg & ~zero).sum()}")
first = np.argmax((G1[:, 0] > 0) & (G2[:, 0] > 0))
print("first strict bet at state 1:", X[first].astype(int).tolist(), "g1 on meet", G1[first, :3].tolist(), "g2 on meet", G2[first, :3].tolist())
first4 = np.argmax((G1[:, 3] > 0) & (G2[:, 3] > 0))
print("first strict bet at state 4:", X[first4].astype(int).tolist(), "g1 on meet", G1[first4, 3:].tolist(), "g2 on meet", G2[first4, 3:].tolist())
# Emp 3 description: zero posteriors on {1,2,3} iff x3 = 0 and x2 = -x1
desc = (X[:, 2] == 0) & (X[:, 1] == -X[:, 0])
zero123 = np.all(G1[:, :3] == 0, axis=1) & np.all(G2[:, :3] == 0, axis=1)
print("Emp3 description count", desc.sum(), "zero-posterior count", zero123.sum(), "equal sets", bool(np.array_equal(desc, zero123)))
