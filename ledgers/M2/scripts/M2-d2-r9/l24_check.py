import math
from decimal import Decimal, getcontext
from fractions import Fraction
getcontext().prec = 80
e_dec = Decimal(1).exp()
target = math.e
def fwd(x,h): return (math.exp(x+h)-math.exp(x))/h
def cen(x,h): return (math.exp(x+h)-math.exp(x-h))/(2*h)
for k in range(1,16):
    h = 10.0**-k
    f = fwd(1.0,h); c = cen(1.0,h)
    ef_signed = f - target; ec_signed = c - target
    # exact (decimal, using exact e) errors
    hd = Decimal(10)**(-k)
    ex_f = (Decimal(1)+hd).exp()  # placeholder
    exact_fwd = (e_dec*(hd.exp()-1)/hd) - e_dec if False else None
    print(f"k={k:2d} computed fwd signed {ef_signed:+.6e}  cen signed {ec_signed:+.6e}")
print("exact fwd error at 1e-8 (decimal):", float(e_dec*((Decimal("1e-8")).exp()-1)/Decimal("1e-8") - e_dec))
print("exact cen error at 1e-4 (decimal):", float(e_dec*(Decimal("1e-4").exp()-Decimal("-1e-4").exp())/(2*Decimal("1e-4")) - e_dec))
# exact central quotient error: e*sinh(h)/h - e  (exact in decimal)
def exact_cen(h):
    hd = Decimal(h)
    sh = (hd.exp() - (-hd).exp())/2
    return e_dec*sh/hd - e_dec
def exact_fwd(h):
    hd = Decimal(h)
    return e_dec*(hd.exp()-1)/hd - e_dec
for k in [1,2,3,4,5,6,7,8,9,10]:
    h = 10.0**-k
    print("exact fwd err k=%d: %.6e   exact cen err: %.6e" % (k, float(exact_fwd(Decimal(10)**(-k))), float(exact_cen(Decimal(10)**(-k)))))
c5 = cen(1.0,1e-5); c7 = cen(1.0,1e-7)
print("central at 1e-5:", repr(c5), " at 1e-7:", repr(c7), " diff:", c5-c7, " diff/ulp(e)", (c5-c7)/2**-51)
print("cen(1e-5)-e signed", c5-target, " cen(1e-7)-e", c7-target)
print("cen(1e-5) round-off part:", (c5-target) - float(exact_cen(Decimal("1e-5"))))
print("cen(1e-6) signed - exact:", cen(1.0,1e-6)-target, float(exact_cen(Decimal("1e-6"))))
print("fwd(1e-9) exact", float(exact_fwd(Decimal("1e-9"))), " fwd computed signed", fwd(1.0,1e-9)-target)
print("fwd(1e-8) exact", float(exact_fwd(Decimal("1e-8"))))
print("cen(1e-4) exact", float(exact_cen(Decimal("1e-4"))))
print("ratio 4.531e-9/5.859e-11 =", 4.531e-9/5.859e-11)
print("half ulp e =", 2**-52 , "ulp for [2,4) =", 2**-51)
print("predicted minimizers: 2*sqrt(delta/e) =", 2*math.sqrt(2.22e-16/math.e), " (3 delta/e)^(1/3) =", (3*2.22e-16/math.e)**(1/3))
print("round-off bound 2 delta/h at 1e-15 =", 2*2.22e-16/1e-15)
print("M3 forward (page): 12.61? see later")
