import numpy as np
A = np.array([[2.0, 1.0, 0.0], [0.0, 3.0, 1.0], [0.0, 0.0, 5.0]])
values, vectors = np.linalg.eig(A)
for j in range(3):
    r = A @ vectors[:, j] - values[j] * vectors[:, j]
    print(f"lambda={values[j]!r} residual={r!r} max|r|={np.max(np.abs(r))!r}")
