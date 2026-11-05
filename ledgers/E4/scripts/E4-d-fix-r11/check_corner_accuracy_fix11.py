"""Round-11 fixer check: relative accuracy of grader/reference.py at the domain edge (noise volume 1e-50 to 1.06e-50, tau-bar at least 1e-2). Run from the repository root with -I."""
import math, sys
sys.path.insert(0, "course/modules/E/E4/grader")
import reference as R
def closed(sd, c):
    t = 2.0*math.exp(-4.0*c) - 1.0
    return 2.0*sd*math.sqrt(t/(1.0-t))
c_edge = -math.log(1.01/2.0)/4.0
worst = (0, None); n = 0; over = 0
for i in range(300):
    sd = 1e-50 * (1 + 0.002*i)
    for j in range(300):
        c = c_edge - 0.0005 + 0.0005*j/299
        t = 2*math.exp(-4*c)-1
        if t < 1e-2: continue
        ex = closed(sd, c)
        if ex >= 1.0 or ex <= 0: continue
        n += 1
        out = R.solve_model(sd, c)["informed_fraction"]
        rel = abs(out-ex)/ex
        if rel > 1e-10: over += 1
        if rel > worst[0]: worst = (rel, (sd, c, t, ex, out))
print("cases", n, "over 1e-10:", over, "max rel", f"{worst[0]:.4e}", "ratio", f"{worst[0]/1e-10:.3f}", worst[1])
