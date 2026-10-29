"""A4 hypothesis and singularity checks on the Lab 3 input (NumPy, independent of the module)."""
import numpy as np
c = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
w, V = np.linalg.eigh(c)
X = V @ np.diag(np.maximum(w, 0)) @ V.T
print("clipped X diagonal:", np.diag(X), "all positive:", bool((np.diag(X) > 0).all()))
print("singular values of X:", np.linalg.svd(X, compute_uv=False))
d = np.sqrt(np.diag(X))
Y = X / np.outer(d, d)
print("smallest |eig| of Y:", np.abs(np.linalg.eigvalsh(Y)).min())
S = np.diag(v) @ Y @ np.diag(v)
print("smallest |eig| of Sigma from clipped Y:", np.abs(np.linalg.eigvalsh(S)).min())
S_in = np.diag(v) @ c @ np.diag(v)
print("det Sigma input:", np.linalg.det(S_in), " (prod v)^2 det C:", np.prod(v)**2 * np.linalg.det(c))
