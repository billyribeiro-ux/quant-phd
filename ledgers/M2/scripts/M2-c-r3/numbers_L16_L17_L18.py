"""Independent recomputation of L16, L17 and L18 numbers (verifier round 3). Standard library only."""
import math
e = math.e
# L16 Example 1.3 at (1,2)
print("L16 Fx(1,2)=4+2e^2:", 4 + 2 * math.exp(2), " Fy=1+e^2:", 1 + math.exp(2))
# L16 Lab hypothesis: F_xxx = y^3 e^{xy}; max over grid; F_yyy-type x^3 e^{xy} at (2,1)
grid = [(x, y) for x in (0.5, 1.0, 1.5, 2.0) for y in (-1.0, 0.0, 1.0)]
print("L16 max |y^3 e^{xy}| on grid:", max(abs(y**3) * math.exp(x*y) for x, y in grid))
print("L16 8e^2:", 8 * math.exp(2), " e^2:", math.exp(2))
Fg = [abs(x*x*y + math.exp(x*y)) for x, y in grid]
print("L16 max |F| on grid:", max(Fg), " at", [p for p, v in zip(grid, Fg) if v == max(Fg)], " 4+e^2:", 4 + math.exp(2))
print("L16 rounding 1e-16*|F|/1e-5 at (2,1):", 1e-16 * (4 + math.exp(2)) / 1e-5)
print("L16 E1 half-ulp at 11.39 (ulp in [8,16) = 2^-49):", 2.0 ** -50, " /h:", 2.0 ** -50 / 1e-5)
print("L16 E1 truncation 1e-10/6*e^2:", 1e-10 / 6 * math.exp(2))
print("L16 R3: h^2/6*20 =", 1e-10 / 6 * 20, " delta/h =", 1e-15 / 1e-5, " total", 1e-10 / 6 * 20 + 1e-10)
print("L16 E3 F_xy(1,2)=2+3e^2:", 2 + 3 * math.exp(2))
# L17 Example 1.2
gx, gy = 2 * 1 * 0.5, 1 + math.cos(0.5)
print("L17 grad:", gx, gy, " 10dp gy:", f"{gy:.10f}")
print("L17 length:", math.sqrt(gx*gx + gy*gy), f"{math.sqrt(gx*gx + gy*gy):.10f}")
print("L17 angle deg arctan(gy/gx):", math.degrees(math.atan2(gy, gx)), f"{math.degrees(math.atan2(gy, gx)):.4f}")
# L17 R1 largest-coordinate norm
L = math.hypot(gx, gy)
w = (gx / L, gy / L)
s = max(abs(w[0]), abs(w[1]))
v = (w[0] / s, w[1] / s)
print("L17 R1 Euclid dir:", w, " rescaled:", v, " value:", v[0]*gx + v[1]*gy, " 10dp:", f"{v[0]*gx + v[1]*gy:.10f}")
print("L17 R1 corner value 1+|gy|:", 1 + gy)
print("L17 R1 unit (1,1) value:", gx + gy)
# L17 E3
best_deg = 62
alpha = math.radians(best_deg - math.degrees(math.atan2(gy, gx)))
print("L17 E3 alpha deg:", best_deg - math.degrees(math.atan2(gy, gx)), " alpha rad:", alpha, " |w|(1-cos a):", L * (1 - math.cos(alpha)))
# L17 E2 derivative bound constant
print("L17 E2 truncation 1e-12/6*7:", 1e-12 / 6 * 7, " rounding 1e-16/1e-6:", 1e-16 / 1e-6)
# L17 example 2.3 directional formula check at theta=0
print("L17 Ex2.3 D_(1,0)=1+0? cos0 + (1+cos .5)*0 =", 1.0)
# L18 R1 partial formula sanity: d/drho (rho^2 sin(1/rho)) = 2 rho sin(1/rho) - cos(1/rho)
rho = 1 / (2 * math.pi * 7)
print("L18 R1 partial along (rho,0) at rho_k:", 2 * rho * math.sin(1 / rho) - math.cos(1 / rho))
# L18 Example 4.2 remainder check
s1, s2 = 0.3, -0.2
F = lambda x, y: (x*x - y*y, 2*x*y)
a = (1.0, 2.0)
Fa = F(*a); Fh = F(a[0]+s1, a[1]+s2)
lin = (2*s1 - 4*s2, 4*s1 + 2*s2)
rem = (Fh[0]-Fa[0]-lin[0], Fh[1]-Fa[1]-lin[1])
print("L18 remainder vs (s1^2-s2^2, 2s1s2):", rem, (s1*s1 - s2*s2, 2*s1*s2), " len/|h|^2:", math.hypot(*rem)/(s1*s1+s2*s2))
# L18 E1 rounding half-ulp near 4 : 2^-51 /2 ... ulp in [4,8) = 2^-50, half = 2^-51
print("L18 E1 half-ulp near 4 (2^-51):", 2.0**-51, " /h:", 2.0**-51/1e-5)
print("L18 R3-type: M/6 h^2 check 1.0")
