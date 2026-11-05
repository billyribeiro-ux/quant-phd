"""Round 9, slice e: independent recomputation of prose numbers in the changed M2 hunks and the sin ratio claim."""

import importlib.util
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path

CHECK = Path("/Users/billyribeiro/.fanout/wt/verifyD9-M2-e")
GRADER = CHECK / "course/modules/M/M2/grader"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# L22 Part A: unrounded maximizer errors against a - 1 (lab golden-section search)
src = (CHECK / "tests/labs/M2/lab-M2-L22-1.py").read_text(encoding="utf-8").replace("\nmain()", "")
ns: dict = {}
exec(compile(src, "l22", "exec"), ns)
for a in ns["PARAMETERS_A"]:
    x = ns["maximizer_a"](a)
    print(f"L22 A a={a} xhat={x!r} |xhat-(a-1)|={abs(x - (a - 1)):.4e}")
print("L22 f_xx(1.5 maximizer) =", -1.5 / (1 + 0.5) ** 2, " 0.5*0.667*1e-16 =", 0.5 * (2 / 3) * 1e-16)

# L24 exact forward and central errors of exp at 1 (Decimal, exact up to 50 digits)
getcontext().prec = 50


def e_dec() -> Decimal:
    s, t = Decimal(0), Decimal(1)
    for n in range(1, 90):
        s += t
        t = t / n
    return s


E = e_dec()


def expm1(h: Decimal) -> Decimal:
    s, t, n = Decimal(0), h, 1
    while abs(t) > Decimal(10) ** -60:
        s += t
        n += 1
        t = t * h / n
    return s


for h in (Decimal("1e-8"), Decimal("1e-9"), Decimal("1e-4"), Decimal("1e-5"), Decimal("1e-6")):
    fwd = E * (expm1(h) / h - 1)
    sinh = (expm1(h) - expm1(-h)) / 2
    cen = E * (sinh / h - 1)
    print(f"L24 exact h={h}: forward error {fwd:.6e}, central error {cen:.6e}")
for h in (1e-8, 1e-9):
    print(f"L24 float forward signed error at h={h}: {(math.exp(1 + h) - math.exp(1)) / h - math.e:.6e}")
c5 = (math.exp(1 + 1e-5) - math.exp(1 - 1e-5)) / 2e-5 - math.e
c7 = (math.exp(1 + 1e-7) - math.exp(1 - 1e-7)) / 2e-7 - math.e
print(f"L24 E3 unrounded central errors: 1e-5 {abs(c5):.10e}, 1e-7 {abs(c7):.10e}, difference {abs(c5) - abs(c7):.3e}")

# project.html Exemplar B: sin central ratio over the 100 instances (seeds 0-49, two each)
inst = load(GRADER / "instance.py", "instance_r9")
vals = []
for seed in range(50):
    for s in (seed, seed + 7919):
        x0 = inst.make_instance(s)["x0"]
        e1 = abs((math.sin(x0 + 1e-2) - math.sin(x0 - 1e-2)) / 2e-2 - math.cos(x0))
        e2 = abs((math.sin(x0 + 5e-3) - math.sin(x0 - 5e-3)) / 1e-2 - math.cos(x0))
        vals.append(e1 / e2)
print(f"sin ratio range over 100 instances: {min(vals)!r} .. {max(vals)!r}; 7 dp {round(min(vals), 7)} .. {round(max(vals), 7)}")

# project.html Exemplar B: relative size of the central error at 1e-6 against the analytic derivative
print("Exemplar B relative error 7.111207e-04 / 23407826.805475 =", 7.111207e-04 / 23407826.805475)
print("Lab 3 ulp at 2721581 (2^21..2^22):", 2.0 ** (21 - 52), "; ulp near 1e8:", 2.0 ** (26 - 52))
