"""Verifier script (M2 slice c, round 1): recompute the displayed numbers of L13-L18 from unrounded values."""

import math

print("--- L13")
e = math.e
for k in (5, 7, 8, 9):
    h = 10.0 ** (-k)
    fwd = abs((math.exp(1 + h) - math.exp(1)) / h - e)
    cen = abs((math.exp(1 + h) - math.exp(1 - h)) / (2 * h) - e)
    print(f"k={k} fwd={fwd!r} cen={cen!r}")
c5 = abs((math.exp(1 + 1e-5) - math.exp(1 - 1e-5)) / (2e-5) - e)
c7 = abs((math.exp(1 + 1e-7) - math.exp(1 - 1e-7)) / (2e-7) - e)
print("central 1e-5 minus 1e-7 (full precision):", c5 - c7)
print("ratio fwd 1e-2 / 1e-3 (printed-form):", (abs((math.exp(1.01) - math.e) / 0.01 - e)) / (abs((math.exp(1.001) - math.e) / 0.001 - e)))
print("forward 1e-9 / 1e-8 ratio:", 2.154e-7 / 6.603e-9)
print("central 4.530e-5 vs forward 1.364e-2 ratio:", 1.364e-2 / 4.530e-5)
print("2 delta/h at 1e-9, truncation (h/2)e at 1e-9:", 2 * 2**-52 / 1e-9, 0.5e-9 * e)
print("ratio rounding/truncation at 1e-9:", (2 * 2**-52 / 1e-9) / (0.5e-9 * e))
print("R1 h* = 2 sqrt(1e-3/e) =", 2 * math.sqrt(1e-3 / e))
print("R3 2^-53/1e-8 =", 2**-53 / 1e-8, " e* that =", e * 2**-53 / 1e-8, " B(h*)=2sqrt(e*2^-52)=", 2 * math.sqrt(e * 2**-52))
print("L13 M3 h* central (3 d/e)^(1/3) =", (3 * 2**-52 / e) ** (1 / 3))
print("Exact: 2/(3 sqrt3)", 2 / (3 * math.sqrt(3)))
print("Ex2.3 bounds: e*0.005=", e * 0.005, " e^1.01*0.005=", math.exp(1.01) * 0.005)
print("Ex2.3 central: e^0.99*1e-4/6=", math.exp(0.99) * 1e-4 / 6, " e^1.01*1e-4/6=", math.exp(1.01) * 1e-4 / 6)
print("E1 ratio bounds: 10e^-0.001 =", 10 * math.exp(-0.001), " 10e^0.01=", 10 * math.exp(0.01))
print("central ratio bounds: 100e^-0.011 =", 100 * math.exp(-0.011), " 100e^0.011=", 100 * math.exp(0.011))
print("M3 sin(0.01)=", math.sin(0.01), " D=", math.sin(0.01) / 0.01, " err=", math.sin(0.01) / 0.01 - 1)
print("M3 bound 0.005*sin(0.01)=", 0.005 * math.sin(0.01))

print("--- L14")
f1 = lambda x: x * math.exp(x) + math.sin(x) / x
e2 = math.exp(2)
print("f1(2) exact =", repr(f1(2.0)), " f1'(2) exact =", repr(math.exp(2) + 2 * math.exp(2) + (2 * math.cos(2) - math.sin(2)) / 4))
print("Example 4.1 sum of rounded pieces 14.778112198+0.454648714 =", 14.778112198 + 0.454648714)
print("2e^2 =", 2 * e2, " e^2 =", e2, " sin2/2 =", math.sin(2) / 2)
print("E1: exp(sin1)=", math.exp(math.sin(1)), " product*2 =", math.exp(math.sin(1)) * math.cos(1) * 2)
print("E1 sin1 =", math.sin(1), " cos1 =", math.cos(1))
print("R2 Example 5.1: 2+cos1 =", 2 + math.cos(1), " f=", 2 + math.sin(1), " sin1=", math.sin(1))

print("--- L15")
pts = [(math.cos(2 * math.pi * k / 360), math.sin(2 * math.pi * k / 360)) for k in range(360)]
best = max(range(360), key=lambda k: abs(pts[k][0] ** 2 * pts[k][1]))
print("argmax f/r angle index:", best, " value:", abs(pts[best][0] ** 2 * pts[best][1]))
print("value at 35 deg:", abs(math.cos(math.radians(35)) ** 2 * math.sin(math.radians(35))), " at 36:", abs(math.cos(math.radians(36)) ** 2 * math.sin(math.radians(36))))
print("arcsin(1/sqrt3) in degrees:", math.degrees(math.asin(1 / math.sqrt(3))))
print("2/(3sqrt3):", 2 / (3 * math.sqrt(3)))

print("--- L16")
F = lambda x, y: x * x * y + math.exp(x * y)
print("F_x(1,2)=", 4 + 2 * math.exp(2), " F_y(1,2)=", 1 + math.exp(2), " F_xy+F_yx at (1,2)=", 2 + 3 * math.exp(2))
print("F(2,1)=", F(2, 1), " half spacing at [8,16)=", 2**-50 / 2, " /h=", 2**-50 / 2 / 1e-5)
print("e^2.00001=", math.exp(2.00001), " (1e-10/6)*7.39=", 1e-10 / 6 * 7.39)

print("--- L17")
gx, gy = 2 * 1 * 0.5, 1 + math.cos(0.5)
print("gradient", gx, gy, " 1+cos0.5 =", 1 + math.cos(0.5))
print("length", math.hypot(gx, gy), " angle deg", math.degrees(math.atan(gy / gx)))
print("E3 delta deg", 62 - math.degrees(math.atan2(gy, gx)))
print("R1 Euclid dir", gx / math.hypot(gx, gy), gy / math.hypot(gx, gy), " rescaled", gx / gy, " value", gx / gy + gy)
print("sup-norm corner value", 1 + gy)

print("--- L18")
print("remainder check ok")
