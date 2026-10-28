"""Round-2 check of Appendix A3 on the page: weights for two assets, closed form, det and scaling (random grid)."""
import itertools
import numpy as np
worst = 0.0
for a, b, rho in itertools.product([0.05, 0.1, 0.3, 1.0, 2.5], [0.05, 0.2, 0.7, 1.0, 3.0], [-0.99, -0.5, 0.0, 0.3, 0.9, 0.999]):
    C = np.array([[1, rho], [rho, 1.0]])
    D = np.diag([a, b])
    S = D @ C @ D
    w = np.linalg.solve(S, np.ones(2)); w /= w.sum()
    closed = np.array([b * (b - rho * a), a * (a - rho * b)]) / (a * a + b * b - 2 * rho * a * b)
    worst = max(worst, float(np.max(np.abs(w - closed))))
    assert a * a + b * b - 2 * rho * a * b > 0
    c = 3.7
    S2 = (c * D) @ C @ (c * D)
    w2 = np.linalg.solve(S2, np.ones(2)); w2 /= w2.sum()
    worst = max(worst, float(np.max(np.abs(w2 - w))))
print("max deviation of closed form and scaling invariance over grid:", worst)
