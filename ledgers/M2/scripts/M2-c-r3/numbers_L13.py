"""Independent recomputation of the L13 numbers (verifier round 3). Standard library only."""
import math

e = math.e
d = 2.0 ** -52
def fwd(h): return (math.exp(1 + h) - math.exp(1)) / h
def cen(h): return (math.exp(1 + h) - math.exp(1 - h)) / (2 * h)

print("forward err 1e-2 unrounded:", fwd(1e-2) - e, " lo/hi bound:", e * 0.005, math.exp(1.01) * 0.005)
print("central err 1e-2 unrounded:", cen(1e-2) - e, " bounds:", math.exp(0.99) * 1e-4 / 6, math.exp(1.01) * 1e-4 / 6)
ratio_f = (fwd(1e-2) - e) / (fwd(1e-3) - e)
print("forward ratio unrounded 1e-2/1e-3:", ratio_f, "interval:", 10 * math.exp(-0.001), 10 * math.exp(0.01))
ratio_c = (cen(1e-2) - e) / (cen(1e-3) - e)
print("central ratio unrounded 1e-2/1e-3:", ratio_c, "interval:", 100 * math.exp(-0.011), 100 * math.exp(0.011))
print("MC1 forward/central ratio at 1e-2, unrounded:", (fwd(1e-2) - e) / (cen(1e-2) - e))
print("MC1 printed digits 1.364e-2/4.530e-5:", 1.364e-2 / 4.530e-5)
print("MC1 forward 2.154e-7 / 6.603e-9:", 2.154e-7 / 6.603e-9)
print("E2 2d/h at 1e-8, 1e-9:", 2 * d / 1e-8, 2 * d / 1e-9)
print("E2 truncation h/2 e at 1e-8, 1e-9:", 0.5e-8 * e, 0.5e-9 * e)
print("E2 ratio rounding/truncation 1e-9 (unrounded):", (2 * d / 1e-9) / (0.5e-9 * e))
print("E2 total bound 1e-9:", 2 * d / 1e-9 + 0.5e-9 * e)
print("balanced forward h* = 2 sqrt(d/e):", 2 * math.sqrt(d / e), " B(h*) = 2 sqrt(e d):", 2 * math.sqrt(e * d))
print("balanced central h* = (3d/e)^(1/3):", (3 * d / e) ** (1 / 3), " 3d/e:", 3 * d / e)
print("R1 h* = 2 sqrt(1e-3/e):", 2 * math.sqrt(1e-3 / e))
print("R3 2^-53/1e-8:", 2.0 ** -53 / 1e-8, " e*that:", e * 2.0 ** -53 / 1e-8)
print("sec5 2 sqrt(e*2^-52):", 2 * math.sqrt(e * d))
print("Lab hypothesis h* forward 2 sqrt(d/e) ~ 1.8e-8 ok; e^h0-1 at h0=2e-8:", math.exp(2e-8) - 1)
print("M1 D_0.1 t^2 at 1:", ((1.1) ** 2 - 1) / 0.1)
print("M3 sin(0.01)/0.01:", math.sin(0.01) / 0.01, " err:", math.sin(0.01) / 0.01 - 1, " 0.005 sin(0.01):", 0.005 * math.sin(0.01))
print("Ex2.3 central interval endpoints check:", e * 0.005, math.exp(1.01) * 0.005)
print("Quiz numeric t^2 at 1 h=0.5:", ((1.5) ** 2 - 1) / 0.5)
print("P3 B_c(h*) identity 3d/(2h*) vs direct:", 3 * d / (2 * (3 * d / e) ** (1 / 3)), (e / 6) * (3 * d / e) ** (2 / 3) + d / (3 * d / e) ** (1 / 3))
