"""Round-13 check of the corner numbers cited in ledgers/E4/equivalent/README.md (run with -I from the repository root).

Reproduces the round-11 grid (sd = 1e-50 (1 + 0.002 i), i < 300; cost on the tau-bar = 1e-2 edge) at the cited point, with
the cap of 200 and of 240 halvings, and reports the sd range the grid actually covers."""
import math, sys
sys.path.insert(0, "course/modules/E/E4/grader")
import reference as R


def solve_cap(sd, cost, cap):
    low, high, steps = 0.0, 1.0, 0
    while high - low > R.BISECTION_TOLERANCE * high and steps < cap:
        mid = 0.5 * (low + high)
        if R.indifference_gap(mid, sd, cost) > 0.0:
            low = mid
        else:
            high = mid
        steps += 1
    return 0.5 * (low + high)


def closed(sd, c):
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


c_edge = -math.log(1.01 / 2.0) / 4.0
cited_cost = 0.17076911209224613
print("cited point: tau_bar =", 2 * math.exp(-4 * cited_cost) - 1, "root =", closed(1e-50, cited_cost))
for cap in (200, 240):
    lam = solve_cap(1e-50, cited_cost, cap)
    ex = closed(1e-50, cited_cost)
    print(f"cap {cap} at full-precision cited cost: rel err = {abs(lam - ex) / ex:.4e}")
    lam = solve_cap(1e-50, 0.17076911209, cap)
    print(f"cap {cap} at the README's truncated cost 0.17076911209: rel err = {abs(lam - closed(1e-50, 0.17076911209)) / closed(1e-50, 0.17076911209):.4e}")
sds = [1e-50 * (1 + 0.002 * i) for i in range(300)]
print(f"round-11 grid sd range: {min(sds):.4e} .. {max(sds):.4e} (README states 1e-50 .. 1.06e-50)")
costs = [c_edge - 0.0005 + 0.0005 * j / 299 for j in range(300)]
print(f"round-11 grid cost range: {min(costs):.10f} .. {max(costs):.10f}; tau_bar range {2*math.exp(-4*max(costs))-1:.6f} .. {2*math.exp(-4*min(costs))-1:.6f}")
