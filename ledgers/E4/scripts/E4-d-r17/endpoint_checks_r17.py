"""Round 17: endpoint and closed-form checks for the E4 page's stated numbers (independent of the page code).
Prints Lab 1 and Lab 2 gap limits at fraction 0 (proxy 1e-9) and at 1, the Lab 1 closed form, the target
precision, the box bounds of the Inputs paragraph, and the 22 by 22 box count of Lab 3. Usage: endpoint_checks_r17.py <checkout>"""
import importlib.util as u
import math
import sys

root = sys.argv[1]
spec = u.spec_from_file_location("ref", f"{root}/course/modules/E/E4/grader/reference.py")
R = u.module_from_spec(spec)
spec.loader.exec_module(R)
for label, sd, c in (("lab1", 0.60, 0.13), ("lab2", 0.70, 0.14)):
    g0 = R.gap_at_zero(sd, c)
    g_small = R.indifference_gap(1e-9, sd, c)
    print(label, "gap limit at 0 (closed form)", f"{g0:+.6f}", "gap at 1e-9", f"{g_small:+.6f}", "gap at 1", f"{R.indifference_gap(1.0, sd, c):+.6f}")
tau_e, tau_v, a = 1.0, 1.0, 2.0
c = 0.13
print("lab1 informativeness closed form 1 - e^{2ac} tau_v/(tau_v+tau_e) =", f"{1 - math.exp(2 * a * c) * tau_v / (tau_v + tau_e):.8f}")
print("tau_bar(0.150) =", f"{2 * math.exp(-4 * 0.150) - 1:.8f}", " tau_bar(0.120) =", f"{2 * math.exp(-4 * 0.120) - 1:.8f}")
print("tau_y(1) lower bound at sigma 0.75 =", f"{1 / (1 + 4 * 0.75 ** 2):.6f}")
inside = 0
for i in range(22):
    for j in range(22):
        sd = 0.500 + 0.250 * i / 21.0
        cost = 0.120 + 0.030 * j / 21.0
        if R.gap_at_zero(sd, cost) > 0.0 and R.indifference_gap(1.0, sd, cost) < 0.0:
            inside += 1
print("box interior count:", inside, "of", 22 * 22)
