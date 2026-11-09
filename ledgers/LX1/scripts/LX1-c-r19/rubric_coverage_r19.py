"""LX1-c round 19: exhaustive scoring model of the project rubric (course/modules/LX/LX1/project.html, #rubric).

Each criterion's level cells are encoded as predicates over essay features, transcribed from the page's cells
(table#rubric, lines 473-477; the scoring rule at line 467). The score of a criterion is the highest level whose
predicate holds; 0 if none holds. The script enumerates every feature combination and reports (a) the number of
combinations that score 0 and whether each is a 'no chain, no similarity' essay, (b) combinations where two
readings of an ambiguous clause give different scores, and (c) the ten student-error patterns of plan section 5.4.
Usage: python -I rubric_coverage_r19.py  (prints a table; no file access).
"""
from itertools import product


def c1(f, strict_missing):
    """Lenient reading: L2 holds when a date or a locator is missing for at least one of the two items.
    Strict reading: L2 holds when exactly one of the two items lacks a date or a locator."""
    e_missing = (not f["dates_e"]) or (not f["loc_e"])
    c_missing = (not f["dates_c"]) or (not f["loc_c"])
    locs = f["loc_e"] + f["loc_c"]
    if f["names_both"] and f["dates_e"] and f["dates_c"] and locs == 2:
        return 4
    if f["names_both"] and f["dates_e"] and f["dates_c"] and locs == 1:
        return 3
    l2 = (e_missing != c_missing) if strict_missing else (e_missing or c_missing)
    if f["names_both"] and l2:
        return 2
    if f["picks_two"]:
        return 1
    return 0


def c2(f, bubble_l2=True):
    chain3, chain_any = f["chain3"], f["chain_any"]
    rests, analogy, failure, evid = f["rests_all"], f["analogy"], f["failure"], f["failure_evidence"]
    bubble_ok = (not f["bubble"]) or f["benchmark"]
    if chain3 and rests and analogy and failure and evid and bubble_ok:
        return 4
    if chain3 and rests and analogy and failure and bubble_ok:
        return 3
    l2 = ((f["similarity"] and f["difference"])
          or (chain_any and not failure)
          or (chain_any and not chain3)
          or (chain3 and failure and not analogy)
          or (chain3 and analogy and failure and not rests)
          or (bubble_l2 and chain3 and rests and analogy and failure and f["bubble"] and not f["benchmark"]))
    if l2:
        return 2
    if f["similarity"] and not chain_any:
        return 1
    return 0


def c3(f):
    if f["all_cited_or_inference"] and f["no_locator_count"] == 0 and f["counter_or_none"]:
        return 4
    if f["all_cited_or_inference"] and f["no_locator_count"] <= 2 and f["counter_or_none"]:
        return 3
    if f["uncited_count"] <= 2:
        return 2
    if f["has_source"]:
        return 1
    return 0


def c4(f):
    if f["computed"] and f["unrounded_all"] and f["rule_all"] and f["formula_all"] and f["base_sign_all"]:
        return 4
    if (f["computed"] and f["rule_all_but_one_nonrounded"] and f["formula_all"] and f["base_sign_all"]):
        return 3
    if f["rounds_input"] or (f["rule_some"] and not f["rule_all"]) or (
            f["computed"] and f["unrounded_all"] and f["rule_all"] and not (f["formula_all"] and f["base_sign_all"])):
        return 2
    return 1 if (not f["computed"] or not f["rule_some"]) else 0


def c5(f):
    if f["limits"] >= 2 and f["tested"] == f["limits"]:
        return 4
    if f["limits"] >= 2 and f["tested"] >= 1:
        return 3
    if f["limits"] >= 1:
        return 2
    return 1 if f["caveat"] else 0


C2_KEYS = ["chain3", "chain_any", "rests_all", "analogy", "failure", "failure_evidence", "bubble", "benchmark",
           "similarity", "difference"]
zero_c2 = []
for vals in product([False, True], repeat=len(C2_KEYS)):
    f = dict(zip(C2_KEYS, vals))
    if f["chain3"] and not f["chain_any"]:
        continue
    if f["rests_all"] and not f["chain3"]:
        continue
    if f["failure_evidence"] and not f["failure"]:
        continue
    if f["benchmark"] and not f["bubble"]:
        continue
    if c2(f) == 0:
        zero_c2.append(f)
print("C2 feature combinations (consistent) scoring 0:", len(zero_c2))
print("   of which have a chain or a similarity (must be 0):", sum(1 for f in zero_c2 if f["chain_any"] or f["similarity"]))
for f in zero_c2[:6]:
    print("   ", {k: v for k, v in f.items() if v})
