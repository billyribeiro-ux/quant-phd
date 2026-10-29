"""Fine-grid check that omega_{1/2}(p) = sqrt(p)/(1+2 sqrt(p(1-p))) is nondecreasing on [0,1] (L07 Definition 1.1 requirement)."""
import math
N = 2_000_000
prev = -1.0
bad = []
for i in range(N + 1):
    p = i / N
    w = math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p))) if 0 < p < 1 else float(p)
    if w < prev - 1e-15:
        bad.append((p, w, prev))
    prev = w
print("grid points", N + 1, "decreases (tol 1e-15):", len(bad), bad[:3])
# exact derivative sign: d/dp of w(p); numeric central difference at many points
mins = min((math.sqrt(p + 1e-7) / (1 + 2 * math.sqrt((p + 1e-7) * (1 - p - 1e-7))) - math.sqrt(p - 1e-7) / (1 + 2 * math.sqrt((p - 1e-7) * (1 - p + 1e-7)))) for p in [i / 10000 for i in range(1, 10000)])
print("min forward difference over p in (0,1):", mins)
