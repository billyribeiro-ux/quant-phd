"""Independent recomputation of L02 numbers (floating point, printed at stated precision)."""
import math

F = 5000 * math.exp(0.05 * 0.5)
print("F* cents unrounded", F, "display", f"{F:.2f}")
print("Example 2.4 dollars", 50 * math.exp(0.025), f"{50 * math.exp(0.025):.4f}")
print("M1 50e^0.025", 50 * 1.0253151205, "e^0.025 =", math.exp(0.025))
print("M2 e^0.01", math.exp(0.01), "80e^0.01", 80 * math.exp(0.01), "profit", 81 - 80 * math.exp(0.01))
print("M3 e^-0.015", math.exp(-0.015), "100e^-0.015", 100 * math.exp(-0.015), "value", 104 - 100 * math.exp(-0.015))
print("E3 e^-0.0125", math.exp(-0.0125), "F e^-0.0125", F * math.exp(-0.0125), "value", 5300 - F * math.exp(-0.0125))
print("E3 with 8-place factor 0.98757780:", F * 0.98757780, 5300 - F * 0.98757780)
print("E3 with F=5126.58:", 5300 - 5126.58 * math.exp(-0.0125))
print("R3 e^0.1", math.exp(0.1), "1.05^2", 1.05 ** 2, "diff", math.exp(0.1) - 1.1025)
print("Remark 2.5 e^{r tau}>1 check", math.exp(0.05 * 0.5) > 1)
print("R3 0.0027: diff rounded", round(math.exp(0.1) - 1.1025, 4))
print("e^0.1 four places", f"{math.exp(0.1):.4f}")
print("P2 derivatives at sample point S=5000,r=.05,tau=.5: dF/dr=", 5000 * 0.5 * math.exp(0.025), " dF/dtau=", 5000 * 0.05 * math.exp(0.025))
