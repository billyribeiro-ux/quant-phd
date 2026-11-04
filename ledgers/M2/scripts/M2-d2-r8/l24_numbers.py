"""Re-derive every L24 number: exact truncation errors, computed errors (float, the lab's formulas), decade grid,
the E2/E3 unrounded values, the predicted minimizers, and the bound functions. Independent of the twin code paths
except for the same float formulas (checked against the twin output in twin_vs_page.out)."""
import math
from decimal import Decimal, getcontext
getcontext().prec = 50

e = math.e
def fwd(f, x, h): return (f(x + h) - f(x)) / h
def cen(f, x, h): return (f(x + h) - f(x - h)) / (2.0 * h)
ex = math.exp

print("== Remark 4.4: h = 1e-8, exp at 1")
h = 1e-8
print("exact forward error (e*(e^h-1)/h - e) via Decimal:")
getcontext().prec = 60
D = Decimal
hD = D("1e-8")
eD = D(1).exp()
exact_fwd = eD * ((hD).exp() - 1) / hD - eD
print("  ", float(exact_fwd))
computed_fwd = fwd(ex, 1.0, h) - e
print("computed forward error (float, lab formula):", computed_fwd)
print("  ratio computed/exact:", computed_fwd / float(exact_fwd))

print("== Part B grid: forward and central errors (float, vs math.e), k=1..15")
for k in range(1, 16):
    hk = 10.0 ** -k
    fe = fwd(ex, 1.0, hk) - e
    ce = cen(ex, 1.0, hk) - e
    print(f"k={k:2d} h={hk:.0e} fwd_signed={fe:+.4e} |fwd|={abs(fe):.3e} cen_signed={ce:+.4e} |cen|={abs(ce):.3e}")

print("== E3 unrounded central quotient errors at 1e-5 and 1e-7 (difference of unrounded values)")
c5 = cen(ex, 1.0, 1e-5); c7 = cen(ex, 1.0, 1e-7)
e5 = abs(c5 - e); e7 = abs(c7 - e)
print("  unrounded errors:", f"{e5:.6e}", f"{e7:.6e}", "difference (float):", e5 - e7, "ulp(e)=", math.ulp(e))
print("  exact-real central error e(sinh h/h - 1) at 1e-5 via Decimal:")
hD = D("1e-5")
for hs in ("1e-5", "1e-6", "1e-7"):
    hD = D(hs)
    val = eD * (hD.exp() - (-hD).exp()) / (2 * hD) - eD
    print("   ", hs, float(val))
print("  unrounded float central error via printed formula: e(h^2/6) =", [e*float(hs)**2/6 for hs in ("1e-5","1e-6","1e-7")])

print("== Predicted minimizers")
delta = 2.220446049250313e-16
print("forward h* = 2 sqrt(delta/e) =", 2*math.sqrt(delta/e))
print("central h* = (3 delta/e)^(1/3) =", (3*delta/e)**(1/3))
print("central h* (delta=2^-52 as in L13 model?) =", (3*2**-52/e)**(1/3))
print("forward h* with delta=2^-52:", 2*math.sqrt(2**-52/e))
print("log10 distances of 6.3e-6 to 1e-5 and 1e-6:", math.log10(6.3e-6)-(-5), abs(math.log10(6.3e-6)-(-6)))

print("== Proposition 4.2 bound at h* for f = exp at 1 (M2 = e), delta = 2.22e-16")
M2 = e
hstar = 2*math.sqrt(delta/M2)
print("h*", hstar, "bound 2 sqrt(M2 delta) =", 2*math.sqrt(M2*delta))
print("E2 round-off bound 2 delta/h at h=1e-15:", 2*delta/1e-15)
print("E2 printed error at 1e-15 (fwd):", abs(fwd(ex,1.0,1e-15)-e), "central:", abs(cen(ex,1.0,1e-15)-e))
print("half ulp of e:", math.ulp(e)/2, " ulp(e)=", math.ulp(e), " delta used =", delta)

print("== extra checks added in round 8")
for hs in ("1e-9",):
    hD = D(hs)
    print("exact forward error at", hs, "=", float(eD * ((hD).exp() - 1) / hD - eD), " (page: 1.36e-9)")
hD = D("1e-4")
print("exact central error at 1e-4 =", float(eD * (hD.exp() - (-hD).exp()) / (2 * hD) - eD), " (page: 4.530e-9)")
print("printed-digit ratio 4.531e-9 / 5.859e-11 =", 4.531e-9 / 5.859e-11)
print("L24 M3 quotient: (2.1**3 - 2**3)/0.1 =", (2.1**3 - 2**3) / 0.1, " error =", (2.1**3 - 2**3) / 0.1 - 12, " M2 = sup|6x| on [2,2.1] =", 6 * 2.1, " bound =", 0.5 * 12.6 * 0.1)
print("1e-5 truncation (1/2) e h =", 0.5 * e * 1e-5, " (page: 1.359e-5)")
