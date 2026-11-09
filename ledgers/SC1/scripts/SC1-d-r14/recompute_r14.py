"""Independent recomputation of every number on project.html for seed 0, from the grader's reference (not the labs).

Prints each number with the locator it backs. Run: .venv/bin/python -I recompute_r14.py <checkout root>
"""
import math
import sys
from fractions import Fraction

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

inst = make_instance(0)
H, a, N, n = inst["H"], inst["a"], inst["n_paths"], inst["n_steps"]
print("instance seed 0:", H, a, N, n)
tail = ref.reflection_tail(a, H)
print(f"tail erfc = {tail:.6f} ({tail!r})")
# Simpson on the normal density, independent of the twin's code
def simpson(level, horizon, m=4000):
    top = level + 12 * math.sqrt(horizon)
    h = (top - level) / m
    f = lambda x: math.exp(-x * x / (2 * horizon)) / math.sqrt(2 * math.pi * horizon)
    s = f(level) + f(top) + sum((4 if k % 2 else 2) * f(level + k * h) for k in range(1, m))
    return 2 * s * h / 3
q = simpson(a, H)
print(f"quadrature = {q:.6f}; |quad - tail| = {abs(q - tail):.2e}")
# one-step estimate and its SE (divisor N-1)
est, se = ref.discrete_max_exceedance(inst, 1)
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print(f"one step est {est:.6f} se {se:.6f} target {target:.6f} target_se {tse:.6f} band {band:.6f} diff {abs(est-target):.6f}")
print(f"diff/se_sample = {abs(est-target)/se:.4f}  diff/tse = {abs(est-target)/tse:.4f}  tail/2 - est = {target-est:.6f}")
print(f"(tail - est) - target = {(tail-est)-target:.6f}")
for g in (1, 4, 16, 64, 256):
    e, s = ref.discrete_max_exceedance(inst, g)
    print(f"grid {g:>3}: est {e:.6f} se {s:.6f} tail-est {tail-e:.6f} hits {round(e*N)}")
for coarse in (64, 16, 4, 1):
    fc, cc = ref.nested_grid_counts(inst, 256, coarse)
    print(f"nested fine 256 = {fc}, coarse {coarse} = {cc}, coarse<=fine {cc<=fc}")
mx, ends = ref.srw_max_count(12, 3), ref.srw_terminal_count(12, 3)
print(f"walk 12 level 3: max {mx}, ends>=3 {ends}, ends>=4 {ref.srw_terminal_count(12,4)}, 2^12={2**12}")
print("1588 = 794 + 794:", mx == 794 + 794, " 1588 = 2*794:", 2 * 794 == mx)
print("interp: (0.086497-0.059548)?", round(tail-est,6))
print("0.001799/0.012870 =", round(0.001799/0.012870,4), "  0.016300/0.010735 =", round(0.016300/0.010735,4), "  0.016300/0.009218 =", round(0.016300/0.009218,4))
print("0.088296-0.086497 =", round(0.088296-0.086497,6))
print("half tail:", round(tail/2,6), " 0.043248 ->", round(tail/2, 6) == 0.043248)
print("band check: 0.048142 - 0.016300 =", round(0.048142 - 0.016300, 6))
# Rounding of the 1-step tail-minus-estimate printed by Lab 3 vs the unrounded
print("printed 0.026948 unrounded:", tail - est)
# sanity: a continuous-maximum identity check with exact fractions for the walk count (n=12, a=3)
import itertools
cnt = sum(1 for steps in itertools.product((1, -1), repeat=12) if max(itertools.accumulate(steps)) >= 3)
print("enumerated walks reaching 3 (n=12):", cnt)
