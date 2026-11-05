"""Recompute the L02 E3 numbers from the lab seed (standard library only).

Usage: python -I e3_l02_check.py
"""
import math
import random

SEED = 20260101
rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
xi11 = rng.gauss(0.0, 1.0)
sup1 = abs(xi11) * 2 ** (-1.0)
print("xi_{1,1} (unrounded) =", repr(xi11))
print("level-1 observed sup (unrounded) =", repr(sup1), "rounded 6dp:", f"{sup1:.6f}")
print("twice the unrounded sup =", f"{2 * sup1:.10f}", "rounded 6dp:", f"{2 * sup1:.6f}")
print("twice the printed 6dp sup =", f"{2 * round(sup1, 6):.6f}")
print("bound lambda_1/2 =", f"{math.sqrt(4 * math.log(2)) * 2 ** (-1.0):.10f}", "rounded 6dp:",
      f"{math.sqrt(4 * math.log(2)) * 2 ** (-1.0):.6f}")
print("sqrt(4 log 2) =", f"{math.sqrt(4 * math.log(2)):.6f}")
