import math
pi4 = math.pi / 4
c = math.atan(2) - pi4
print("pi/4", f"{pi4:.10f}", "c=arctan2-pi/4", f"{c:.12f}", "printed 0.3217505544 diff", f"{c - 0.3217505544:+.2e}")
print("9c", f"{9*c:.10f}", "<3", 9*c < 3, "10c", f"{10*c:.9f}", ">3", 10*c > 3)
print("quad y-first error", f"{0.7853982936 - pi4:+.2e}", "closed printed 0.7853981634 vs pi/4", f"{0.7853981634 - pi4:+.2e}")
print("diff 0.7853982936-0.7853981634 =", f"{0.7853982936 - 0.7853981634:.10f}")
# c_k = integral over [1,2] of 1/(1+t^2), midpoint rule with 200000 cells, and min integrand on [1,2]
n = 200000
s = sum(1.0 / (1.0 + ((1 + (i + 0.5) / n)) ** 2) for i in range(n)) / n
print("numeric c", f"{s:.10f}", "min integrand on [1,2]", f"{1/(1+4):.4f}", "c>=1/5", s >= 0.2)
# block integral check: integral over x in [a,2a] of a/(x^2+a^2) dx equals the same c for several a
for k in range(4):
    a = 2.0 ** (-(k + 1))
    m = 200000
    tot = sum(a / ((a + (i + 0.5) * a / m) ** 2 + a * a) for i in range(m)) * a / m
    print("k", k, "a_k", a, "block integral", f"{tot:.10f}")
# f >= 0 on blocks and denominator bound a^4 on closed rectangle
ok = all((x*x - y*y) >= 0 for a in [2.0**-(k+1) for k in range(5)] for x in [a+(2*a-a)*i/50 for i in range(51)] for y in [a*j/50 for j in range(51)] if x > a and y <= a)
print("f>=0 on blocks sample", ok)
