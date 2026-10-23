import numpy as np

# Lesson 1's bond-and-stock market, now with state probabilities. Every state-price vector psi gives an SDF
# m = psi / pi (Proposition 2.1); x* is the one in the payoff space, and the one with the smallest E[m^2].
probs = np.array([0.25, 0.5, 0.25])
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])
p = np.array([0.96, 0.976])
direction = np.array([-0.5, 0.8, -0.3])  # spans ker X'
end_a, end_b = np.array([0.5, 0.0, 0.46]), np.array([0.0, 0.8, 0.16])  # nonnegative ends of the state-price line

print("tau    state prices psi           SDF m = psi / pi          E[m^2]   m in span(X)?")
for tau in np.linspace(0.0, 1.0, 5):
    psi = (1 - tau) * end_a + tau * end_b
    m = psi / probs
    resid = m - X @ np.linalg.lstsq(X, m, rcond=None)[0]
    print(f"{tau:4.2f}  {np.round(psi, 4)}  {np.round(m, 4)}  {probs @ m**2:.6f}  {bool(np.allclose(resid, 0))}")

b = np.linalg.solve(X.T @ (probs[:, None] * X), p)
x_star = X @ b
print("x* =", np.round(x_star, 6), "| E[x*^2] =", round(float(probs @ x_star**2), 6))
print(
    "x* is strictly positive here:",
    bool(np.all(x_star > 0)),
    "| its state prices pi * x* =",
    np.round(probs * x_star, 6),
)
t_star = float((probs * x_star)[1] / end_b[1])  # position of x*'s state prices on the segment from end_a to end_b
print(f"x*'s state prices lie on the segment at tau = {t_star:.6f}")
