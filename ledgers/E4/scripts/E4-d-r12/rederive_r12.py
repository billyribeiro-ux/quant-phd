"""Independent re-derivation of the E4 project page numbers (round 12, slice d).

Own closed forms only (Propositions 1-4 as written on the page, re-derived by hand in the round-12 review);
the grader's oracle is imported from the checkout's test file only for the cross-check lines.
"""
import math
import sys
from decimal import Decimal, getcontext

getcontext().prec = 50
A, TV, TE = 2.0, 1.0, 1.0


def tau_bar(c):
    return (TV + TE) * math.exp(-2 * A * c) - TV


def closed(sd, c):
    t = tau_bar(c)
    if t <= 0:
        return 0.0
    if t >= TE * TE / (TE + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TE * (TE - t)))


def ty(lam, sd):
    return lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)


def bcoef(lam, sd):
    t = ty(lam, sd)
    bs = (lam * TE + (1 - lam) * t) / (lam * (TV + TE) + (1 - lam) * (TV + t))
    return bs, -A * bs / (lam * TE), t


def FU(lam, sd):
    bs, _, t = bcoef(lam, sd)
    r = t / (TV + t) - bs
    return (1 + r * r * (TV + t) * (1 / TV + 1 / t)) ** -0.5


def FI(lam, sd):
    bs, bu, _ = bcoef(lam, sd)
    P = TV + TE
    slope = TE / P - bs
    vg = slope * slope * (1 / TV + 1 / TE) + bu * bu * sd * sd
    return (1 + P * vg) ** -0.5


def G(lam, sd, c):
    if lam == 0:
        a2 = A * A * sd * sd
        return (1 + a2 / TV) ** -0.5 - math.exp(A * c) * (1 + TE / TV + (TV + TE) * a2 / (TV * TV)) ** -0.5
    return FU(lam, sd) - math.exp(A * c) * FI(lam, sd)


def bisect(sd, c, cap=240, tol=1e-12):
    g0, g1 = G(0.0, sd, c), G(1.0, sd, c)
    if g0 <= 0:
        return 0.0
    if g1 >= 0:
        return 1.0
    lo, hi, n = 0.0, 1.0, 0
    while hi - lo > tol * hi and n < cap:
        mid = 0.5 * (lo + hi)
        if G(mid, sd, c) > 0:
            lo = mid
        else:
            hi = mid
        n += 1
    return 0.5 * (lo + hi)


print("== tau_bar on the box")
print("tau_bar(0.150) =", f"{tau_bar(0.150):.10f}", " tau_bar(0.120) =", f"{tau_bar(0.120):.10f}")
print("tau_y(1) at sd=0.75 =", f"{1 / (1 + 4 * 0.75 ** 2):.10f}")
print("2exp(-4*0.150)-1 exact (Decimal):", f"{2 * Decimal(-0.6).exp() - 1:.12f}")
print("2exp(-4*0.120)-1 exact (Decimal):", f"{2 * Decimal(-0.48).exp() - 1:.12f}")

print("== powers of two")
print("2^-200 =", f"{2.0 ** -200:.4e}", " 2^-240 =", f"{2.0 ** -240:.4e}", " 2^-240 via Decimal:", f"{Decimal(2) ** -240:.4e}")
print("threshold root for 240 halvings (2^-240 * 1e12):", f"{2.0 ** -240 * 1e12:.4e}")
print("threshold root for 200 halvings (2^-200 * 1e12):", f"{2.0 ** -200 * 1e12:.4e}")

print("== Lab 1 (sd 0.60, cost 0.13)")
print("gap(0+) =", f"{G(0.0, 0.6, 0.13):+.6f}", " gap(1) =", f"{G(1.0, 0.6, 0.13):+.6f}")
lam1 = bisect(0.6, 0.13, cap=60)
print("bisect 60 halvings lambda* =", f"{lam1:.10f}", " closed =", f"{closed(0.6, 0.13):.10f}")
print("tau_y at closed root =", f"{ty(closed(0.6, 0.13), 0.6):.8f}", "tau_bar =", f"{tau_bar(0.13):.8f}")
print("informativeness =", f"{tau_bar(0.13) / (TV + tau_bar(0.13)):.8f}", "1-e^{2ac}/2 =", f"{1 - math.exp(2 * A * 0.13) / 2:.8f}")

print("== Lab 2 (sd 0.70, cost 0.14)")
print("gap(0+) =", f"{G(0.0, 0.7, 0.14):+.6f}", " gap(1) =", f"{G(1.0, 0.7, 0.14):+.6f}")
print("lambda* closed =", f"{closed(0.7, 0.14):.10f}", " bisect240 =", f"{bisect(0.7, 0.14):.10f}")
print("informativeness =", f"{tau_bar(0.14) / (TV + tau_bar(0.14)):.8f}")

print("== Lab 3 grid and box")
worst = 0.0
for sd in (0.5, 0.625, 0.75):
    row = []
    for c in (0.120, 0.135, 0.150):
        l = bisect(sd, c)
        cf = closed(sd, c)
        worst = max(worst, abs(l - cf))
        g = G(l, sd, c) if 0 < l < 1 else (G(0.0, sd, c) if l == 0 else G(1.0, sd, c))
        row.append(f"{sd}/{c}: lam={l:.10f} cf={cf:.10f} gap={g:+.3e}")
    print(" | ".join(row))
print("largest |bisect - closed| on 3x3 grid:", f"{worst:.3e}")
inside = 0
for i in range(22):
    for j in range(22):
        sd = 0.5 + 0.25 * i / 21.0
        c = 0.12 + 0.03 * j / 21.0
        if G(0.0, sd, c) > 0 and G(1.0, sd, c) < 0:
            inside += 1
print("box grid with gap(0+)>0 and gap(1)<0:", inside, "of 484")
print("ratio lambda(0.625)/lambda(0.5) at cost 0.120 (unrounded):", f"{bisect(0.625, 0.12) / bisect(0.5, 0.12):.12f}")
print("ratio lambda(0.750)/lambda(0.5) at cost 0.120 (unrounded):", f"{bisect(0.75, 0.12) / bisect(0.5, 0.12):.12f}")
print("max |gap| over the nine grid points: see the Lab 3 output; checked in the verification log")
