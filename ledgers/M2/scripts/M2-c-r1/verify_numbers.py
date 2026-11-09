"""Independent recomputation of the numbers printed in prose on M2 lessons L13 to L18 (verifier scratch, round 1).

Run: .venv/bin/python -I ledgers/M2/scripts/M2-c-r1/verify_numbers.py
"""
import math
import sys

try:
    import mpmath as mp
    mp.mp.dps = 40
    HAVE_MP = True
except ImportError:  # pragma: no cover
    HAVE_MP = False

out = []


def show(label, value):
    out.append(f"{label}: {value}")


e = math.e
delta = 2.0 ** -52
u53 = 2.0 ** -53

# ---- L13 ----
show("L13 e*h/2 at h=1e-2", f"{e*1e-2/2:.7e}")
show("L13 e*h^2/6 at h=1e-2", f"{e*1e-4/6:.7e}")
show("L13 e^1.01*0.005", f"{math.exp(1.01)*0.005:.7e}")
show("L13 e^0.99*h^2/6", f"{math.exp(0.99)*1e-4/6:.7e}")
show("L13 e^1.01*h^2/6", f"{math.exp(1.01)*1e-4/6:.7e}")
show("L13 unrounded forward/central ratio at 1e-2 (lab definitions)",
     "see verify block below")
fwd = {}
cen = {}
for k in range(1, 13):
    h = 10.0 ** (-k)
    fwd[k] = abs((math.exp(1 + h) - math.exp(1)) / h - e)
    cen[k] = abs((math.exp(1 + h) - math.exp(1 - h)) / (2 * h) - e)
show("L13 unrounded forward/central ratio at 1e-2", f"{fwd[2] / cen[2]:.4f}")
show("L13 printed-digit ratio 1.364e-2/4.530e-5", f"{1.364e-2 / 4.530e-5:.4f}")
show("L13 forward err 1e-9 / 1e-8 ratio (printed 6.603e-9, 2.154e-7)", f"{2.154e-7 / 6.603e-9:.4f}")
show("L13 full-precision central err at 1e-5 and 1e-7 (lab values)",
     f"{cen[5]:.6e} {cen[7]:.6e} diff={abs(cen[5]-cen[7]):.3e}")
show("L13 full-precision forward minimum k", min(fwd, key=fwd.get))
show("L13 full-precision central minimum k", min(cen, key=cen.get))
show("L13 E2 2delta/h at 1e-8, 1e-9", f"{2*delta/1e-8:.6e} {2*delta/1e-9:.6e}")
show("L13 E2 truncation e*h/2 at 1e-9 (e^xi ~ e)", f"{e*1e-9/2:.7e}")
show("L13 E2 ratio rounding/truncation at 1e-9 with unrounded values",
     f"{(2*delta/1e-9)/(e*1e-9/2):.2f} (e^xi uncertain; using e)")
show("L13 E2 unrounded 2delta/h=4.4409e-7 and 1.3591e-9 ratio", f"{(2*delta/1e-9)/1.3591e-9:.2f}")
show("L13 E3 3delta/e", f"{3*delta/e:.8e}")
show("L13 E3 cube root (3delta/e)^(1/3)", f"{(3*delta/e)**(1/3):.8e}")
show("L13 Lab1 forward step 2sqrt(delta/e)", f"{2*math.sqrt(delta/e):.8e}")
show("L13 Lab1 central step (3delta/e)^(1/3)", f"{(3*delta/e)**(1/3):.8e}")
show("L13 R1 2sqrt(1e-3/e)", f"{2*math.sqrt(1e-3/e):.8e}")
show("L13 R3 2^-53/1e-8", f"{u53/1e-8:.6e}")
show("L13 R3 e*2^-53/1e-8", f"{e*u53/1e-8:.6e}")
show("L13 Cor4.1 2sqrt(M delta), M=e", f"{2*math.sqrt(e*delta):.6e}")
show("L13 E1 (10 e^{-0.001}, 10 e^{0.01})", f"({10*math.exp(-0.001):.4f}, {10*math.exp(0.01):.4f})")
show("L13 central ratio bounds 100 e^{-0.011}, 100 e^{0.011}",
     f"({100*math.exp(-0.011):.2f}, {100*math.exp(0.011):.2f})")
show("L13 M3 sin(0.01)/0.01 - 1", f"{math.sin(0.01)/0.01-1:.6e}")
show("L13 M3 (0.01/2) sin(0.01)", f"{0.005*math.sin(0.01):.6e}")
show("L13 sin(0.01)", f"{math.sin(0.01):.12f}")
show("L13 P3 h* (M3=e) check", f"{(3*delta/e)**(1/3):.5e}")

# ---- L14 ----
show("L14 exp(sin 1)", f"{math.exp(math.sin(1)):.10f}")
show("L14 cos 1", f"{math.cos(1):.10f}")
show("L14 sin 1", f"{math.sin(1):.10f}")
show("L14 2*exp(sin1)*cos1 (unrounded)", f"{2*math.exp(math.sin(1))*math.cos(1):.12f}")
show("L14 printed-factor product 2.3197768247*0.5403023059*2",
     f"{2.3197768247*0.5403023059*2:.10f}")
