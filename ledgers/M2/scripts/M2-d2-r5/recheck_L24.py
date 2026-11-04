# Independent recomputation of the L24 numbers. Does not import the lab twin.
import math
from decimal import Decimal, getcontext
getcontext().prec = 60
e = math.e
def fwd(x, h): return (math.exp(x + h) - math.exp(x)) / h
def cen(x, h): return (math.exp(x + h) - math.exp(x - h)) / (2 * h)
for k in range(1, 16):
    h = 10.0 ** -k
    print("k=%2d h=%.0e fwd err %.3e cen err %.3e" % (k, h, abs(fwd(1.0, h) - e), abs(cen(1.0, h) - e)))
# unrounded central errors at 1e-5 and 1e-7 (exact decimal of the float quotient)
for k in (5, 7):
    h = 10.0 ** -k
    c = cen(1.0, h)
    print("k=%d central float %.17g err %.9e" % (k, c, abs(c - e)))
print("ulp(e) =", math.ulp(e), " half ulp =", math.ulp(e) / 2)
d5 = abs(cen(1.0, 1e-5) - e); d7 = abs(cen(1.0, 1e-7) - e)
print("diff of unrounded errors 1e-5 vs 1e-7 = %.6e" % abs(d5 - d7))
# E2 bound
delta = 2.22e-16
print("2 delta/1e-15 =", 2 * delta / 1e-15, " printed 0.3903")
print("2 sqrt(delta/e) =", 2 * math.sqrt(delta / e), " (3 delta/e)^(1/3) =", (3 * delta / e) ** (1 / 3))
print("half e h at 1e-5 =", 0.5 * e * 1e-5, " half e h at 1e-5 printed 1.359e-05")
print("4.531e-9/5.859e-11 =", 4.531e-9 / 5.859e-11)
print("log10 6.3e-6 =", math.log10(6.3e-6))
# Part A printed values (exact in float)
print([ (abs(1.0)-0)/1e-3 ])
