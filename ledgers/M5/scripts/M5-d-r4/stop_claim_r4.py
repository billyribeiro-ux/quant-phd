import math
p = {"beta": 0.8535397019795181, "alpha": 0.3276562928132905}
grid = [0.23, 0.24, 0.98, 1.46]
tol = 1.0119307470200622e-11
beta, alpha = p["beta"], p["alpha"]
def sw(values):
    out = []
    for k in grid:
        r = k**alpha
        out.append(max(math.sqrt(r - kp) + beta * v for kp, v in zip(grid, values) if kp <= r))
    return out
factor = beta / (1 - beta)
vals = [0.0]*4
stop_sup = stop_last = None
for s in range(1, 401):
    new = sw(vals)
    ch_sup = max(abs(a-b) for a,b in zip(new, vals))
    ch_last = abs(new[-1]-vals[-1])
    if stop_last is None and factor*ch_last <= tol: stop_last = s
    if stop_sup is None and factor*ch_sup <= tol: stop_sup = s
    vals = new
    if stop_sup and stop_last: break
print("stop sup-norm sweep", stop_sup, "stop last-point-only sweep", stop_last)
