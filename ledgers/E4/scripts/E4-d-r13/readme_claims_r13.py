"""Re-derives the numeric claims in ledgers/E4/equivalent/README.md (round 13): the 200- and 240-halving corner cases."""
import math
import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE13-E4-d/course/modules/E/E4/grader")
import reference as ref


def solve_cap(sd: float, cost: float, cap: int) -> float:
    g0, g1 = ref.gap_at_zero(sd, cost), ref.indifference_gap(1.0, sd, cost)
    assert g0 > 0.0 and g1 < 0.0
    low, high, steps = 0.0, 1.0, 0
    while high - low > ref.BISECTION_TOLERANCE * high and steps < cap:
        mid = 0.5 * (low + high)
        if ref.indifference_gap(mid, sd, cost) > 0.0:
            low = mid
        else:
            high = mid
        steps += 1
    return 0.5 * (low + high)


def closed(sd: float, cost: float) -> float:
    t = 2.0 * math.exp(-4.0 * cost) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


sd, cost = 1e-50, 0.17076911209
print("tau_bar at README cost:", 2.0 * math.exp(-4.0 * cost) - 1.0)
for cap in (200, 240):
    lam = solve_cap(sd, cost, cap)
    print(f"cap {cap}: rel err at (1e-50, 0.17076911209) = {abs(lam - closed(sd, cost)) / closed(sd, cost):.3e}")
print("2^-200 =", 2.0 ** -200, " 1e-10*root (root=closed) =", 1e-10 * closed(sd, cost))
root = closed(sd, cost)
n = 0
w = 1.0
while w > 1e-12 * root:
    w /= 2.0
    n += 1
print("halvings for width <= 1e-12 * root near 2e-51:", n)
# corner scan: noise 1e-50 to 1.06e-50 and costs with tau_bar >= 1e-2; count cap-200 cases above 1e-10
import random
rng = random.Random(7)
bad200 = bad240 = 0
worst200 = worst240 = 0.0
N = 3000
for _ in range(N):
    s = 1e-50 * rng.uniform(1.0, 1.06)
    c = rng.uniform(0.0, 0.1725)
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    if t < 1e-2:
        continue
    ex = closed(s, c)
    if ex <= 0 or ex >= 1:
        continue
    e200 = abs(solve_cap(s, c, 200) - ex) / ex
    e240 = abs(solve_cap(s, c, 240) - ex) / ex
    worst200, worst240 = max(worst200, e200), max(worst240, e240)
    bad200 += e200 > 1e-10
    bad240 += e240 > 1e-10
print(f"random corner scan N={N}: cap200 cases>1e-10: {bad200}, worst {worst200:.3e}; cap240 cases>1e-10: {bad240}, worst {worst240:.3e}")
