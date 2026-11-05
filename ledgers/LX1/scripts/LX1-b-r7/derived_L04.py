"""Derived numbers on L04 (LX1-b r7): M1, M2, M3, E2, R2 and the quiz bound, recomputed from exact formulas."""
import math
from fractions import Fraction as F
print("M1 ln1.1 =", round(math.log(1.1), 6), " simple-minus-log =", round(0.1 - math.log(1.1), 6))
mean = F(2, 100) / 3
ss = F(1, 10000) + F(9, 10000) + F(4, 10000)
dev = ss - 3 * (F(1, 150)) ** 2
print("M2 mean =", float(mean), " sum sq dev =", dev, " == 19/15000:", dev == F(19, 15000), " disp =", round(math.sqrt(float(dev) / 2), 6), " sqrt(19/30000) =", round(math.sqrt(19 / 30000), 6))
L = 0.13584567275950138  # Lab 1 Part C window one largest absolute change, unrounded
print("R2 tanh(L/2) =", math.tanh(L / 2), " 6dp:", round(math.tanh(L / 2), 6), " 4dp:", round(math.tanh(L / 2), 4))
print("R2 bound at h=0.0678:", math.log((1 + 0.0678) / (1 - 0.0678)))
x = -0.0965747399762115  # window two largest move, signed
print("E2 simple change =", math.exp(x) - 1, " 6dp:", round(math.exp(x) - 1, 6))
print("M3 window-two count:", 26 * 12 + 9)
print("E3 L04 Part D difference printed:", round(0.024700 - 0.027935, 6))
