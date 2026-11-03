"""Re-derive every number in the L23 and L24 prose that is not a verbatim lab print (run under pinned CPython)."""
import math
from fractions import Fraction
import importlib.util, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    return spec, mod

# ---- L23: load the twin without running main() by reading only the functions (main() runs at import, so exec the text minus the final call)
src = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()\n", "\n")
ns = {}
exec(compile(src, "twin_L23_nomain", "exec"), ns)
price, taylor_first, taylor_second = ns["price"], ns["taylor_first"], ns["taylor_second"]
price_first_derivative, price_second_derivative = ns["price_first_derivative"], ns["price_second_derivative"]
price_cents = ns["price_cents"]
y0 = 0.04
print("L23 unrounded price at y0:", float(price(y0)))
for dy in (0.01, -0.01):
    e2 = price(y0 + dy) - taylor_second(y0, dy)
    print(f"L23 second-order error (exact - expansion) at dy={dy:+}: {float(e2):.6f} cents; abs {abs(float(e2)):.6f}")
    print("   exact price cents", float(price(y0+dy)), " expansion", float(taylor_second(y0, dy)), " cents-rounded diff", price_cents(y0+dy)-round(taylor_second(y0,dy)))
# float yield at 5 percent
yf = 0.04 + 0.01
print("L23 0.04+0.01 =", repr(yf), " float(0.05) =", repr(0.05), " difference =", Fraction(yf) - Fraction(0.05), float(Fraction(yf)-Fraction(0.05)))
d = float(Fraction(yf) - Fraction(0.05))
pp = price_first_derivative(0.05)
print("L23 P'(0.05) =", pp, " price change from float offset =", pp * d, "cents")
print("L23 unrounded price at float 0.05:", float(price(yf)), " exact-5% price:", float(price(0.05)))
# Quiz q8: c1=-1, c2=1000 at y=0.04
c = {1: -1, 2: 1000}
y = 0.04
v = 1 + Fraction(y)
Pp = -sum((Fraction(t * c[t]) / v ** (t + 1) for t in (1, 2)), Fraction(0))
print("L23 quiz q8 P'(0.04) with c1=-1, c2=1000:", float(Pp))
# Prop 2.2 sanity: 5% coupon, 10 years, face 100000 at yield 0.05
print("L23 price at 0.05 (should be 100000):", float(price(0.05)))
# Preview numbers
print("preview -P'/P", -price_first_derivative(0.04)/float(price(0.04)), " P''/P", price_second_derivative(0.04)/float(price(0.04)))

# ---- L24
def central(f, x, h): return (f(x+h)-f(x-h))/(2*h)
e = math.e
for k in (5, 7):
    h = 10.0**-k
    val = central(math.exp, 1.0, h)
    err = abs(val - e)
    print(f"L24 central at k={k}: value {val!r} unrounded error {err:.10e}")
    # exact-arithmetic reference for the error using high-precision decimals
from decimal import Decimal, getcontext
getcontext().prec = 60
def dexp(x): return Decimal(x).exp()
E = Decimal(1).exp()
for k in (5, 7):
    h = Decimal(10) ** (-k)
    # the lab's own float quotient, with the float h
    hf = 10.0 ** -k
    fq = (math.exp(1.0 + hf) - math.exp(1.0 - hf)) / (2.0 * hf)
    print(f"L24 float quotient k={k}: fq={fq!r}  |fq-e| as float={abs(fq-math.e):.6e}")
    print(f"   |fq - e| using Decimal e: {abs(Decimal(fq) - E):.6e}")
print("L24 central error ratio 4.531e-9/5.859e-11 =", 4.531e-9/5.859e-11)
print("L24 ulp(e) =", math.ulp(math.e), " half ulp", math.ulp(math.e)/2, " 2^-52=", 2.0**-52)
print("L24 2*delta/1e-15 =", 2*2.22e-16/1e-15)
print("L24 predicted minimizers:", 2*math.sqrt(2.22e-16/math.e), (3*2.22e-16/math.e)**(1/3))
print("L24 forward at 1e-5 vs 0.5*e*h:", 0.5*math.e*1e-5)
