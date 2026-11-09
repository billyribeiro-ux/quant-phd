"""Round-15 re-run of the README corner scan (equivalent/README.md, 'Stop-rule variants'), for one halving cap.

Grid as in ledgers/E4/scripts/E4-d-fix-r11/check_corner_accuracy_fix11.py: 300 noise volumes 1e-50 * (1 + 0.002 i) and
300 costs in [c_edge - 0.0005, c_edge], c_edge = -ln(1.01/2)/4 (tau-bar >= 0.01). Uses grader/reference.py.
Usage: python -I corner_scan_r15.py <cap>   (cap is MAX_BISECTION_STEPS: 240 is the page's value, 200 the old one)
"""
import math
import sys

sys.path.insert(0, "course/modules/E/E4/grader")
import reference as R  # noqa: E402

R.MAX_BISECTION_STEPS = int(sys.argv[1])


def closed(sd, c):
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


c_edge = -math.log(1.01 / 2.0) / 4.0
print("c_edge", repr(c_edge), "cost range", f"{c_edge - 0.0005:.10f}", f"{c_edge:.10f}")
print("tau-bar range", f"{2*math.exp(-4*(c_edge-0.0005))-1:.6f}", f"{2*math.exp(-4*c_edge)-1:.6f}")
worst = (0.0, None)
n = 0
over = 0
for i in range(300):
    sd = 1e-50 * (1 + 0.002 * i)
    for j in range(300):
        c = c_edge - 0.0005 + 0.0005 * j / 299
        t = 2 * math.exp(-4 * c) - 1
        if t < 1e-2:
            continue
        ex = closed(sd, c)
        if ex >= 1.0 or ex <= 0:
            continue
        n += 1
        out = R.solve_model(sd, c)["informed_fraction"]
        rel = abs(out - ex) / ex
        if rel > 1e-10:
            over += 1
        if rel > worst[0]:
            worst = (rel, (sd, c, t, ex, out))
print("cap", R.MAX_BISECTION_STEPS, "cases", n, "over 1e-10:", over, "max rel", f"{worst[0]:.4e}", "ratio", f"{worst[0]/1e-10:.4f}")
print("worst case sd, cost, tau-bar, root, out:", worst[1])
for sd, c in [(1e-50, 0.17076911209224613), (1e-50, 0.17076911209)]:
    t = 2 * math.exp(-4 * c) - 1
    ex = closed(sd, c)
    out = R.solve_model(sd, c)["informed_fraction"]
    print("point", sd, repr(c), "tau-bar", f"{t:.7f}", "root", f"{ex:.4e}", "rel err", f"{abs(out-ex)/ex:.4e}")
