"""Round-5 verifier script (M2 slice c): re-derives the numbers printed or stated on L13-L18 that changed since 2657ab5.

Run as: <checkout>/.venv/bin/python ledgers/M2/scripts/M2-c-r5/rederive_r5.py
Prints each claim with its recomputed value so each can be compared with the page text.
"""
import math

e = math.e
delta = 2.0 ** -52
print("L13 Lab 1 hypothesis: h* forward = 2 sqrt(delta/e) =", 2 * math.sqrt(delta / e))
print("L13 Lab 1 hypothesis: central step (3 delta/e)^(1/3) =", (3 * delta / e) ** (1 / 3))
print("L13 Example 2.3 forward interval:", 0.005 * e, 0.005 * math.exp(1.01))
print("L13 Example 2.3 central interval:", (1e-4 / 6) * math.exp(0.99), (1e-4 / 6) * math.exp(1.01))
print("L13 E2 rounding 2delta/h at 1e-9 =", 2 * delta / 1e-9, " truncation (h/2)e at 1e-9 =", 0.5e-9 * e)
print("L13 E2 ratio rounding/truncation =", (2 * delta / 1e-9) / (0.5e-9 * e))
print("L13 E2 total bound =", 2 * delta / 1e-9 + 0.5e-9 * e)
print("L13 M3 sin(0.01) =", math.sin(0.01), " D =", math.sin(0.01) / 0.01, " bound 0.005 sin(0.01) =", 0.005 * math.sin(0.01))
print("L13 R1 2 sqrt(1e-3/e) =", 2 * math.sqrt(1e-3 / e))
print("L13 R3 2^-53/1e-8 =", 2 ** -53 / 1e-8, " e times =", e * 2 ** -53 / 1e-8, " 2sqrt(M delta) =", 2 * math.sqrt(e * delta))
print("L13 lab ratio 1.364e-2/1.360e-3 =", 1.364e-2 / 1.360e-3, " 2.154e-7/6.603e-9 =", 2.154e-7 / 6.603e-9)
print("L13 full-precision central errors at 1e-5, 1e-7 differ by", abs(
    abs((math.exp(1 + 1e-5) - math.exp(1 - 1e-5)) / 2e-5 - e) - abs((math.exp(1 + 1e-7) - math.exp(1 - 1e-7)) / 2e-7 - e)))
print("L14 2 exp(sin1) cos1 =", repr(2 * math.exp(math.sin(1)) * math.cos(1)))
print("L14 product of printed factors =", repr(2.3197768247 * 0.5403023059 * 2))
print("L14 Example 4.1 f(2), f'(2) closed form =", 2 * math.exp(2) + math.sin(2) / 2,
      math.exp(2) + 2 * math.exp(2) + (2 * math.cos(2) - math.sin(2)) / 4)
print("L15 2/(3 sqrt 3) =", 2 / (3 * math.sqrt(3)))
print("L16 F_x(1,2)=", 4 + 2 * math.exp(2), " F_y(1,2)=", 1 + math.exp(2), " F_xy(1,2)=", 2 + 3 * math.exp(2))
gy = 1 + math.cos(0.5)
L = math.hypot(1, gy)
print("L17 gradient (1, %.10f) length %.10f angle %.6f deg" % (gy, L, math.degrees(math.atan2(gy, 1))))
c = (1 / L, gy / L)
m = max(abs(c[0]), abs(c[1]))
r = (c[0] / m, c[1] / m)
print("L17 R1 rescaled Euclidean direction", r, "value", r[0] + gy * r[1], "corner value", 1 + gy)
print("L17 E3 delta (deg)", 62 - math.degrees(math.atan2(gy, 1)), " |g|(1-cos delta)", L * (1 - math.cos(math.radians(62 - math.degrees(math.atan2(gy, 1))))))
print("L17 E2 third derivative check: d3/dy3 sin y = -cos y needs (cos)' = -sin, which Assumption 1 does not state")
print("L18 Example 4.2 remainder length at s=(0.3,-0.2):",
      math.hypot(0.3 * 0.3 - 0.2 * 0.2, 2 * 0.3 * -0.2), " |h|^2 =", 0.3 ** 2 + 0.2 ** 2)
