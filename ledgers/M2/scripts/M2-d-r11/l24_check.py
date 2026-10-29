import math
from fractions import Fraction
e = math.e
def c(h):
    return (math.exp(1+h) - math.exp(1-h))/(2*h)
a = c(1e-5) - e; b = c(1e-7) - e
print("central err 1e-5 unrounded", repr(a), "1e-7", repr(b), "diff", abs(a-b))
print("ulp near e", math.ulp(e))
print("e-spacing check: 1e-5 err %.9e  1e-7 err %.9e" % (abs(a), abs(b)))
print("2*delta/h at 1e-15:", 2*2.22e-16/1e-15, "printed 0.390 vs 3.903e-1")
print("bound 0.5*e*h at 1e-5", 0.5*e*1e-5, "at 0.1", 0.5*e*0.1)
print("pred forward min 2sqrt(delta/e)", 2*math.sqrt(2.22e-16/e), " central (3delta/e)^(1/3)", (3*2.22e-16/e)**(1/3))
# independent kink check with Fractions for |x| at 0
for k in range(1,7):
    h = Fraction(1, 10**k)
    print(k, float((abs(h)-0)/h), float((0-abs(-h))/h), float((abs(h)-abs(-h))/(2*h)))
