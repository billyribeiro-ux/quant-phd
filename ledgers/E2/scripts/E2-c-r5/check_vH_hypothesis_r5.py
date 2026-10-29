"""Counterexample check for Proposition 3.2 without the hypothesis v_H > 0 (round 5). Exact fractions, brute force over a menu grid."""
from fractions import Fraction as F
import itertools

def best(vL, vH, pH):
    pL = 1 - pH
    V = {"L": vL, "H": vH}
    P = {"L": pL, "H": pH}
    qs = [F(0), F(1, 2), F(1)]
    taus = [F(k, 2) for k in range(-12, 13)]
    top = None
    for qL, qH, tL, tH in itertools.product(qs, qs, taus, taus):
        m = {"L": (qL, tL), "H": (qH, tH)}
        u = lambda t, r: V[t] * m[r][0] - m[r][1]
        ic = all(u(t, t) >= u(t, r) for t in V for r in V)
        ir = all(u(t, t) >= 0 for t in V)
        if ic and ir:
            rev = P["L"] * tL + P["H"] * tH
            if top is None or rev > top[0]:
                top = (rev, qL, qH, tL, tH)
    return top

vL, vH, pH = F(-2), F(-1), F(1, 2)
c = (1 - pH) * vL - pH * (vH - vL)
print("c =", c, "claimed max p_H v_H =", pH * vH)
print("brute-force optimum (revenue, qL, qH, tauL, tauH) =", best(vL, vH, pH))