both_missing_c1 = [(a, b, c, d) for a, b, c, d in product([False, True], repeat=4)]
for strict in (False, True):
    res = {}
    for dte, dtc, le, lc in product([False, True], repeat=4):
        f = {"names_both": True, "dates_e": dte, "dates_c": dtc, "loc_e": le, "loc_c": lc, "picks_two": True}
        res[(dte, dtc, le, lc)] = c1(f, strict)
    key = (True, True, False, False)
    print(f"C1 reading strict={strict}: dated both, no locators -> {res[key]}; dated episode only, both locators -> "
          f"{res[(True, False, True, True)]}")


def c2_old(f):
    """The page before round 19 (pin 505592668894): identical cell, without the bubble clause in L2."""
    return c2(f, bubble_l2=False)


def scores(ff, strict=False):
    return {
        "C1": c1(ff["C1"], strict), "C2": c2(ff["C2"]), "C3": c3(ff["C3"]), "C4": c4(ff["C4"]), "C5": c5(ff["C5"]),
    }


exA = {
    "C1": dict(names_both=True, dates_e=True, dates_c=True, loc_e=True, loc_c=True, picks_two=True),
    "C2": dict(chain3=True, chain_any=True, rests_all=True, analogy=True, failure=True, failure_evidence=True,
               bubble=True, benchmark=True, similarity=True, difference=True),
    "C3": dict(all_cited_or_inference=True, no_locator_count=0, counter_or_none=True, uncited_count=0, has_source=True),
    "C4": dict(computed=True, unrounded_all=True, rule_all=True, rule_all_but_one_nonrounded=True, rule_some=True,
               rounds_input=False, formula_all=True, base_sign_all=True),
    "C5": dict(limits=3, tested=1, caveat=True),
}
exB = {
    "C1": dict(names_both=True, dates_e=True, dates_c=False, loc_e=True, loc_c=False, picks_two=True),
    "C2": dict(chain3=False, chain_any=False, rests_all=False, analogy=False, failure=False, failure_evidence=False,
               bubble=False, benchmark=False, similarity=True, difference=True),
    "C3": dict(all_cited_or_inference=False, no_locator_count=3, counter_or_none=False, uncited_count=3,
               has_source=True),
    "C4": dict(computed=True, unrounded_all=False, rule_all=False, rule_all_but_one_nonrounded=False, rule_some=True,
               rounds_input=True, formula_all=False, base_sign_all=False),
    "C5": dict(limits=0, tested=0, caveat=True),
}
print("exemplar A scores (expect 4,4,4,4,3):", [scores(exA)[k] for k in ("C1", "C2", "C3", "C4", "C5")])
print("exemplar B scores (expect 2,2,1,2,1):", [scores(exB)[k] for k in ("C1", "C2", "C3", "C4", "C5")])

# The ten student-error patterns of plan section 5.4, each applied to the exemplar-A essay (a 4 on C2 and C4).
patterns = {
    "1 real debt as nominal (wrong formula)": ("C4", dict(formula_all=False)),
    "2 percent change with no base or sign": ("C4", dict(base_sign_all=False)),
    "3 bubble for a price rise, no benchmark": ("C2", dict(bubble=True, benchmark=False)),
    "4 locator does not contain claim (counts as uncited)": ("C3", dict(all_cited_or_inference=False, uncited_count=1,
                                                                       no_locator_count=1)),
    "5 analogy asserted, no failure step": ("C2", dict(failure=False, failure_evidence=False)),
    "6 numbers rounded before computing": ("C4", dict(rounds_input=True, unrounded_all=False,
                                                     rule_all_but_one_nonrounded=False)),
    "7 causal gold-standard claim, no source": ("C3", dict(all_cited_or_inference=False, uncited_count=1)),
    "8 current-condition number, no source": ("C3", dict(all_cited_or_inference=False, uncited_count=1)),
    "9 rung-2 blank from memory (lab, not rubric)": (None, {}),
    "10 episode date with no locator (dates both, locator for condition only)": ("C1", dict(loc_e=False)),
}
variant = {k: dict(v) for k, v in exA.items()}
variant["C2"].update(similarity=False, difference=False, bubble=True, benchmark=False)
print("bubble without benchmark, no similarity or difference listed: new C2 =", c2(variant["C2"]),
      "old C2 =", c2_old(variant["C2"]))
variant["C2"].update(benchmark=True)
print("same essay with the benchmark named: new C2 =", c2(variant["C2"]), "old C2 =", c2_old(variant["C2"]))
for name, (crit, change) in patterns.items():
    base = {k: dict(v) for k, v in exA.items()}
    if crit:
        base[crit].update(change)
    new = scores(base)
    old = None
    if crit == "C2":
        old = c2_old(base["C2"])
    print(f"pattern {name}: {crit or '-'} -> {new[crit] if crit else 'lab'}"
          + (f" (before round 19: {old})" if old is not None else ""))
