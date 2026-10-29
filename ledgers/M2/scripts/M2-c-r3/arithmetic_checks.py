"""Round-3 numeric checks for the displayed digits quoted in L13-L18 prose (python -I)."""
import math

# L13 Example 2.3 intervals
print("L13 forward h=0.01:", 0.005 * math.e, 0.005 * math.exp(1.01))
print("L13 central h=0.01:", 1e-4 / 6 * math.exp(0.99), 1e-4 / 6 * math.exp(1.01))
# L13 Corollary 4.1 with M=e, delta=2^-52
d = 2.0**-52
print("L13 h* forward:", 2 * math.sqrt(d / math.e), "central:", (3 * d / math.e) ** (1 / 3), "B(h*):", 2 * math.sqrt(math.e * d))
print("L13 R1 h*:", 2 * math.sqrt(1e-3 / math.e))
print("L13 misc ratio 2.154e-7/6.603e-9 =", 2.154e-7 / 6.603e-9, " 1.364e-2/4.530e-5 =", 1.364e-2 / 4.530e-5)
# L14 Example 4.1 and E1 product
print("L14 E1 product from displayed factors:", repr(2.3197768247 * 0.5403023059 * 2))
print("L14 E1 product from full precision:", repr(math.exp(math.sin(1)) * math.cos(1) * 2))
print("L14 f1(2), f1'(2):", 2 * math.exp(2) + math.sin(2) / 2, math.exp(2) + 2 * math.exp(2) + (2 * math.cos(2) - math.sin(2)) / 4)
# L15 2/(3 sqrt 3)
print("L15 max |f|/r:", 2 / (3 * math.sqrt(3)))
# L17 gradient
g = (1.0, 1 + math.cos(0.5))
n = math.hypot(*g)
print("L17 |grad|:", n, "angle deg:", math.degrees(math.atan2(g[1], g[0])), "L-inf steepest value:", n / max(abs(c) / n for c in g))
