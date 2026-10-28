"""Random check of Proposition 2.2 (tau_D >= tau_S for conventional flows, r >= 0, both paybacks exist) and of R2 (tau_D <= N iff NPV(r) >= 0)."""
import random

def cums(flows, r):
    out, total = [], 0.0
    for t, f in enumerate(flows):
        total += f / (1 + r) ** t
        out.append(total)
    return out

def first(xs):
    for t in range(1, len(xs)):
        if xs[t] >= 0:
            return t
    return None

rng = random.Random(8)
checked = viol22 = both = r2_checked = r2_viol = 0
for _ in range(200000):
    N = rng.randint(1, 8)
    flows = [-rng.uniform(1, 1000)] + [rng.choice([0.0, rng.uniform(0, 800)]) for _ in range(N)]
    r = rng.uniform(0, 1.5)
    cum = cums(flows, 0.0)
    disc = cums(flows, r)
    ts, td = first(cum), first(disc)
    checked += 1
    if ts is not None and td is not None:
        both += 1
        if not td >= ts:
            viol22 += 1
    if td is not None or True:
        r2_checked += 1
        reached = td is not None and td <= N
        if reached != (disc[N] >= 0):
            r2_viol += 1
print("cases", checked, "both_paybacks", both, "prop2.2_violations", viol22, "R2_checked", r2_checked, "R2_violations", r2_viol)
