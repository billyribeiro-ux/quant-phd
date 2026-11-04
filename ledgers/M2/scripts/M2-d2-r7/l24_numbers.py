"""Re-derive every L24 number that the page states in prose (signed errors, exact errors, unrounded values, ulp)."""
import math
from decimal import Decimal, getcontext

getcontext().prec = 60
E = Decimal("2.71828182845904523536028747135266249775724709369995957496696763")

def smooth(x):
    return math.exp(x)

def forward(f, x, h):
    return (f(x + h) - f(x)) / h

def central(f, x, h):
    return (f(x + h) - f(x - h)) / (2.0 * h)

print("== signed computed errors (float quotient minus float e) and printed absolute errors")
for k in (4, 5, 6, 7, 8, 9):
    h = 10.0 ** -k
    fw = forward(smooth, 1.0, h) - math.e
    ce = central(smooth, 1.0, h) - math.e
    print(f"k={k} h={h:.0e} forward signed {fw:+.10e} abs {abs(fw):.3e} | central signed {ce:+.10e} abs {abs(ce):.3e}")

print("== exact (decimal) forward and central errors of e^x at 1, with h=10^-k")
for k in (4, 5, 6, 7, 8, 9):
    h = Decimal(10) ** (-k)
    ex = E.exp() if False else None
    e1 = E  # e^1
    # e^(1+h) = e * e^h ; use Decimal exp directly
    fwd_q = (Decimal(1 + h).exp() - E) / h if False else ((E * h.exp()) - E) / h
    cen_q = (E * h.exp() - E * (-h).exp()) / (2 * h)
    print(f"k={k}: exact forward quotient error {float(fwd_q - E):+.6e} ; exact central quotient error {float(cen_q - E):+.6e}; e*h/2={float(E*h/2):.6e}; e*(sinh h/h -1)={float(E*((h.exp()-(-h).exp())/(2*h) - 1)):.6e}")

print("== exact forward error at h=1e-8 vs the float forward quotient (the page's 1.359e-8 and -6.603e-9)")
h = Decimal("1e-8")
exact_fwd = ((E * h.exp()) - E) / h
print("exact forward quotient minus e at 1e-8:", float(exact_fwd - E))
print("float forward quotient minus float e at 1e-8:", forward(smooth, 1.0, 1e-8) - math.e)
print("float forward quotient at 1e-8 minus exact quotient:", float(Decimal(forward(smooth, 1.0, 1e-8)) - exact_fwd))

print("== page E3: unrounded central errors at 1e-5 and 1e-7 (float, full precision)")
for k in (5, 7):
    h = 10.0 ** -k
    c = central(smooth, 1.0, h)
    print(f"k={k}: central quotient {c!r}; minus math.e = {c - math.e:.17e}")
c5 = central(smooth, 1.0, 1e-5) - math.e
c7 = central(smooth, 1.0, 1e-7) - math.e
print("difference c7 - c5 =", f"{c7 - c5:.6e}", " ulp(e) =", math.ulp(math.e), " 2^-51 =", 2.0**-51)

print("== grid spacing of central quotient: ulp(e)/(2h)")
for k in (5, 7):
    h = 10.0 ** -k
    print(f"k={k}: ulp(e)/(2h) = {math.ulp(math.e)/(2*h):.3e}; 2.2e-16/h = {2.2e-16/h:.3e}")

print("== L24 Interpretation: 0.5*e*h at 1e-5 and 1e-9; 2*delta/h at 1e-15 with delta=2.22e-16")
print("e*1e-5/2 =", math.e * 1e-5 / 2, " e*1e-9/2 =", math.e * 1e-9 / 2)
print("2*2.22e-16/1e-15 =", 2 * 2.22e-16 / 1e-15)
print("predicted minimizers: 2*sqrt(delta/e) =", 2 * math.sqrt(2.22e-16 / math.e), " (3 delta/e)^(1/3) =", (3 * 2.22e-16 / math.e) ** (1 / 3))
print("2*delta/h* ... forward minimum value 2 sqrt(M delta)=", 2 * math.sqrt(math.e * 2.22e-16))
print("truncation 0.5*e*h at h*:", 0.5 * math.e * 2 * math.sqrt(2.22e-16 / math.e))
print("== Remark 4.4 numbers: 1/2 e h at 1e-8 =", 0.5 * math.e * 1e-8)
