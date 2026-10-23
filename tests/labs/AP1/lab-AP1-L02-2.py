import numpy as np

# The separating-hyperplane proof of Theorem 3.1, run on the three-state market with the stock at 0.976.
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])
p = np.array([0.96, 0.976])
n_states = X.shape[0]

# L = {(-p'theta, X theta)}: a 2-dimensional subspace of R^4, spanned by the columns of G.
G = np.vstack([-p, X])
P = G @ np.linalg.solve(G.T @ G, G.T)  # orthogonal projection onto L
resid = np.eye(n_states + 1) - P  # projection onto the orthogonal complement of L

# Minimize ||(I - P) k|| over the simplex K = {k >= 0, sum k = 1} by projected gradient descent.
k = np.full(n_states + 1, 1.0 / (n_states + 1))
for _ in range(20000):
    k = k - 0.5 * resid @ k
    # Euclidean projection onto the simplex (sort-and-threshold).
    u = np.sort(k)[::-1]
    css = np.cumsum(u)
    rho = int(np.nonzero(u * np.arange(1, k.size + 1) > css - 1.0)[0][-1])
    k = np.maximum(k - (css[rho] - 1.0) / (rho + 1), 0.0)
w = resid @ k  # the separating vector of the proof
print("separating vector w:", np.round(w, 6))
print(
    "w is orthogonal to L:", bool(np.allclose(G.T @ w, 0.0, atol=1e-10)), "| w strictly positive:", bool(np.all(w > 0))
)
psi = w[1:] / w[0]
print("state prices psi = w[1:] / w[0]:", np.round(psi, 6))
print("X' psi:", np.round(X.T @ psi, 6), "| quoted prices:", p)
