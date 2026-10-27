"""Round 28: L07 Lab 4 interpretation (3) (line 521): T_beta = 915, b(SR) = 1 + 2 SR + 2 SR^2 at SR = 0.09, first-order sd and mean, Phi(...).
Also the Lab 4 twin's printed numbers are checked in the builder against twins/L07-4/out.txt. Usage: python -I lab4_part3_r28B.py"""
import math
from statistics import NormalDist

N = NormalDist()
SR = 0.09
b = 1 + 2 * SR + 2 * SR**2
bp = 2 + 4 * SR
sd = 1 - SR * bp / (2 * b)
T_beta = 915
mean = math.sqrt(T_beta - 1) * SR / math.sqrt(b)
p = N.cdf((mean - 1.645) / sd)
print(f"b(SR)={b:.4f} (1.1962); b'(SR)={bp:.2f} (2.36); first-order sd {sd:.4f} (0.91); sqrt(914)={math.sqrt(914):.4f}; mean {mean:.4f} (2.488); Phi((2.488-1.645)/0.911)={N.cdf((2.488-1.645)/0.911):.4f} (0.82); with unrounded: {p:.4f}")
