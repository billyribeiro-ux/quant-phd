"""Round-10 rubric exclusivity and exhaustiveness check for BK4 project.html (rows C1-C5).

Each criterion is encoded as the features a memo can have, and each level descriptor as the predicate that its
wording (course/modules/BK/BK4/project.html, rubric table, lines 412-416) states. The script enumerates every
feature combination and prints the combinations matched by no level (gaps) and by more than one level (overlaps).
Usage: python rubric_enum_r10.py   (stdlib only)
"""

from itertools import product

B = (False, True)


def report(name, feats, levels, realistic):
    gaps, overlaps = [], []
    for combo in product(*[B] * len(feats)):
        env = dict(zip(feats, combo))
        hits = [lvl for lvl, pred in levels.items() if pred(env)]
        if not hits:
            gaps.append(env)
        elif len(hits) > 1:
            overlaps.append((env, hits))
    print(f"== {name}: {len(list(product(*[B] * len(feats))))} feature combinations; gaps {len(gaps)}; overlaps {len(overlaps)}")
    for env in gaps:
        print("   GAP:", {k: v for k, v in env.items() if v}, "matches no level")
    for env, hits in overlaps[:5]:
        print("   OVERLAP:", {k: v for k, v in env.items() if v}, "matches", hits)
    return gaps, overlaps


# C1: names each layer in order; gives its cents for a stated scenario; states the waits rule. Memo level feature:
# n_layers is 0..4 as three booleans (ge1, ge2, all4); ordering and cents and waits apply to the all-four case.
c1_feats = ["ge2", "ge1", "all4", "in_order", "cents_for_scenario", "waits"]


def c1_valid(e):
    return (not e["ge2"] or e["ge1"]) and (not e["all4"] or e["ge2"])


c1_levels = {
    4: lambda e: e["all4"] and e["in_order"] and e["cents_for_scenario"] and e["waits"],
    3: lambda e: e["all4"] and e["in_order"] and e["cents_for_scenario"] and not e["waits"],
    2: lambda e: (e["ge2"] and not e["all4"]) or (e["all4"] and (not e["cents_for_scenario"] or not e["in_order"])),
    1: lambda e: not e["ge2"],
}
c1_feats_valid = [dict(zip(c1_feats, c)) for c in product(*[B] * len(c1_feats))]
c1_feats_valid = [e for e in c1_feats_valid if c1_valid(e)]


def run_valid(name, feats, levels, valid):
    gaps, overlaps = [], []
    for env in valid:
        hits = [lvl for lvl, pred in levels.items() if pred(env)]
        if not hits:
            gaps.append(env)
        elif len(hits) > 1:
            overlaps.append((env, hits))
    print(f"== {name}: {len(valid)} valid feature combinations; gaps {len(gaps)}; overlaps {len(overlaps)}")
    for env in gaps:
        print("   GAP:", {k: v for k, v in env.items() if v})
    for env, hits in overlaps[:5]:
        print("   OVERLAP:", {k: v for k, v in env.items() if v}, hits)
    return gaps, overlaps


results = {}
results["C1"] = run_valid("C1 waterfall order", c1_feats, c1_levels, c1_feats_valid)

# C2: T = target stated; Tb = target in basis points; K = value of k; P = sorted position; M = numeric margin;
# C1c = cover checked at chosen margin; C2c = cover checked one cent below; S = sizing rule or margin value stated
# (R = S and T, the descriptor's "margin value or sizing rule for a stated target").
c2_feats = ["T", "Tb", "K", "P", "M", "C1c", "C2c", "S"]
c2_levels = {
    4: lambda e: e["Tb"] and e["K"] and e["P"] and e["C1c"] and e["C2c"],
    3: lambda e: e["T"] and e["K"] and e["M"] and e["C1c"] and not (e["Tb"] and e["P"] and e["C2c"]),
    2: lambda e: e["S"] and e["T"] and (not e["C1c"] or not e["K"]),
    1: lambda e: not (e["S"] and e["T"]),
}
c2_valid = [dict(zip(c2_feats, c)) for c in product(*[B] * len(c2_feats))]
c2_valid = [e for e in c2_valid if all(not e[x] or e["S"] for x in ("M", "K", "P", "C1c", "C2c"))
            and (not e["Tb"] or e["T"])]  # a k, a position, a margin or a cover check each presuppose a sizing rule
results["C2"] = run_valid("C2 margin sizing", c2_feats, c2_levels, c2_valid)

# C3: P = pro rata named; Lf = leftover named; O = another sharing rule named; A = survivor amounts given;
# Sum = a sum check for a stated scenario.
c3_feats = ["P", "Lf", "O", "A", "Sum"]
c3_levels = {
    4: lambda e: e["P"] and e["Lf"] and e["Sum"],
    3: lambda e: e["P"] and e["Lf"] and not e["Sum"],
    2: lambda e: (e["A"] and not (e["P"] or e["Lf"] or e["O"])) or (e["P"] != e["Lf"]),
    1: lambda e: not (e["P"] or e["Lf"] or e["O"]) and not e["A"],
}
c3_valid = [dict(zip(c3_feats, c)) for c in product(*[B] * len(c3_feats))]
c3_valid = [e for e in c3_valid if not e["Sum"] or e["A"]]
results["C3"] = run_valid("C3 survivor sharing", c3_feats, c3_levels, c3_valid)

# C4: nrec = number of margins recommended (0, 1, 2+); c = cover stated for it; a = one alternative compared;
# n = count of scenarios past survivors or uncovered.
c4_feats = ["nrec0", "nrec1", "nrec2", "c", "a", "n"]
c4_levels = {
    4: lambda e: e["nrec1"] and e["c"] and e["a"] and e["n"],
    3: lambda e: e["nrec1"] and e["c"] and e["a"] and not e["n"],
    2: lambda e: e["nrec1"] and (not e["c"] or not e["a"]),
    1: lambda e: e["nrec0"],
}
c4_valid = [dict(zip(c4_feats, c)) for c in product(*[B] * len(c4_feats))]
c4_valid = [e for e in c4_valid if sum([e["nrec0"], e["nrec1"], e["nrec2"]]) == 1 and (e["nrec1"] or not (e["c"] or e["a"] or e["n"]))]
results["C4"] = run_valid("C4 interpretation", c4_feats, c4_levels, c4_valid)

# C5: N = number of the four listed limits named (0..4 as N0..N4 booleans: N1 means at least one, etc.);
# D = a direction stated for each named limit; E = counter-evidence statement (or none-cited statement).
c5_feats = ["N1", "N2", "N3", "N4", "D", "E"]


def c5_valid(e):
    return (not e["N2"] or e["N1"]) and (not e["N3"] or e["N2"]) and (not e["N4"] or e["N3"])


c5_levels = {
    4: lambda e: e["N4"] and e["D"] and e["E"],
    3: lambda e: (e["N3"] and not e["N4"] and e["D"]) or (e["N4"] and e["D"] and not e["E"]),
    2: lambda e: (e["N1"] and not e["N3"]) or (e["N3"] and not e["D"]) or (e["N4"] and not e["D"]),
    1: lambda e: not e["N1"],
}
c5_valid_list = [dict(zip(c5_feats, c)) for c in product(*[B] * len(c5_feats))]
c5_valid_list = [e for e in c5_valid_list if c5_valid(e)]
results["C5"] = run_valid("C5 limits", c5_feats, c5_levels, c5_valid_list)

total = sum(len(g) for g, _ in results.values())
print("TOTAL GAPS", total)
