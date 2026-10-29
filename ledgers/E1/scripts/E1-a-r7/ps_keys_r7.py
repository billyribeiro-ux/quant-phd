"""Round 7: check the corrected hub skill-check keys against the project model at several (a, b, c)."""
from fractions import Fraction as Fr

def monopoly_profit(Q, a, b, c):
    return ((a - Q) / b - c) * Q

def cournot_profit(q1, q2, a, b, c):
    return ((a - q1 - q2) / b - c) * q1

fails = 0
for a, b, c in [(Fr(120), Fr(1), Fr(20)), (Fr(120), Fr(2), Fr(20)), (Fr(90), Fr(3), Fr(5)), (Fr(7), Fr(1, 2), Fr(2))]:
    # Ps1 key a - bc - 2Q = 0 -> Q = (a - bc)/2; check derivative numerically by finite difference-free algebra
    Qs = (a - b * c) / 2
    h = Fr(1, 10**6)
    deriv = (monopoly_profit(Qs + h, a, b, c) - monopoly_profit(Qs - h, a, b, c)) / (2 * h)
    ok1 = abs(deriv) < Fr(1, 10**4)
    # distractors: a - bc - Q = 0 -> Q = a - bc ; a - 2bQ - c = 0 -> Q=(a-c)/(2b)
    wrong_ok = [abs(((a - b*c) - Qd) ) for Qd in [(a - b*c)]]
    # Ps2 key q1 = (a - bc - q2)/2 is the zero of the q1-derivative at q2 = 1
    q2 = Fr(1)
    r1 = (a - b * c - q2) / 2
    d2 = (cournot_profit(r1 + h, q2, a, b, c) - cournot_profit(r1 - h, q2, a, b, c)) / (2 * h)
    ok2 = abs(d2) < Fr(1, 10**4)
    # the page's own monopoly volume d/2 and profit d^2/(4b)
    d = a - b * c
    ok3 = monopoly_profit(d / 2, a, b, c) == d * d / (4 * b)
    print(f"a={a} b={b} c={c}: Ps1 root {Qs} derivative~0 {ok1}; Ps2 root {r1} derivative~0 {ok2}; monopoly profit d^2/(4b) {ok3}")
    fails += not (ok1 and ok2 and ok3)
print("FAILS:", fails)
