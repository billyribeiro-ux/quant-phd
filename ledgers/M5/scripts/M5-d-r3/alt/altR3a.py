# Alternative 1: relative feasibility cutoff (1e-12) and last-index tie-break; certificate beta/(1-beta)*change.
import math
import reference_r3 as ref
def bellman_operator(params, grid, values):
    beta, alpha = ref._params(params); pts = ref._grid(grid); vals = ref._values(values, len(pts))
    out=[]
    for k in pts:
        avail=k**alpha; best=-math.inf
        for kp, v in zip(pts, vals, strict=True):
            if kp <= avail*(1+1e-12):
                c=max(avail-kp,0.0)
                cand=math.sqrt(c)+beta*v
                if cand>=best: best=cand
        out.append(best)
    return out
def solve(params, grid, tol, max_iter):
    beta, alpha = ref._params(params); pts=ref._grid(grid); t=ref._tolerance(tol); b=ref._budget(max_iter)
    vals=[0.0]*len(pts); it=0; cert=math.inf
    while it<b:
        new=bellman_operator({"beta":beta,"alpha":alpha}, pts, vals); it+=1
        ch=max(abs(x-y) for x,y in zip(new,vals,strict=True)); vals=new
        cert=beta/(1-beta)*ch
        if cert<=t: break
    return {"value":vals,"iterations":it,"certified_error":cert,"converged":cert<=t}
