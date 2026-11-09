import json, math, sys
import elicit as sol
from instance import make_instance
for seed in map(int, sys.argv[1:]):
    r = json.loads(str(make_instance(seed)["responses_json"]))
    parsed = [sol._parse(x) for x in r]
    sol.LAST_XI.clear()
    try:
        sol.estimate(r)
        print(seed, "ok")
        continue
    except RuntimeError as e:
        print(seed, "RuntimeError:", str(e)[:60])
    xi, grad = sol.LAST_XI[-1]
    f = lambda t: sol._objective(t, parsed)
    g, hess = sol._gradient_and_hessian(f, xi)
    neg = [[-h for h in row] for row in hess]
    print("  xi", [f"{x:.6f}" for x in xi], "gamma", 1/(1+math.exp(-xi[0])), "lam", math.exp(xi[1]), "kappa", math.exp(xi[2]))
    print("  score", [f"{x:.3e}" for x in g])
    print("  -Hessian", [[f"{v:.4e}" for v in row] for row in neg])
    print("  -Hessian PD (Cholesky of -H at this point):", sol._cholesky(neg) is not None)
    print("  max|score| <", sol._STATIONARY, ":", max(abs(x) for x in g) < sol._STATIONARY)
