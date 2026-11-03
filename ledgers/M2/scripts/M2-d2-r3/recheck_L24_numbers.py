# Independent recomputation of L24 numbers (own code, not the twin's functions). Usage: python -I recheck_L24_numbers.py
import math
from decimal import Decimal as D, getcontext
getcontext().prec = 50
E_TRUE = D("2.71828182845904523536028747135266249775724709369995")
def fwd(f, x, h): return (f(x + h) - f(x)) / h
def cen(f, x, h): return (f(x + h) - f(x - h)) / (2 * h)
ex = math.exp
print("Part A kink, own code:")
for k in range(1, 7):
    h = 10.0 ** -k
    absf = abs
    print(k, "%+.6f" % fwd(absf, 0.0, h), "%+.6f" % ((abs(0.0) - abs(-h)) / h), "%+.6f" % ((abs(h) - abs(-h)) / (2 * h)))
print("Part B: float error vs math.e (as the lab) and vs 50-digit e (exact in Decimal), forward and central")
rows = {}
for k in range(1, 16):
    h = 10.0 ** -k
    ef = abs(fwd(ex, 1.0, h) - math.e)
    ec = abs(cen(ex, 1.0, h) - math.e)
    rows[k] = (ef, ec)
    print("k=%2d h=%.0e fwd %.3e cen %.3e" % (k, h, ef, ec))
print("argmin forward decade:", min(rows, key=lambda k: rows[k][0]), "argmin central decade:", min(rows, key=lambda k: rows[k][1]))
# unrounded central errors at 1e-5 and 1e-7, and their difference
e5 = rows[5][1]; e7 = rows[7][1]
print("central err 1e-5 = %.10e, 1e-7 = %.10e, difference = %.4e" % (e5, e7, e5 - e7))
print("ulp(e) = 2^-51 =", 2 ** -51)
print("2*delta/h at 1e-15 with delta=2.22e-16:", 2 * 2.22e-16 / 1e-15)
print("predicted forward minimizer 2 sqrt(delta/e) =", 2 * math.sqrt(2.22e-16 / math.e))
print("predicted central minimizer (3 delta/e)^(1/3) =", (3 * 2.22e-16 / math.e) ** (1 / 3))
print("truncation 1/2 e h at 1e-5 =", 0.5 * math.e * 1e-5)
print("central factor 4.531e-9/5.859e-11 =", 4.531e-9 / 5.859e-11)
print("forward err 1e-1 -> 1e-5 printed 1.406e-1 and 1.359e-5")
print("e - math.e (exact minus float) =", float(E_TRUE - D(repr(math.e))))
