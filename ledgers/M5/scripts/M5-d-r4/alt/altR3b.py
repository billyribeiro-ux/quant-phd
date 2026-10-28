# Alternative 2: certificate from the residual of the value: ||B V_n - V_n|| / (1 - beta) bounds ||V_n - V*||.
import math
import reference_r3 as ref
def bellman_operator(params, grid, values):
    return ref.bellman_operator(params, grid, values)
def solve(params, grid, tol, max_iter):
    beta, alpha = ref._params(params); pts=ref._grid(grid); t=ref._tolerance(tol); b=ref._budget(max_iter)
    vals=[0.0]*len(pts); it=0
    while True:
        new=ref._sweep(beta, alpha, pts, vals); it+=1
        resid=max(abs(x-y) for x,y in zip(new,vals,strict=True))
        vals=new
        cert=resid/(1-beta)
        if cert<=t or it>=b:
            return {"value":vals,"iterations":it,"certified_error":cert,"converged":cert<=t}
