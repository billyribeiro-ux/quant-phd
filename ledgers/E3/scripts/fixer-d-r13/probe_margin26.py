"""Fixed-26 participant: observed-information margin (eigenvalues and Cholesky pivots) at the reference estimate."""
import ast
import sys
from pathlib import Path

GRADER = Path("/Users/billyribeiro/dev/quant-phd/course/modules/E/E3/grader")
sys.path.insert(0, str(GRADER))
import reference as sol  # noqa: E402

rows = None
for node in ast.parse((GRADER / "test_project.py").read_text(encoding="utf-8")).body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "FIXED_26_ANSWERS":
        rows = ast.literal_eval(node.value)
responses = [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in rows]
parsed = [sol._parse(r) for r in responses]
xi = sol._maximise(parsed)
f = lambda t: sol._objective(t, parsed)  # noqa: E731
_, hess = sol._gradient_and_hessian(f, xi)
info = [[-h for h in row] for row in hess]
# eigenvalues of the symmetric 3x3 observed information via the characteristic polynomial (no numpy needed)
import numpy as np  # noqa: E402
print("xi (zeta, log lambda, log kappa):", xi)
print("observed information (reference, h=1e-5):")
print(np.array(info))
print("eigenvalues:", np.linalg.eigvalsh(np.array(info)))
print("cholesky pivots squared (s_ii):", [sol._cholesky(info) is not None])
L = sol._cholesky(info)
print("cholesky diagonal:", [L[i][i] for i in range(3)] if L else None)
for h in (1e-4, 1e-5, 1e-6, 1e-7):
    # observed information by central differences of the oracle at step h (test's own formula)
    th = list(xi)
    def at(*moves):
        y = list(th)
        for idx, amount in moves:
            y[idx] += amount
        return sol._objective(y, parsed)
    f0 = at()
    m = np.zeros((3, 3))
    for i in range(3):
        m[i, i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            m[i, j] = m[j, i] = v
    print("h", h, "eigs", np.linalg.eigvalsh(m), "diag", np.diag(m))
