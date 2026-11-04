"""Machine constants and hand-arithmetic values quoted on the L22-L24 pages."""
import math
import sys
print("sys.float_info.epsilon =", sys.float_info.epsilon)
print("sqrt(epsilon) =", math.sqrt(sys.float_info.epsilon))
print("2^-53 =", 2.0 ** -53, " half ulp(e) =", math.ulp(math.e) / 2)
print("L22 objective change at a=1.5: 0.5*0.666667*(1e-8)^2 =", 0.5 * 0.666667 * 1e-16)
print("L22 f_xx at a=1.5, x=0.5:", -1.5 / (1.5) ** 2)
print("L24 M3: (2.1**3-8)/0.1 =", (2.1 ** 3 - 8) / 0.1, " 0.5*12.6*0.1 =", 0.5 * 12.6 * 0.1)
print("L24 E2: 2*2.22e-16/1e-15 =", 2 * 2.22e-16 / 1e-15)
print("L23 M1: 50/1.05+1050/1.05**2 =", 50 / 1.05 + 1050 / 1.05 ** 2)
