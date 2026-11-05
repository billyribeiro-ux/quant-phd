"""Round 7 (SC1-d): recompute every number on project.html's labs, exemplars and interpretations for seed 0.

Uses grader/reference.py (the engine) and grader/instance.py, which the labs do not import, so the labs' printed numbers
are checked against an independent implementation. Also re-derives the Simpson quadrature and the exact walk counts.
Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-d-r7/recompute_numbers_r7.py
"""
import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/SC/SC1/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", GRADER / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

inst = make_instance(0)
H, a, N = inst["H"], inst["a"], inst["n_paths"]
tail = ref.reflection_tail(a, H)
print(f"instance: H={H} a={a} N={N} n_steps={inst['n_steps']}")
print(f"tail erfc(a/sqrt(2H)) = {tail:.6f}   (page: 0.086497)")
target = tail / 2.0
target_se = math.sqrt(target * (1 - target) / N)
band = 5 * target_se + 1 / N
print(f"target tail/2 = {target:.6f} (page 0.043248); target se = {target_se:.6f}; band = {band:.6f} (page 0.048142)")
est1, se1 = ref.discrete_max_exceedance(inst, 1)
print(f"one step: est {est1:.6f} se {se1:.6f} (page 0.059548 / 0.010735); est - target = {est1 - target:.6f} "
      f"(page 0.016300); in band: {abs(est1 - target) <= band}; (est-target)/se = {(est1 - target) / se1:.3f} (page 1.52)")
for n in (1, 4, 16, 64, 256):
    est, se = ref.discrete_max_exceedance(inst, n)
    print(f"grid {n:>3}: est {est:.6f} se {se:.6f} tail-est {tail - est:.6f} within 5se: "
          f"{abs(tail - est) <= 5 * se}")
fine, _ = ref.nested_grid_counts(inst, 256, 256)
parts = []
for c in (64, 16, 4, 1):
    _, coarse = ref.nested_grid_counts(inst, 256, c)
    parts.append((c, coarse, coarse <= fine))
print(f"nested fine(256)={fine} (page 40); coarse:", parts, "(page 35, 29, 27, 22; all <= fine)")
print(f"srw n=12 a=3: max {ref.srw_max_count(12, 3)} (page 1588), terminal {ref.srw_terminal_count(12, 3)} (page 794)")
print(f"srw n=6 a=2: max {ref.srw_max_count(6, 2)} (page 29), terminal>=2 {ref.srw_terminal_count(6, 2)} (page 22), "
      f"terminal>=3 {ref.srw_terminal_count(6, 3)} (page 7)")
# Simpson's quadrature of 2 P(B_H >= a), recomputed here independently of the labs.
top = a + 12 * math.sqrt(H)
steps = 4000
h = (top - a) / steps
dens = lambda x: math.exp(-x * x / (2 * H)) / math.sqrt(2 * math.pi * H)  # noqa: E731
s = dens(a) + dens(top) + sum((4 if k % 2 else 2) * dens(a + k * h) for k in range(1, steps))
quad = 2 * s * h / 3
print(f"Simpson 2P(B_H>=a) = {quad:.6f}; |quad - tail| = {abs(quad - tail):.2e} (page 9.13e-15 in Lab 1)")
# Exemplar A numbers (checks as stated in the exemplar passages).
print(f"exemplar A: 0.0595 ~ {est1:.4f}, se 0.0107 ~ {se1:.4f}, 0.0163 ~ {est1 - target:.4f}, half-tail 0.0432 ~ {target:.4f}, "
      f"1.52 ~ {(est1 - target) / se1:.4f}")
