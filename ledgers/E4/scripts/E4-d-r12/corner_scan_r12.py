"""Relative error of the bisection against the closed form at the domain corner (round 12), for two caps."""
import math
import sys
sys.path.insert(0, "ledgers/E4/scripts/E4-d-r12")
import importlib.util
spec = importlib.util.spec_from_file_location("rd", "ledgers/E4/scripts/E4-d-r12/rederive_r12.py")
# reuse functions without re-running prints: exec only the defs
src = open("ledgers/E4/scripts/E4-d-r12/rederive_r12.py").read().split('print("== tau_bar on the box")')[0]
ns = {}
exec(compile(src, "rd_defs", "exec"), ns)
bisect, closed, tau_bar = ns["bisect"], ns["closed"], ns["tau_bar"]

c_test = 0.1707691121
sd = 1e-50
print("corner test case: tau_bar =", f"{tau_bar(c_test):.10f}", "closed root =", f"{closed(sd, c_test):.6e}")
for cap in (200, 240):
    lam = bisect(sd, c_test, cap=cap)
    rel = abs(lam - closed(sd, c_test)) / closed(sd, c_test)
    print(f"cap {cap}: lambda={lam:.10e} relative error={rel:.3e} pass(<=1e-10)={rel <= 1e-10}")

# corner grid: sd in [1e-50, 1.06e-50], cost with tau_bar >= 1e-2
c_max = -math.log(0.505) / 4
print("cost where tau_bar = 1e-2 exactly:", f"{c_max:.10f}")
N_SD, N_C = 300, 300
cases = []
for i in range(N_SD):
    s = 1e-50 * (1.06) ** (i / (N_SD - 1))
    for j in range(N_C):
        c = c_max * j / (N_C - 1)
        cases.append((s, c))
for cap in (200, 240):
    over = 0
    worst = 0.0
    for s, c in cases:
        cf = closed(s, c)
        if cf <= 0 or cf >= 1:
            continue
        lam = bisect(s, c, cap=cap)
        rel = abs(lam - cf) / cf
        if rel > 1e-10:
            over += 1
        worst = max(worst, rel)
    print(f"cap {cap}: {len(cases)} cases, interior-closed cases over 1e-10: {over}, worst relative error {worst:.3e}")
