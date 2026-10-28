"""Counterexamples for E2-c round 1: (1) Lemma 3.1 without the hypothesis Delta > 0;
(2) L09 Proposition 3.2 with all values zero (efficiency denominator is 0)."""
from fractions import Fraction as Fr


def ic_ir(values, mech):
    """values: dict type->value; mech: dict report->(q, tau). Returns (IC, IR) by full enumeration."""
    ic = ir = True
    for th, v in values.items():
        truthful = v * mech[th][0] - mech[th][1]
        if truthful < 0:
            ir = False
        for r in values:
            if v * mech[r][0] - mech[r][1] > truthful:
                ic = False
    return ic, ir


# (1) equal values, Delta = 0: IC and IR hold, yet q_L = 1 > q_H = 0, so the 'only if' direction of Lemma 3.1 fails.
vals = {"L": 5000, "H": 5000}
mech = {"L": (Fr(1), Fr(5000)), "H": (Fr(0), Fr(0))}
print("lemma counterexample (v_L = v_H = 5000, q_L=1 tau_L=5000, q_H=0 tau_H=0): IC, IR =", ic_ir(vals, mech),
      "; q_L <= q_H holds:", mech["L"][0] <= mech["H"][0])

# (2) L09 efficiency: all values 0, truthful bids, k = 2
values = [0, 0, 0, 0]
k = 2
best = sum(sorted(values, reverse=True)[:k])
print("L09 zero-value profile: sum of k highest values =", best, "-> efficiency = won/best is 0/0 (undefined)")
