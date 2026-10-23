import numpy as np

# Worked example: x* for Lesson 4's bond-and-stock market, then for a sample drawn from it.
probs = np.array([0.25, 0.5, 0.25])  # state probabilities: E[f] = probs @ f
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])  # rows are states, columns are the bond and the stock
p = np.array([0.96, 0.976])  # prices of one unit of each asset

# Step 1. Second-moment matrix E[x x'] = X' diag(probs) X. It must be invertible: no redundant payoff.
second = X.T @ (probs[:, None] * X)
print("E[x x'] =", np.round(second, 6).tolist(), "| determinant:", round(float(np.linalg.det(second)), 6))

# Step 2. Weights b solve E[x x'] b = p; x* = x'b is the unique SDF in the payoff space (L04, Theorem 3.2).
b = np.linalg.solve(second, p)  # solve, never invert explicitly: same answer, better conditioned
x_star = X @ b
print("b =", np.round(b, 6), "| x* by state =", np.round(x_star, 6))

# Step 3. Verify that it prices both assets. This is the check the autograder runs, to rounding.
print("E[x* x] - p =", np.round(X.T @ (probs * x_star) - p, 12) + 0.0)

# Step 4. A sample of 8 months drawn from the states: the sample x* uses equal weights 1/T (L07, Definition 1.1).
rng = np.random.default_rng(1)
train = X[rng.choice(3, size=8, p=probs)]
test = X[rng.choice(3, size=8, p=probs)]
b_hat = np.linalg.solve(train.T @ train / len(train), p)
in_err = train.T @ (train @ b_hat) / len(train) - p  # zero by construction (L07, Proposition 2.1)
out_err = test.T @ (test @ b_hat) / len(test) - p  # the only informative number
print("sample b =", np.round(b_hat, 6), "| in-sample errors =", np.round(in_err, 12) + 0.0)
print("out-of-sample errors =", np.round(out_err, 6), "| rms =", round(float(np.sqrt(np.mean(out_err**2))), 6))
