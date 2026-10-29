import numpy as np
C = np.array([[1.0, 0.7, 0.3, -0.6],[0.7, 1.0, 0.5, 0.4],[0.3, 0.5, 1.0, 0.2],[-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
print('min eig', np.linalg.eigvalsh(C).min())
print('det C', np.linalg.det(C))
S = np.diag(v); Sig = S @ C @ S
w = np.linalg.solve(Sig, np.ones(4)); w = w / w.sum()
print('weights', np.round(w, 6), w.sum(), 'rounded sum', np.round(w, 6).sum())
lam, V = np.linalg.eigh(C)
X = V @ np.diag(np.maximum(lam, 0)) @ V.T
d = np.diag(X); Y = X / np.sqrt(np.outer(d, d))
print('clip dist', np.linalg.norm(Y - C), 'clip diag', np.diag(Y), 'clip min eig', np.linalg.eigvalsh(Y).min())
print('clip diag dev', np.abs(np.diag(Y) - 1).max())
