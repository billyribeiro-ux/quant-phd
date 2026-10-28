"""Verifier script (M2 slice c, round 1): measure the actual maximum errors that L14, L17 and L16 hypotheses predict."""

import importlib.util
import math
import pathlib
import sys

root = pathlib.Path(sys.argv[1]) / "tests/labs/M2"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    import contextlib
    import io

    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


l14 = load("lab-M2-L14-1")
e1 = l14.max_error(l14.f1, l14.f1_exact)
e2 = l14.max_error(l14.f2, l14.f2_exact)
print(f"L14 max grid error f1 = {e1:.3e}, f2 = {e2:.3e}")

l17 = load("lab-M2-L17-1")
gx, gy = l17.gradient(1.0, 0.5)
worst = 0.0
for angle in range(360):
    u = l17.unit(angle)
    worst = max(worst, abs(l17.directional_central((1.0, 0.5), u, 1e-6) - (gx * u[0] + gy * u[1])))
print(f"L17 max directional error = {worst:.3e}")

l16 = load("lab-M2-L16-1")
w = 0.0
for x, y in l16.grid():
    w = max(w, abs(l16.partial_x(l16.big_f, x, y, 1e-5) - l16.fx_closed(x, y)))
print(f"L16 max F_x error = {w:.3e}")
w = 0.0
for x, y in l16.grid():
    w = max(w, abs(l16.partial_y(l16.big_f, x, y, 1e-5) - l16.fy_closed(x, y)))
print(f"L16 max F_y error = {w:.3e}")
print("L16 F_x(1,2) central minus closed:", l16.partial_x(l16.big_f, 1.0, 2.0, 1e-5) - l16.fx_closed(1.0, 2.0))
