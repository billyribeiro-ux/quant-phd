"""Round-2 recomputation of the changed and slice numbers for M2 L13, L14, L15, L18 and their cards.

Run: python -I verify_numbers_r2.py   (standard library only)
"""

import math
from decimal import Decimal, getcontext

getcontext().prec = 50
out: list[str] = []


def show(label: str, value: object) -> None:
    out.append(f"{label}: {value}")


e = math.e
d = 2.0**-52
show("L13 e*h/2 at h=1e-2", f"{e * 1e-2 / 2:.7e}")
show("L13 e^1.01*0.005", f"{math.exp(1.01) * 0.005:.7e}")
show("L13 e^0.99*h^2/6", f"{math.exp(0.99) * 1e-4 / 6:.7e}")
show("L13 e^1.01*h^2/6", f"{math.exp(1.01) * 1e-4 / 6:.7e}")
show("L13 delta=2^-52", f"{d:.6e}")
show("L13 h*=2 sqrt(delta/e)", f"{2 * math.sqrt(d / e):.6e}")
show("L13 R1 h*=2 sqrt(1e-3/e)", f"{2 * math.sqrt(1e-3 / e):.8e}")
show("L13 E3 3delta/e", f"{3 * d / e:.6e}")
show("L13 E3 cube root (3delta/e)^(1/3)", f"{(3 * d / e) ** (1 / 3):.6e}")
show("L13 Cor4.1 B(h*)=2 sqrt(e delta)", f"{2 * math.sqrt(e * d):.6e}")
show("L13 R3 2^-53/1e-8", f"{2.0**-53 / 1e-8:.6e}")
show("L13 R3 e*2^-53/1e-8", f"{e * 2.0**-53 / 1e-8:.6e}")
show("L13 E2 (2delta/h)/((h/2)e) at 1e-9", f"{(2 * d / 1e-9) / (1e-9 / 2 * e):.4f}")
show("L13 forward ratio bounds 10e^-0.001, 10e^0.01", f"{10 * math.exp(-0.001):.4f} {10 * math.exp(0.01):.4f}")
show("L13 central ratio bounds 100e^-0.011, 100e^0.011", f"{100 * math.exp(-0.011):.4f} {100 * math.exp(0.011):.4f}")
show("L13 M3 sin(0.01)/0.01-1", f"{math.sin(0.01) / 0.01 - 1:.6e}")
show("L13 (0.01/2) sin 0.01", f"{0.005 * math.sin(0.01):.6e}")
ea = {}
for k in range(1, 13):
    h = 10.0 ** (-k)
    fwd = abs((math.exp(1.0 + h) - math.exp(1.0)) / h - e)
    cen = abs((math.exp(1.0 + h) - math.exp(1.0 - h)) / (2 * h) - e)
    ea[k] = (fwd, cen)
show("L13 central err at 1e-5 and 1e-7 (full precision float)", f"{ea[5][1]:.6e} {ea[7][1]:.6e}")
show("L13 |diff| central err 1e-5 vs 1e-7", f"{abs(ea[5][1] - ea[7][1]):.3e}")
show("L13 argmin central k (float formula)", min(ea, key=lambda k: ea[k][1]))
show("L13 argmin forward k (float formula)", min(ea, key=lambda k: ea[k][0]))

show("L14 f1(2) = 2e^2 + sin2/2", f"{2 * math.exp(2) + math.sin(2) / 2:.12f}")
show("L14 f1'(2) closed form", f"{math.exp(2) + 2 * math.exp(2) + (2 * math.cos(2) - math.sin(2)) / 4:.12f}")
show("L14 f1'(2) dual parts: 3e^2 - (2cos2 - sin2)/4 ... see formula", f"{3 * math.exp(2) - (2 * math.cos(2) - math.sin(2)) / 4 * 0 + (-(2 * math.cos(2) - math.sin(2)) / 4) * -1:.12f}")
show("L14 f2'(1)=2exp(sin1)cos1 (float)", f"{2 * math.exp(math.sin(1)) * math.cos(1):.12f}")
show("L14 rounded factors product 2.3197768247*0.5403023059*2 (Decimal)", f"{Decimal('2.3197768247') * Decimal('0.5403023059') * 2}")
show("L14 exp(sin1) float", f"{math.exp(math.sin(1)):.10f}")
show("L14 sin1, cos1", f"{math.sin(1):.10f} {math.cos(1):.10f}")
show("L14 Example 5.1 2+cos1", f"{2 + math.cos(1):.9f}")
show("L14 e^2, 2e^2, 3e^2", f"{math.exp(2):.9f} {2 * math.exp(2):.9f} {3 * math.exp(2):.9f}")


