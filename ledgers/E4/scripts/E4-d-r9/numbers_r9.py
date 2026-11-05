"""Re-derive every displayed number in project.html that this round checks, from first principles (no page text).

Run: python3 -I numbers_r9.py <repo-root>
"""
import importlib.util
import math
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/E/E4/grader"))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", root / "course/modules/E/E4/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
A, TV, TE = 2.0, 1.0, 1.0


def tau_bar(c):
    return (TV + TE) * math.exp(-2 * A * c) - TV


def closed(sd, c):
    t = tau_bar(c)
    if t <= 0:
        return 0.0
    if t >= TE * TE / (TE + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TE * (TE - t)))


print(f"tau_bar(0.150) = {tau_bar(0.150):.8f}  tau_bar(0.120) = {tau_bar(0.120):.8f}  1/(1+4*0.75^2) = {1/(1+4*0.75**2):.7f}")
print(f"tau_bar = 2e^-4c-1 at 0.15: {2*math.exp(-0.6)-1:.8f}; at 0.12: {2*math.exp(-0.48)-1:.8f}")
for sd in (0.500, 0.625, 0.750):
    row = []
    for c in (0.120, 0.135, 0.150):
        row.append(f"sd {sd:.3f} c {c:.3f}: lam {closed(sd, c):.4f} info {tau_bar(c)/(TV+tau_bar(c)):.4f} "
                   f"1-e^4c/2 {1-math.exp(4*c)/2:.4f} bisect-closed {abs(ref.solve_model(sd, c)['informed_fraction']-closed(sd, c)):.1e}")
    print(" | ".join(row))
print(f"ratios at cost 0.120: 0.625/0.500 = {0.625/0.500:.2f} unrounded {closed(0.625,0.12)/closed(0.5,0.12):.10f}; "
      f"0.750/0.500 = {0.75/0.5:.2f} unrounded {closed(0.75,0.12)/closed(0.5,0.12):.10f}; "
      f"displayed 0.6978/0.5582 = {0.6978/0.5582:.5f}, 0.8373/0.5582 = {0.8373/0.5582:.5f}")
draws_sd = [make_instance(s)["noise_sd"] for s in range(50)]
draws_c = [make_instance(s)["info_cost"] for s in range(50)]
print(f"seeds 0-49 draws: noise_sd in [{min(draws_sd)}, {max(draws_sd)}], info_cost in [{min(draws_c)}, {max(draws_c)}]")
print(f"seeds 0-49 distinct instances: {len(set(zip(draws_sd, draws_c)))}")
sd, c = 1e-30, 0.13
exact = closed(sd, c)
got = ref.solve_model(sd, c)["informed_fraction"]
print(f"tiny root sd=1e-30 c=0.13: reference {got:.15e} closed {exact:.15e} relative diff {abs(got-exact)/exact:.2e}")
# Lab 1 and Lab 2 printed values: informativeness identity and gap at 0 for the two labs' inputs
lab1 = (0.60, 0.13)
print(f"lab1 closed-form pi: 1 - e^(2ac) tau_v/(tau_v+tau_e) = {1-math.exp(2*A*lab1[1])*TV/(TV+TE):.8f}; tau_bar = {tau_bar(lab1[1]):.8f}")
print(f"lab1 root via closed form = {closed(lab1[0], lab1[1]):.8f}")
text = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
print("open( in labs:", sum(len(re.findall(r"\bopen\(", (root / f'tests/labs/E4/lab-E4-project-{n}.py').read_text(encoding='utf-8'))) for n in (1, 2, 3)))
print("img/svg/canvas/iframe/figure/data-file in project.html:", len(re.findall(r"<(img|svg|canvas|iframe|figure)\b|data-file", text)))
