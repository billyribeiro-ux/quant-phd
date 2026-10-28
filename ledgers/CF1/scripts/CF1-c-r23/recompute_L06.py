# Independent recomputation of L06 numbers (round 23). Run as: python -I this.py
import math, random, statistics
from fractions import Fraction
# E1
err = 84543.40 - 79078.68
print("E1 error cents", round(err, 2))
q_disp = err / 4400.22
print("E1 ratio from displayed digits", round(q_disp, 6))
q_unr = (5464.72) / 4400.22
print("E1 ratio 5464.72/4400.22", q_unr)
def Phi(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
for z in (1.2419, 1.242, 1.24206):
    print("two-sided tail at", z, round(2 * (1 - Phi(z)), 5))
# E2
p, se = 0.0552, 0.0010
print("E2 band", round(p - 1.96 * se, 5), round(p + 1.96 * se, 5))
# E3
print("E3 width", round(143406.13 - 14896.62, 2), round((143406.13 - 14896.62) / 100, 2))
# unrounded quantile difference from lab re-run
print("unrounded diff claim 128509.5035 vs 143406.126569-14896.623057 =", round(143406.126569 - 14896.623057, 4))
# share se
for cnt in (2761,):
    ph = cnt / 50000
    print("share", ph, "se", round(math.sqrt(ph * (1 - ph) / 50000), 6))
# sqrt ratio and factor
print("factor 4400.22/221.01", round(4400.22 / 221.01, 4), "sqrt(500)", round(math.sqrt(500), 4))
# closed form
INV, LOW, HIGH, Y, r = 300000, 50000, 150000, 5, 0.10
m = HIGH - LOW + 1
mean_r = (LOW + HIGH) / 2
A = sum((1 + r) ** -t for t in range(1, Y + 1))
E = -INV + mean_r * A
sd = math.sqrt(sum(((m * m - 1) / 12) / (1 + r) ** (2 * t) for t in range(1, Y + 1)))
print("closed", round(E, 2), round(sd, 2))
# SD of NPV unrounded used in 1.0008 ratio
print("sd ratio 49419.62/49379.84", round(49419.62 / 49379.84, 5))
# M-items
print("M3", round(-100 + 50 * (1 / 1.1 + 1 / 1.21), 4))
print("M2", 35 / 12, round(math.sqrt(35 / 12), 4))
print("M1 se", 300 / math.sqrt(100))
