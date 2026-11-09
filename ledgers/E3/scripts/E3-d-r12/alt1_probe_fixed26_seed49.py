import math, sys
import elicit as sol
import test_project as tp
import json
from instance import make_instance
r49 = [dict(x) for x in json.loads(str(make_instance(49)["responses_json"]))]
for name, resp in (("fixed26", [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS]), ("seed49", r49)):
    parsed = [sol._parse(x) for x in resp]
    xi = sol._maximise(parsed)
    f = lambda t: sol._objective(t, parsed)
    g, hess = sol._gradient_and_hessian(f, xi)
    neg = [[-h for h in row] for row in hess]
    print(name, "xi", [f"{x:.4f}" for x in xi], "gamma", f"{1/(1+math.exp(-xi[0])):.4g}", "lambda", f"{math.exp(xi[1]):.4g}", "kappa", f"{math.exp(xi[2]):.4g}")
    print("   score", [f"{x:.2e}" for x in g], "-H diag", [f"{neg[i][i]:.3e}" for i in range(3)], "PD", sol._cholesky(neg) is not None)
