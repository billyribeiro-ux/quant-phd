"""Round-2 check: is Sigma = D Y D singular for the Lab 3 clipping repair? Prints eigenvalues, condition number,
and the clipping weights from three solvers (numpy.linalg.solve, numpy.linalg.lstsq, the reference Gauss elimination)."""
import sys
import numpy as np
sys.path.insert(0, "/tmp/verifyB2-M3-d/course/modules/M/M3/grader")
import reference as ref
C = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
vals, vecs = np.linalg.eigh(C)
print("eigenvalues of input:", vals)
clip = np.array(ref.clip_repair(C.tolist()))
print("eigenvalues of clip repair:", np.linalg.eigvalsh(clip))
S = np.diag(v) @ clip @ np.diag(v)
print("eigenvalues of Sigma (clip):", np.linalg.eigvalsh(S))
print("cond(Sigma clip):", np.linalg.cond(S))
w_solve = np.linalg.solve(S, np.ones(4)); w_solve /= w_solve.sum()
w_lstsq = np.linalg.lstsq(S, np.ones(4), rcond=None)[0]; w_lstsq /= w_lstsq.sum()
w_ref = ref.comparison_weights(clip.tolist(), v.tolist())
print("solve :", w_solve)
print("lstsq :", w_lstsq)
print("ref   :", w_ref)
# sensitivity: perturb the clip matrix at 1e-12
rng = np.random.default_rng(1)
for eps in [0, 1e-12, 1e-10]:
    P = clip + eps * rng.standard_normal((4, 4)); P = (P + P.T) / 2; np.fill_diagonal(P, 1.0)
    Sp = np.diag(v) @ P @ np.diag(v)
    try:
        w = np.linalg.solve(Sp, np.ones(4)); w /= w.sum()
        print("eps", eps, "weights", np.round(w, 6))
    except Exception as e:
        print("eps", eps, e)
# the projection repair
proj = np.array(ref.projection_repair(C.tolist()))
print("eigenvalues of projection:", np.linalg.eigvalsh(proj))
print("cond(Sigma proj):", np.linalg.cond(np.diag(v) @ proj @ np.diag(v)))

# Round-2 witness for the weights convention: a singular unit-diagonal PSD correlation matrix.
import sys as _s
_s.path.insert(0, "/tmp/verifyB2-M3-d/course/modules/M/M3/grader")
import reference as _ref
for _c in ([[1.0, 1.0], [1.0, 1.0]],):
    try:
        print("reference weights on", _c, "->", _ref.comparison_weights(_c, [0.1, 0.2]))
    except Exception as _e:  # the witness expects an exception type to be reported, not swallowed
        print("reference weights on", _c, "raises", type(_e).__name__, _e)
