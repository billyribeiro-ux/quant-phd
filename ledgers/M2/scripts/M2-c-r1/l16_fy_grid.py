"""Verifier script (M2 slice c, round 1): locate the grid point of the largest F_y central-difference error (L16 lab),
compare it with the lab hypothesis' third-partial size (e^2 claim), and check the L17 R2 partial formula."""

import importlib.util
import math
import pathlib
import sys

root = pathlib.Path(sys.argv[1]) / "tests/labs/M2"
spec = importlib.util.spec_from_file_location("lab16", root / "lab-M2-L16-1.py")
mod = importlib.util.module_from_spec(spec)
import contextlib
import io

with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(mod)
rows = []
for x, y in mod.grid():
    ey = abs(mod.partial_y(mod.big_f, x, y, mod.H) - mod.fy_closed(x, y))
    rows.append((ey, x, y))
rows.sort(reverse=True)
print("largest F_y error on grid:", rows[0])
x, y = 2.0, 1.0
print("F_yyy = x^3 exp(xy) at (2,1):", x**3 * math.exp(x * y), " = 8e^2:", 8 * math.exp(2))
print("truncation h^2/6 * F_yyy at (2,1), h=1e-5:", 1e-10 / 6 * 8 * math.exp(2))
print("F_xxx = y^3 exp(xy) at (2,1):", 1.0 * math.exp(2), " e^2 =", math.exp(2))

# L17 R2 partial of f = x^2 y/(x^2+y^4): 2 x y^5/(x^2+y^4)^2 and its value on x = y^2
def fx(x, y):
    return 2 * x * y**5 / (x * x + y**4) ** 2

for y in (0.1, 0.01, 0.001):
    print("L17 R2 dfdx on x=y^2 at y=", y, ":", fx(y * y, y), " 1/(2y) =", 1 / (2 * y))
