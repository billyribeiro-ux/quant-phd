"""Independent recomputation of L14 numbers (verifier round 3). Standard library only, unrounded values."""
import math
e = math.e
print("e^2 =", math.exp(2), " 2e^2 =", 2 * math.exp(2), " 3e^2 =", 3 * math.exp(2))
print("sin2 =", math.sin(2), " cos2 =", math.cos(2))
f1 = 2 * math.exp(2) + math.sin(2) / 2
print("f1(2) unrounded:", f1, " 9dp:", f"{f1:.9f}")
d1 = math.exp(2) + 2 * math.exp(2) + (2 * math.cos(2) - math.sin(2)) / 4
print("f1'(2) closed form unrounded:", d1, " 9dp:", f"{d1:.9f}", " 10dp:", f"{d1:.10f}")
print("sum of Example 4.1 rounded terms:", 22.167168297 - 0.435397775, " 9dp of that:", f"{22.167168297 - 0.435397775:.9f}")
print("Example 4.1 quotient part 0.909297427/2 =", 0.909297427 / 2, " tangent part:", (-0.416146837 * 2 - 0.909297427) / 4)
print("E1 exp(sin1) =", math.exp(math.sin(1)), " cos1 =", math.cos(1), " sin1 =", math.sin(1))
print("E1 rounded-factor product:", 2.3197768247 * 0.5403023059 * 2, " 10dp:", f"{2.3197768247 * 0.5403023059 * 2:.10f}")
print("E1 unrounded 2 exp(sin1) cos1 =", 2 * math.exp(math.sin(1)) * math.cos(1), " 10dp:", f"{2 * math.exp(math.sin(1)) * math.cos(1):.10f}")
f2p = math.exp(math.sin(1)) * math.cos(1) * 2
print("f2'(1) 10dp:", f"{f2p:.10f}")
print("f2(1) closed:", math.exp(math.sin(1)))
print("E3 / Example: L13 comparison not here")
print("M1 g'(2) =", 2 * 2 + 3)
print("E2 grid check exists: grid min 0.5 max 3.0 count 251 ->", len([0.5 + i / 100 for i in range(251)]), 0.5 + 250 / 100)
print("branch-sensitivity: |x| dual tangent with x>0 else -x at 0: tangent -1 (conceptual)")
