"""Round-15 check of the exception table's stated range: noise volume up to 1e150 and information cost up to 350
must return three finite keys from the reference (grader/reference.py). Also reports the values at the extremes.
Usage: python -I range_extremes_r15.py"""
import math
import sys

sys.path.insert(0, "course/modules/E/E4/grader")
import reference as R  # noqa: E402

cases = [(1e150, 0.13), (1e150, 350.0), (1e-50, 350.0), (1e-50, 0.0), (0.6, 350.0), (0.6, 0.0), (1e150, 0.0),
         (1e-300, 0.13), (5e149, 1.0), (1e-50, 1e-12)]
for sd, c in cases:
    out = R.solve_model(sd, c)
    finite = all(math.isfinite(v) for v in out.values())
    print(f"sd {sd!r} cost {c!r}: finite={finite} keys={sorted(out)} {({k: f'{v:.6g}' for k, v in out.items()})}")
print("math.exp(2*350) =", f"{math.exp(2*350):.3e}", " exp(4*350) overflows:", end=" ")
try:
    math.exp(4 * 350)
    print("no")
except OverflowError:
    print("yes")
print("max finite float", f"{sys.float_info.max:.3e}", "sd^2 at 1e150 =", f"{(1e150)**2:.3e}")
