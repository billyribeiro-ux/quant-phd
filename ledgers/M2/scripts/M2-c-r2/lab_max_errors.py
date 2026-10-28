"""Verifier script (M2 slice c, round 2): maximum errors measured by the L14, L16 and L18 lab twins.

Loads each twin without its printing side effects is not needed: the twin's main() is run under redirect.
Run as: <checkout>/.venv/bin/python -I ledgers/M2/scripts/M2-c-r2/lab_max_errors.py <checkout>
"""

import contextlib
import importlib.util
import io
import pathlib
import sys

root = pathlib.Path(sys.argv[1])


def load(n: int):
    spec = importlib.util.spec_from_file_location(f"l{n}", root / f"tests/labs/M2/lab-M2-L{n}-1.py")
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


m14 = load(14)
print("L14 max err f1:", m14.max_error(m14.f1, m14.f1_exact), " f2:", m14.max_error(m14.f2, m14.f2_exact))
m16 = load(16)
wx = max(abs(m16.partial_x(m16.big_f, x, y, m16.H) - m16.fx_closed(x, y)) for x, y in m16.grid())
wy = max(abs(m16.partial_y(m16.big_f, x, y, m16.H) - m16.fy_closed(x, y)) for x, y in m16.grid())
print("L16 max err Fx:", wx, " Fy:", wy)
m18 = load(18)
worst = 0.0
for x in [-1.0, -0.5, 0.0, 0.5, 1.0]:
    for y in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        fd = m18.jacobian_fd(x, y, m18.H)
        cf = m18.jacobian_closed(x, y)
        worst = max(worst, max(abs(fd[i][j] - cf[i][j]) for i in range(2) for j in range(2)))
print("L18 max entry err:", worst)
