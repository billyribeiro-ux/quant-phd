# Alternative (round 4): feasibility with an absolute numerical cutoff of 1e-9 and a clamped consumption;
# certificate beta/(1-beta)*change computed as change*beta/(1-beta) (different rounding order).
import math
import reference_r3 as ref


def bellman_operator(params, grid, values):
    beta, alpha = ref._params(params)
    pts = ref._grid(grid)
    vals = ref._values(values, len(pts))
    out = []
    for k in pts:
        avail = k**alpha
        best = -math.inf
        for kp, v in zip(pts, vals, strict=True):
            if kp <= avail + 1e-9:
                cand = math.sqrt(max(avail - kp, 0.0)) + beta * v
                best = max(best, cand)
        out.append(best)
    return out


def solve(params, grid, tol, max_iter):
    beta, alpha = ref._params(params)
    pts = ref._grid(grid)
    t = ref._tolerance(tol)
    b = ref._budget(max_iter)
    vals = [0.0] * len(pts)
    it = 0
    cert = math.inf
    while it < b:
        new = bellman_operator({"beta": beta, "alpha": alpha}, pts, vals)
        it += 1
        change = max(abs(x - y) for x, y in zip(new, vals, strict=True))
        vals = new
        cert = change * beta / (1 - beta)
        if cert <= t:
            break
    return {"value": vals, "iterations": it, "certified_error": cert, "converged": cert <= t}
