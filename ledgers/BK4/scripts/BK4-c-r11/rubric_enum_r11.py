"""Round-11 rubric exclusivity and exhaustiveness check for BK4 project.html (criteria C1-C5), current wording.

Written by the round-11 verifier from the descriptor text now on project.html (rubric table, #rubric). Each criterion is
encoded as the observable features of a memo; each level is the predicate its wording states. The script enumerates every
valid feature combination and prints the combinations matched by no level (gaps) and by more than one level (overlaps).
Validity: a feature that presupposes a sizing rule, a sharing rule, a recommended margin or a limit needs that base
feature (for example, checking the cover at the chosen margin presupposes a stated margin or sizing rule).
Usage: python -I rubric_enum_r11.py   (stdlib only; exit 1 if any criterion has a gap or an overlap)
"""

import sys
from itertools import product

B = (False, True)
bad = 0


def run(name, feats, levels, valid):
    global bad
    gaps, overlaps = [], []
    for env in valid:
        hits = [lvl for lvl, pred in levels.items() if pred(env)]
        if not hits:
            gaps.append(env)
        elif len(hits) > 1:
            overlaps.append((env, hits))
    bad += len(gaps) + len(overlaps)
    print(f"== {name}: {len(valid)} valid feature combinations; gaps {len(gaps)}; overlaps {len(overlaps)}")
    for env in gaps[:5]:
        print("   GAP:", {k: v for k, v in env.items() if v})
    for env, hits in overlaps[:5]:
        print("   OVERLAP:", {k: v for k, v in env.items() if v}, hits)


def combos(feats):
    return [dict(zip(feats, c)) for c in product(*[B] * len(feats))]


# C1 (unchanged this round). ge2: names two or more layers; ge1: names one or more; all4: names all four.
f1 = ["ge1", "ge2", "all4", "in_order", "cents", "waits"]
l1 = {
    4: lambda e: e["all4"] and e["in_order"] and e["cents"] and e["waits"],
    3: lambda e: e["all4"] and e["in_order"] and e["cents"] and not e["waits"],
    2: lambda e: (e["ge2"] and not e["all4"]) or (e["all4"] and (not e["cents"] or not e["in_order"])),
    1: lambda e: not e["ge2"],
}
v1 = [e for e in combos(f1) if (not e["ge2"] or e["ge1"]) and (not e["all4"] or e["ge2"])]
run("C1 waterfall order and layer amounts", f1, l1, v1)

# C2 (changed). T target stated; Tb target in bps; K value of k; P sorted position; S margin value or sizing rule
# stated; C1c cover checked at the chosen margin; C2c cover checked one cent below. Checking, k, position and bps all
# presuppose a stated margin or sizing rule (S) and, for bps, a stated target (T).
f2 = ["T", "Tb", "K", "P", "S", "C1c", "C2c"]
l2 = {
    4: lambda e: e["Tb"] and e["K"] and e["P"] and e["C1c"] and e["C2c"],
    3: lambda e: e["T"] and e["K"] and e["S"] and e["C1c"] and not (e["P"] and e["C2c"] and e["Tb"]),
    2: lambda e: e["S"] and e["T"] and (not e["C1c"] or not e["K"]),
    1: lambda e: not (e["S"] and e["T"]),
}
v2 = [e for e in combos(f2)
      if (not e["Tb"] or e["T"])
      and all(not e[x] or e["S"] for x in ("K", "P", "C1c", "C2c"))]
run("C2 margin sizing", f2, l2, v2)

# C3 (changed). P pro rata named; Lf leftover named; O another sharing rule named; A survivor amounts given;
# Sum a sum check for a stated scenario (needs amounts).
f3 = ["P", "Lf", "O", "A", "Sum"]
l3 = {
    4: lambda e: e["P"] and e["Lf"] and e["Sum"],
    3: lambda e: e["P"] and e["Lf"] and not e["Sum"],
    2: (lambda e: (e["A"] and not (e["P"] or e["Lf"] or e["O"]))
        or (e["P"] != e["Lf"])
        or (e["O"] and not (e["P"] and e["Lf"]))),
    1: lambda e: not (e["P"] or e["Lf"] or e["O"] or e["A"]),
}
v3 = [e for e in combos(f3) if not e["Sum"] or e["A"]]
run("C3 survivor sharing and rounding", f3, l3, v3)

# C4 (changed). R0 no margin recommended; R1 exactly one; R2 two or more (a fallback counts); c cover stated for the
# recommended margin; a one alternative compared; n count of scenarios past the survivors or uncovered.
f4 = ["R0", "R1", "R2", "c", "a", "n"]
l4 = {
    4: lambda e: e["R1"] and e["c"] and e["a"] and e["n"],
    3: lambda e: e["R1"] and e["c"] and e["a"] and not e["n"],
    2: lambda e: (e["R1"] and not (e["c"] and e["a"])) or e["R2"],
    1: lambda e: e["R0"],
}
v4 = [e for e in combos(f4) if sum([e["R0"], e["R1"], e["R2"]]) == 1 and (e["R1"] or not (e["c"] or e["a"] or e["n"]))]
run("C4 interpretation and recommendation", f4, l4, v4)

# C5 (changed). N1/N2/N3/N4: at least one / two / three / all four limits named; D direction stated for each named
# limit (a 'not known' direction counts); E counter-evidence statement for each B/C claim, or a statement that the memo
# cites none.
f5 = ["N1", "N2", "N3", "N4", "D", "E"]
l5 = {
    4: lambda e: e["N4"] and e["D"] and e["E"],
    3: lambda e: (e["N3"] and not e["N4"] and e["D"]) or (e["N4"] and e["D"] and not e["E"]),
    2: lambda e: (e["N1"] and not e["N3"]) or (e["N3"] and not e["D"]) or (e["N4"] and not e["D"]),
    1: lambda e: not e["N1"],
}
v5 = [e for e in combos(f5) if (not e["N2"] or e["N1"]) and (not e["N3"] or e["N2"]) and (not e["N4"] or e["N3"])
      and (not e["D"] or e["N1"]) and (not e["E"] or e["N1"])]
run("C5 limits and evidence", f5, l5, v5)

print("RUBRIC ENUMERATION", "FAIL" if bad else "PASS", "defects", bad)
sys.exit(1 if bad else 0)
