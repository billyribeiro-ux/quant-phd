# Alternative (round 4): the iteration written with a list comprehension and a sum-free change;
# the stop is the same check on the reported certified error, computed as (beta/(1-beta)) * change.
import math
import reference_r3 as ref


def bellman_operator(params, grid, values):
    beta, alpha = ref._params(params)
    pts = ref._grid(grid)
    vals = ref._values(values, len(pts))
    return [
        max((math.sqrt(k**alpha - kp) + beta * v) for kp, v in zip(pts, vals, strict=True) if kp <= k**alpha)
        for k in pts
    ]


def solve(params, grid, tol, max_iter):
    beta, alpha = ref._params(params)
    pts = ref._grid(grid)
    t = ref._tolerance(tol)
    b = ref._budget(max_iter)
    factor = beta / (1 - beta)
    vals = [0.0] * len(pts)
    n = 0
    cert = math.inf
    while n < b:
        new = bellman_operator({"beta": beta, "alpha": alpha}, pts, vals)
        n += 1
        diff = [abs(x - y) for x, y in zip(new, vals, strict=True)]
        vals = new
        cert = factor * max(diff)
        if cert <= t:
            break
    return {"value": vals, "iterations": n, "certified_error": cert, "converged": cert <= t}
