"""Numerical checks of Propositions 3 to 5 on a grid, with the verifier's independent quadrature (indep_model.py).

Usage: python -I ledgers/E4/scripts/E4-d-r2/props_grid.py <repo-root>
Checks: (a) sign of G equals sign(tau_bar - tau_y(lam)) at sampled lam; (b) Proposition 4 closed form equals the
quadrature root (bisection with the page's boundary rule); (c) lam* is strictly decreasing in cost on the interior and
d lam*/d sigma = lam*/sigma (finite difference); (d) informativeness independent of sigma on the interior.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "ledgers/E4/scripts/E4-d-r2"))
import indep_model as im  # noqa: E402

A, TV, TE = im.A, im.TV, im.TE

bad_sign = []
checked = 0
for sd in (0.3, 0.5, 0.75, 1.0, 2.0):
    for c in (0.0, 0.05, 0.12, 0.15, 0.3):
        tbar = (TV + TE) * math.exp(-2 * A * c) - TV
        for lam in (0.05, 0.2, 0.5, 0.8, 1.0):
            tyv = lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)
            g = im.gap_quadrature(lam, sd, c)
            checked += 1
            if abs(g) > 1e-12 and abs(tbar - tyv) > 1e-9 and (g > 0) != (tbar - tyv > 0):
                bad_sign.append((sd, c, lam))
print("(a) sign rule G vs tau_bar - tau_y checked at", checked, "points; violations:", bad_sign)

mism = []
for sd in (0.3, 0.5, 0.6, 0.75, 1.0, 1.5):
    for c in (0.0, 0.02, 0.05, 0.10, 0.13, 0.15, 0.2, 0.3):
        r = im.independent_root(sd, c)
        cf = im.proposition4(sd, c)
        if abs(r - cf) > 1e-9:
            mism.append((sd, c, r, cf))
print("(b) Proposition 4 closed form vs quadrature root: mismatches", mism)

mono_bad = []
for sd in (0.5, 0.6, 0.75):
    prev = None
    for c in [0.12 + 0.005 * k for k in range(7)]:
        lam = im.proposition4(sd, c)
        if prev is not None and 0 < lam < 1 and not lam < prev:
            mono_bad.append((sd, c))
        prev = lam
print("(c1) lam* strictly decreasing in c on the interior; violations:", mono_bad)

prop_bad = []
for c in (0.12, 0.135, 0.15):
    for sd in (0.5, 0.6, 0.75):
        h = 1e-6
        lam = im.proposition4(sd, c)
        dlam = (im.proposition4(sd + h, c) - im.proposition4(sd - h, c)) / (2 * h)
        if abs(dlam - lam / sd) > 1e-6:
            prop_bad.append((sd, c, dlam, lam / sd))
print("(c2) d lam*/d sigma = lam*/sigma on the interior; violations:", prop_bad)

inf_dep = []
for c in (0.12, 0.135, 0.15):
    vals = [im.informativeness(im.proposition4(sd, c), sd) for sd in (0.5, 0.625, 0.75)]
    inf_dep.append((c, [round(v, 12) for v in vals]))
print("(d) informativeness at the three noise volumes per cost:", inf_dep)

box_interior = 0
for i in range(22):
    for j in range(22):
        sd = 0.5 + 0.25 * i / 21.0
        c = 0.12 + 0.03 * j / 21.0
        if im.gap_quadrature(1e-9, sd, c) > 0 and im.gap_quadrature(1.0, sd, c) < 0:
            box_interior += 1
print("box 22x22 interior count (quadrature):", box_interior, "of", 22 * 22)
