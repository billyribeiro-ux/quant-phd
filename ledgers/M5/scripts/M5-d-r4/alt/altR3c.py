# Alternative 3: list-comprehension operator and an explicit running maximum for the change.
import math
import reference_r3 as ref
def bellman_operator(params, grid, values):
    beta, alpha = ref._params(params); pts = ref._grid(grid); vals = ref._values(values, len(pts))
    out = []
    for k in pts:
        r = k**alpha
        cands = [math.sqrt(r-kp) + beta*v for kp, v in zip(pts, vals, strict=True) if kp <= r]
        out.append(max(cands))
    return out
def solve(params, grid, tol, max_iter):
    beta, alpha = ref._params(params); pts = ref._grid(grid); t = ref._tolerance(tol); b = ref._budget(max_iter)
    vals = [0.0]*len(pts); it = 0
    while True:
        new = bellman_operator({"beta": beta, "alpha": alpha}, pts, vals); it += 1
        d = 0.0
        for x, y in zip(new, vals, strict=True):
            d = max(d, abs(x-y))
        vals = new
        cert = d*beta/(1-beta)
        if cert <= t or it >= b:
            return {"value": vals, "iterations": it, "certified_error": cert, "converged": cert <= t}