show("L14 f1(2) exact", f"{2*math.exp(2)+ (math.sin(2)/2):.10f}")
show("L14 Example 4.1 tangent sum", f"{math.exp(2)+2*math.exp(2)+(2*math.cos(2)-math.sin(2))/4:.10f}")
show("L14 e^2", f"{math.exp(2):.9f}")
show("L14 f2'(1)", f"{math.exp(math.sin(1))*math.cos(1)*2:.10f}")
show("L14 x=2 Ex4.1 quotient tangent", f"{(-math.sin(2)*0 + (math.cos(2)*2 - math.sin(2))/4):.9f}")
show("L14 Example 4.1 pieces: 0.454648713, -0.435397775",
     f"{math.sin(2)/2:.9f} {(2*math.cos(2)-math.sin(2))/4:.9f}")
show("L14 Example 5.1 cos1 and 2+cos1", f"{math.cos(1):.9f} {2+math.cos(1):.9f}")
show("L14 Example 5.1 sin1", f"{math.sin(1):.9f}")

# ---- L15 ----
show("L15 2/(3 sqrt3)", f"{2/(3*math.sqrt(3)):.8f}")
best = 0.0
best_deg = None
vals = {}
for k in range(360):
    th = 2 * math.pi * k / 360
    v = abs(math.cos(th) ** 2 * math.sin(th))
    vals[k] = v
    if v > best:
        best, best_deg = v, k
show("L15 max over 1-degree samples of |cos^2 sin|", f"{best:.8f} at {best_deg} deg")
top = sorted(vals.items(), key=lambda kv: -kv[1])[:6]
show("L15 top 6 sampled angles (deg, value)", [(k, round(v, 8)) for k, v in top])
show("L15 asin(1/sqrt3) in degrees", f"{math.degrees(math.asin(1/math.sqrt(3))):.6f}")
show("L15 g max over samples", f"{max(abs(math.cos(2*math.pi*k/360)*math.sin(2*math.pi*k/360)) for k in range(360)):.8f}")
show("L15 |f| at 35, 145, 215, 325 deg",
     [round(abs(math.cos(math.radians(a))**2*math.sin(math.radians(a))), 8) for a in (35, 145, 215, 325)])

# ---- L16 ----
F = lambda x, y: x * x * y + math.exp(x * y)
grid = [(x, y) for x in (0.5, 1.0, 1.5, 2.0) for y in (-1.0, 0.0, 1.0)]
Fmax = max(grid, key=lambda p: abs(F(*p)))
show("L16 largest |F| on 12-point grid", f"{Fmax} value {F(*Fmax):.6f}")
show("L16 4+e^2", f"{4+math.exp(2):.6f}")
show("L16 F_x(1,2) closed", f"{4+2*math.exp(2):.9f}")
show("L16 F_y(1,2) closed", f"{1+math.exp(2):.9f}")
show("L16 ulp half at 11.389 (delta)", f"{2.0**-53*8:.4e}")
show("L16 delta/h at h=1e-5 with delta=8.88e-16", f"{8.8817841970012523e-16/1e-5:.4e}")
show("L16 trunc bound (1e-10/6)*e^2", f"{1e-10/6*math.exp(2):.4e}")
show("L16 R3 truncation (h^2/6)*20", f"{1e-10/6*20:.4e}")
show("L16 y^3 e^{xy} at (2,1)", f"{math.exp(2):.6f}")
show("L16 8 e^2", f"{8*math.exp(2):.4f}")
show("L16 E3 2+3e^2", f"{2+3*math.exp(2):.6f}")

# ---- L17 ----
c = math.cos(0.5)
gy = 1 + c
L = math.hypot(1.0, gy)
show("L17 cos 0.5", f"{c:.10f}")
show("L17 gradient length", f"{L:.10f}")
show("L17 angle deg", f"{math.degrees(math.atan(gy)):.6f}")
show("L17 unit w", f"{1/L:.6f} {gy/L:.6f}")
show("L17 E3 alpha deg and rad", f"{62-math.degrees(math.atan(gy)):.6f} {math.radians(62-math.degrees(math.atan(gy))):.6e}")
alpha = math.radians(62 - math.degrees(math.atan(gy)))
show("L17 E3 |w|(1-cos alpha)", f"{L*(1-math.cos(alpha)):.6e}")
show("L17 E3 alpha^2/2*|w|", f"{L*alpha*alpha/2:.6e}")
show("L17 R1 max-norm sup = 1+gy", f"{1+gy:.7f}")
show("L17 R1 Euclid direction", f"{1/L:.5f} {gy/L:.5f}")
show("L17 R1 rescaled (w1/w2,1) value", f"{(1/gy)+gy:.6f}")
show("L17 R1 (1+gy^2)/gy exact", f"{(1+gy*gy)/gy:.6f}")
show("L17 w1/w2", f"{1/gy:.6f}")
show("L17 E2 truncation bound 7e-12/6", f"{1e-12/6*7:.4e}")
show("L17 E2 rounding 1e-16/1e-6", f"{1e-16/1e-6:.2e}")

# ---- L18 ----
show("L18 rounding delta near 4 (ulp 2^-50 half)", f"{2.0**-51:.4e} rounding delta/h={2.0**-51/1e-5:.4e}")
show("L18 check 4.44e-16/1e-5", f"{4.44e-16/1e-5:.3e}")

for line in out:
    print(line)
