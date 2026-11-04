"""Re-derive L23 numeric claims: the bond numbers, the 0.04+0.01 float offset, P'(0.05), the -15/+16 cents, the ratios, the -1777.07 example."""
import sys
from fractions import Fraction
from pathlib import Path

twin = Path(sys.argv[1]) / "tests/labs/M2/lab-M2-L23-1.py"
ns: dict = {"__name__": "twin_module"}
src = twin.read_text(encoding="utf-8").replace("\nmain()", "\n")  # import the functions without running main
exec(compile(src, str(twin), "exec"), ns)
price, p1, p2 = ns["price"], ns["price_first_derivative"], ns["price_second_derivative"]

y_float = 0.04 + 0.01
print("float 0.04+0.01 repr:", repr(y_float))
off = Fraction(y_float) - Fraction(1, 20)
print("exact offset float(0.04+0.01) - 1/20 =", float(off), "(as fraction", off, ")")
print("P'(0.05) closed form =", p1(0.05), " P'(float 0.05)=", p1(y_float))
print("unrounded price change P'*offset =", float(Fraction(p1(0.05)) * off))
print("unrounded price at float yield 0.04+0.01:", float(price(y_float)), " rounded:", round(price(y_float)))
print("unrounded price at 0.05 exact decimal:", float(price(0.05)))
print("unrounded P(0.04) =", float(price(0.04)), " P'(0.04)=", p1(0.04), " P''(0.04)=", p2(0.04))
print("-P'/P =", -p1(0.04) / float(price(0.04)), " P''/P =", p2(0.04) / float(price(0.04)))
print("P'(0.04) per face-percent sanity: face 100000 check price(0.05)=", float(price(0.05)))

# price-at-coupon-rate check (Prop 2.2): coupon rate 5%, yield 5%, face 100000
# exact second-order errors at the 3 shifts, for the ratio claims
from fractions import Fraction as Fr
y0 = 0.04
def e1(dy):
    return price(y0 + dy) - ns["taylor_first"](y0, dy)
def e2(dy):
    return price(y0 + dy) - ns["taylor_second"](y0, dy)
for dy in (0.01, 0.005, 0.0025, -0.01):
    print(f"dy={dy:+.4f}: first-order error {float(e1(dy)):+.6e}  second-order error {float(e2(dy)):+.6e}")
print("ratio first 0.01/0.005 =", float(e1(0.01) / e1(0.005)), " second =", float(e2(0.01) / e2(0.005)))
print("ratio first 0.005/0.0025 =", float(e1(0.005) / e1(0.0025)), " second =", float(e2(0.005) / e2(0.0025)))
print("unrounded second-order error at +0.01 =", float(e2(0.01)), " at -0.01 =", float(e2(-0.01)))
print("unrounded price at -0.01 =", float(price(0.03)), " second-order at -0.01 =", float(ns['taylor_second'](y0, -0.01)))

# quiz explanation: two cash flows c1=-1, c2=1000 at y=0.04, P'(y) = -sum t c_t (1+y)^(-t-1)
y = 0.04
pp = -sum(t * c * (1 + y) ** (-t - 1) for t, c in ((1, -1), (2, 1000)))
print("two-cash-flow P'(0.04) =", pp)

# zero coupon quiz: P(y)=100(1+y)^-2, P'(0)=-200
print("zero-coupon P'(0) =", -2 * 100 * (1 + 0) ** -3)

# M1 two-year bond at yield .05: 50/1.05 + 1050/1.05^2
print("M1 price =", 50 / 1.05 + 1050 / 1.05**2)
# M3 P'(0.04) = -200/1.04^3
print("M3 P'(0.04) =", -200 / 1.04**3)
# price and remainder sign check at several dy using exact
print("R2 at dy=0.5: P(0.54) =", float(price(0.54)), " P2(0.5)=", float(ns['taylor_second'](y0, 0.5)))
