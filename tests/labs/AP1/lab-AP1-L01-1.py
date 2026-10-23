import numpy as np

# An illustrative one-period market on three states. Columns of X are assets, rows are states.
X = np.array(
    [
        [1.0, 1.4, 2.4],  # state 1: bond, stock, fund
        [1.0, 1.1, 2.1],  # state 2
        [1.0, 0.6, 1.6],  # state 3
    ]
)
p = np.array([0.96, 0.976, 1.95])  # quoted prices: the fund's payoff is one bond plus one stock

# Is the fund redundant? Solve X[:, :2] c = X[:, 2] by least squares and check the fit.
c, *_ = np.linalg.lstsq(X[:, :2], X[:, 2], rcond=None)
print("fund = bond x", round(float(c[0]), 6), "+ stock x", round(float(c[1]), 6))
print("rank of X:", int(np.linalg.matrix_rank(X)))

# Kernel vector theta = (c, -1): its payoff is zero in every state (Proposition 2.2 needs p'theta = 0).
theta = np.append(c, -1.0)
print("payoff of theta:", np.round(X @ theta, 12) + 0.0, "| cost p'theta:", round(float(p @ theta), 6))

# A LOOP violation: scale theta so that it costs -1, i.e. you are paid 1 today and owe nothing tomorrow.
scaled = theta / -float(p @ theta)
print("scaled portfolio:", np.round(scaled, 4), "| cost:", round(float(p @ scaled), 6))

# Repricing the fund at the cost of its replicating portfolio restores LOOP.
p_fixed = p.copy()
p_fixed[2] = float(p[:2] @ c)
print("LOOP price of the fund:", round(float(p_fixed[2]), 6), "| p'theta:", round(float(p_fixed @ theta), 12) + 0.0)

# Every psi with X'psi = p is a linear pricing vector; rank 2 < 3 states leaves a line of them.
direction = np.cross(X[:, 0], X[:, 1])  # spans ker X' (orthogonal to both independent columns)
psi0, *_ = np.linalg.lstsq(X.T, p_fixed, rcond=None)  # the minimum-norm solution
print("direction of ker X':", np.round(direction, 6))
for t in (0.0, 0.25, 0.7):
    psi = psi0 + t * direction
    print(f"t = {t:+.2f}: psi = {np.round(psi, 4)}, prices all three: {bool(np.allclose(X.T @ psi, p_fixed))}")
