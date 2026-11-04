"""Counterexample search for the CONDITIONING of Proposition 3.1 (PC3-b round 6).
Proposition 3.1 concludes E[c_t + sigma_t v_t | v_t = v] = (1-p)h - p[(v-a)^+ + (b-v)^+] under H1 (I_{t-1} = 0) and
H2 (a = a_t, b = b_t). The displayed conditioning is on v_t alone. Under A3 the quote may be any function of the
public fill history. Rule B (admissible under A3, same A1, A4, A5, A6 with h = 10): mid = 10000 + 10 * (number of
fills so far), quote a = mid + 10, b = mid - 10, size 1. Here the quote at I = 0 is NOT fixed. Exact enumeration.
"""
from fractions import Fraction as F
from collections import defaultdict

def run(T, rule):
    states = [(F(1), 10000, 0, 0, 0)]  # prob, v_prev, inv, nfills, last_mid-free
    rec = defaultdict(F)
    tsum = defaultdict(F)
    for t in range(1, T + 1):
        new = []
        for prob, vprev, inv, nf, _ in states:
            for mv in (5, -5):
                v = vprev + mv
                mid = rule(nf)
                a, b = mid + 10, mid - 10
                for arr, pa in (("ub", F(1, 4)), ("us", F(1, 4)), ("inf", F(1, 2))):
                    pr = prob * F(1, 2) * pa
                    if arr == "ub":
                        side = -1
                    elif arr == "us":
                        side = 1
                    else:
                        side = -1 if v > a else (1 if v < b else 0)
                    filled = side != 0 and abs(inv + side) <= 10
                    term = F(0)
                    if filled:
                        price = a if side < 0 else b
                        term = -side * price + side * v
                    if t == T:
                        key = (v, (a, b), inv)
                        rec[key] += pr
                        tsum[key] += pr * term
                    new.append((pr, v, inv + (side if filled else 0), nf + (1 if filled else 0), 0))
        states = new
    return rec, tsum

def formula(v, a, b, p=F(1, 2)):
    return (1 - p) * F(a - b, 2) - p * (max(v - a, 0) + max(b - v, 0))

rule_b = lambda nf: 10000 + 10 * nf
rec, ts = run(5, rule_b)
found = []
for v in sorted({k[0] for k in rec}):
    keys = [k for k in rec if k[0] == v and k[2] == 0]
    mass = sum(rec[k] for k in keys)
    if mass == 0:
        continue
    mix = sum(ts[k] for k in keys) / mass
    quotes = sorted({k[1] for k in keys})
    per_quote = {q: (sum(ts[k] for k in keys if k[1] == q) / sum(rec[k] for k in keys if k[1] == q)) for q in quotes}
    ok_each = all(per_quote[q] == formula(v, *q) for q in quotes)
    if mix != formula(v, *quotes[0]) and len(quotes) > 1:
        found.append((v, str(mix), float(mix), [(q, str(per_quote[q]), str(formula(v, *q))) for q in quotes], ok_each))
print("rule B, T=5, conditioning on v_5 = v and I_4 = 0 (quote NOT fixed):")
print("values of v with a quote mixture:", len(found))
for row in found[:6]:
    print(" v=%d  E_mixture=%s (%.4f)  per-quote (quote, E, formula): %s  each quote matches formula: %s" % (row[0], row[1], row[2], row[3], row[4]))
