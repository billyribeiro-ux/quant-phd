# Independent recomputation for L09 numeric claims (run with python3 -I).
import math
d = math.sqrt(3) / 2  # ||V_1 - V_0|| on the four-point grid, V_0 = 0 (value at k = 1.0)
print("R2 a priori least n for bound <= 1e-6:", next(n for n in range(1, 10000) if 0.9**n * d / 0.1 <= 1e-6))
for n in (151, 152):
    print("R2 bound at n =", n, 0.9**n * d / 0.1)
print("E2 ratio actual/step:", 0.0000085808 / 0.0000009534)
print("quiz 0.9^10/0.1 =", 0.9**10 / 0.1)
print("M1 factors:", 0.5 / 0.5, 0.9 / 0.1, 0.99 / 0.01)
print("M3 largest step for 1e-3 at beta 0.9:", 1e-3 * (1 - 0.9) / 0.9)
print("Theorem 2.4 threshold ln(tau(1-b)/d)/ln b:", [round(math.log(1e-12 * (1 - b) / d) / math.log(b), 2) for b in (0.5, 0.9, 0.95)])
print("naive stop error over tolerance:", 0.0000085808 / 1e-6)
