"""Verifier round 12: unrounded values behind the lesson prose (L05 E1/E3, L07 E1/E2) from the lab twins' own code."""
import importlib.util
import io
import math
import random
import re
import contextlib
from pathlib import Path

LAB = Path("tests/labs/M4")


def load_without_main(path):
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"\nmain\(\)\s*$", "\n", src)
    ns = {"__name__": "twin"}
    exec(compile(src, str(path), "exec"), ns)
    return ns


# L05: sample covariance and quadratic forms at n = 20000
ns = load_without_main(LAB / "lab-M4-L05-1.py")
draws, sample_cov = ns["draws"], ns["sample_cov"]
quadratic_form, S1, S2, RHO = ns["quadratic_form"], ns["S1"], ns["S2"], ns["RHO"]
s = sample_cov(draws(20000, ns["SEED"]))
sig11 = S1 * S1
print("L05 E1 relative error of s11 at n=20000:", (s[0][0] - sig11) / sig11)
print("L05 E1 from printed 0.00039491:", (0.00039491 - 0.0004) / 0.0004)
vals = []
for k in range(9):
    a = k * math.pi / 8
    vals.append(quadratic_form(s, (math.cos(a), math.sin(a))))
print("L05 E3 ratio largest/smallest (k=3 / k=7):", vals[3] / vals[7], "max k", vals.index(max(vals)), "min k", vals.index(min(vals)))

# L07: seeded Cauchy-free two-point mean of cos and phi(1); and the Part A error at t = 2
ns7 = load_without_main(LAB / "lab-M4-L07-1.py")
rng = random.Random(ns7["SEED"])
cos_sum = 0.0
sin_sum = 0.0
for _ in range(ns7["N_DRAWS"]):
    x = ns7["VALUE_A"] if rng.random() < ns7["P_A"] else ns7["VALUE_B"]
    cos_sum += math.cos(x)
    sin_sum += math.sin(x)
phi1 = ns7["phi_two_point"](1.0)
mc = cos_sum / ns7["N_DRAWS"]
print("L07 E1 sample mean cos:", mc, "real phi(1):", phi1.real, "difference:", mc - phi1.real)
num = ns7["mgf_numerical"](2.0, ns7["MU"], ns7["SIGMA"])
clo = ns7["mgf_closed"](2.0, ns7["MU"], ns7["SIGMA"])
print("L07 E2 absolute difference at t=2:", abs(num - clo), "closed", clo, "relative", abs(num - clo) / clo,
      "over eps", abs(num - clo) / 2.220446049250313e-16)