def g(x: float, y: float) -> float:
    return 0.0 if x == 0 and y == 0 else x * y / (x * x + y * y)


def f(x: float, y: float) -> float:
    return 0.0 if x == 0 and y == 0 else x * x * y / (x * x + y * y)


pts = [(math.cos(2 * math.pi * k / 360), math.sin(2 * math.pi * k / 360)) for k in range(360)]
vals_f = sorted(((abs(f(x, y)), k) for k, (x, y) in enumerate(pts)), reverse=True)[:6]
show("L15 top6 |f| on unit circle samples (value, degree)", [(f"{v:.8f}", k) for v, k in vals_f])
show("L15 exact 2/(3 sqrt3)", f"{2 / (3 * math.sqrt(3)):.8f}")
show("L15 asin(1/sqrt3) degrees", f"{math.degrees(math.asin(1 / math.sqrt(3))):.6f}")
show("L15 top3 |g| samples (value, degree)", [(f"{v:.8f}", k) for v, k in sorted(((abs(g(x, y)), k) for k, (x, y) in enumerate(pts)), reverse=True)[:3]])
for n in (10, 100, 1000, 10000):
    x = 1.0 / n
    show(f"L15 n={n}: g, f at (1/n,1/n)", f"{g(x, x):.6f} {f(x, x):.9f}")
show("L15 f(rx,ry)/(r f(x,y)) with r=1e-3 at (0.6,0.8)", f"{f(1e-3 * 0.6, 1e-3 * 0.8) / (1e-3 * f(0.6, 0.8)):.12f}")


def big_f(x: float, y: float) -> tuple[float, float]:
    return (x * x - y * y, 2 * x * y)


def jac_fd(x: float, y: float, h: float) -> list[list[float]]:
    ux, dx = big_f(x + h, y), big_f(x - h, y)
    uy, dy = big_f(x, y + h), big_f(x, y - h)
    c0 = [(ux[i] - dx[i]) / (2 * h) for i in range(2)]
    c1 = [(uy[i] - dy[i]) / (2 * h) for i in range(2)]
    return [[c0[0], c1[0]], [c0[1], c1[1]]]


worst = 0.0
grid = [-1.0, -0.5, 0.0, 0.5, 1.0]
for x in grid:
    for y in grid:
        J = jac_fd(x, y, 1e-5)
        C = [[2 * x, -2 * y], [2 * y, 2 * x]]
        for i in range(2):
            for j in range(2):
                worst = max(worst, abs(J[i][j] - C[i][j]))
show("L18 25-point worst entry error (central h=1e-5)", f"{worst:.3e}")
show("L18 J at (1,2) central diff", [[round(v, 6) for v in row] for row in jac_fd(1.0, 2.0, 1e-5)])
show("L18 half spacing of doubles in [4,8) = 2^-51/2 wait: spacing 2^-50, half 2^-51", f"{2.0**-51:.3e}")
show("L18 E1 rounding estimate half-spacing(4)/h", f"{2.0**-51 / 1e-5:.3e}")
show("L18 R1 partial at (rho,0), rho=1/(2 pi 5): 2 rho sin(1/rho)-cos(1/rho)", f"{2 * (1 / (2 * math.pi * 5)) * math.sin(2 * math.pi * 5) - math.cos(2 * math.pi * 5):.6f}")
print("\n".join(out))
