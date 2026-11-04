"""Round-6 check of L24 Remark 4.4 (line 129): 'the true error at h* is at most the bound only if h* is in H'.
Counterexample: f(x) = x^2 at x = 0, exact computed values (f~ = f, so Definition 4.1 holds with any delta > 0),
M2 = 1.5, delta = 1. Then |f''| = 2 > M2 on every interval, so H is empty and h* is not in H, yet the true error
at h* is below the bound. Standard library only."""
import math
f = lambda t: t * t
fprime0 = 0.0
M2, delta = 1.5, 1.0
hstar = 2 * math.sqrt(delta / M2)
D_plus = (f(0.0 + hstar) - f(0.0)) / hstar
true_error = abs(D_plus - fprime0)
bound = 0.5 * M2 * hstar + 2 * delta / hstar
print(f"h* = {hstar:.6f}; D+ = {D_plus:.6f}; true error = {true_error:.6f}; bound g(h*) = {bound:.6f}")
print("true error <= bound:", true_error <= bound)
# H membership: need |f''| = 2 <= M2 = 1.5 on [0, h*]; it fails for every h > 0
print("|f''| on [0, h*] =", 2.0, " <= M2?", 2.0 <= M2, " => h* in H is False")
print("min over h>0 of g equals 2 sqrt(M2 delta) =", 2 * math.sqrt(M2 * delta), "; g(h*) =", bound)
