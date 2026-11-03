"""Numeric re-derivation of the minimizers and the envelope/constraint formulas on L22 and L24 (verifier round 3)."""
import math

# Prop 4.2: g(h) = A h + B/h, A = M2/2, B = 2 delta; claimed h* = 2 sqrt(delta/M2), g(h*) = 2 sqrt(M2 delta)
d, M2, M3 = 2.22e-16, math.e, math.e
A, B = M2 / 2, 2 * d
g = lambda h: A * h + B / h
hs = 2 * math.sqrt(d / M2)
grid = [hs * (1 + k / 1000) for k in range(-900, 901)]
best = min(grid, key=g)
print("P4.2 claimed h*", hs, "grid argmin", best, "g(h*)", g(hs), "2sqrt(M2 d)", 2 * math.sqrt(M2 * d))
# Prop 4.3: g(h) = C h^2 + B/h, C = M3/6, B = delta; claimed h*^3 = 3 delta / M3
C, B3 = M3 / 6, d
g3 = lambda h: C * h * h + B3 / h
hs3 = (3 * d / M3) ** (1 / 3)
grid3 = [hs3 * (1 + k / 1000) for k in range(-900, 901)]
print("P4.3 claimed h*", hs3, "grid argmin", min(grid3, key=g3))
# Example 1.5: V(a)= a ln a - (a-1), V'(a)=ln a; central difference check at a=1.5
V = lambda a: a * math.log(a) - (a - 1)
a = 1.5; h = 1e-5
print("Ex1.5 V' numeric", (V(a + h) - V(a - h)) / (2 * h), "ln a", math.log(a))
# Example 2.2: V(a)=a^2/4, V'=a/2; Prop 2.1 term g_y c_a = (a/2)(1)
print("Ex2.2 numeric V'(2)", ((2 + h) ** 2 / 4 - (2 - h) ** 2 / 4) / (2 * h), "a/2 =", 1.0)
# M1 (L22) f=ax - x^2/2 ; V=a^2/2 ; V(a)=5/2 at a^2=5
print("L22 quiz V with a^2=5:", 5 / 2)
# L22 misconception: second-order error 0.5*0.666667*1e-16
print("L22 location-error objective change:", 0.5 * (1.5 / (1.5) ** 2) * 1e-16)
# L23 P3 zero coupon: P'(0.04) = -200/1.04^3
print("L23 zero-coupon P'(0.04):", -200 / 1.04 ** 3)
# L24 M3 numbers: forward truncation bound example: f=x^3 at 2, h=0.1
print("L24 M3 check: D+ err", (2.1 ** 3 - 8) / 0.1 - 12, "bound", 0.5 * 12.6 * 0.1)
# L24 R1: 2 delta/h* equals sqrt(M2 delta)
print("L24 R1: 2d/h* =", 2 * d / hs, " sqrt(M2 d) =", math.sqrt(M2 * d))
