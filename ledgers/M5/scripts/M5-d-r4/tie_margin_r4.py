import math
beta = 0.8535397019795181
alpha = 0.3276562928132905
grid = [0.23, 0.24, 0.98, 1.46]
tol = 1.0119307470200622e-11
def sw(values):
    out = []
    for k in grid:
        r = k**alpha
        out.append(max(math.sqrt(r - kp) + beta * v for kp, v in zip(grid, values) if kp <= r))
    return out
vals = [0.0]*4
changes = []
for s in range(1, 175):
    new = sw(vals)
    changes.append(max(abs(a-b) for a,b in zip(new, vals)))
    vals = new
forms = {
 "beta/(1-beta)*c": lambda c: beta/(1-beta)*c,
 "beta*c/(1-beta)": lambda c: beta*c/(1-beta),
 "c/((1-beta)/beta)": lambda c: c/((1-beta)/beta),
 "c*beta/(1-beta)": lambda c: c*beta/(1-beta),
}
for name, f in forms.items():
    stop = next(s for s in range(1,175) if f(changes[s-1]) <= tol)
    print(f"{name:20s} first stop sweep {stop}")
for s in (169,170,171):
    c = changes[s-1]
    print(s, "cert ref %.17e" % (beta/(1-beta)*c), "tol %.17e" % tol, "rel diff %.3e" % ((beta/(1-beta)*c - tol)/tol))
