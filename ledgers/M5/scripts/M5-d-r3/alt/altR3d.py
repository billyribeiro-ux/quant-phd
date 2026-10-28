# Alternative 4 (valid): certificate ||B V_n - V_n||_inf / (1 - beta) for the returned value V_n
# (standard contraction bound: ||V_n - V*|| <= ||B V_n - V_n|| / (1 - beta)); stop when it is at most tol.
import math
import reference_r3 as ref
def bellman_operator(params, grid, values):
    return ref.bellman_operator(params, grid, values)
def solve(params, grid, tol, max_iter):
    beta, alpha = ref._params(params); pts = ref._grid(grid); t = ref._tolerance(tol); b = ref._budget(max_iter)
    vals = [0.0]*len(pts); it = 0
    while True:
        vals = ref._sweep(beta, alpha, pts, vals); it += 1          # V_n after n sweeps
        nxt = ref._sweep(beta, alpha, pts, vals)                     # B V_n, used only for the residual
        cert = max(abs(x-y) for x, y in zip(nxt, vals, strict=True))/(1-beta)
        if cert <= t or it >= b:
            return {"value": vals, "iterations": it, "certified_error": cert, "converged": cert <= t}
