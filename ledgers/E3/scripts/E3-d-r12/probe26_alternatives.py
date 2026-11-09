import math
import elicit as sol
import test_project as tp
responses = [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS]
parsed = [sol._parse(r) for r in responses]
xi = sol._maximise(parsed)
f = lambda t: sol._objective(t, parsed)
g, hess = sol._gradient_and_hessian(f, xi)
print("xi", [f"{x:.4f}" for x in xi], "gamma_hat", f"{1/(1+math.exp(-xi[0])):.3e}", "max|score| (1e-5 step)", f"{max(abs(x) for x in g):.2e}", "PD(-H)", sol._cholesky([[-h for h in row] for row in hess]) is not None)
