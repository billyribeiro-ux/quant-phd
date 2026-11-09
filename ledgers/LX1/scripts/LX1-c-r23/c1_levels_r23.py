"""Round 23 (LX1-c): enumerates every combination of the C1 facts an essay can show (item-level booleans) and the
level each cell of project.html:473 (current text) assigns. Reports (a) combinations matched by two or more levels
(dominance / overlap), (b) combinations matched by no level, and (c) combinations whose level-1 match depends on
reading 'event' as 'episode' (a condition-only essay). Usage: python -I c1_levels_r23.py"""
from itertools import product

FACTS = ["E", "C", "W", "dE", "dC", "lE", "lC", "ldE", "ldC"]
# E episode named; C condition named; W says which is the episode and which the condition; dE/dC a date for each;
# lE/lC a locator for each item; ldE/ldC a locator for every date of the item (implies a date and a locator).


def levels(f):
    L4 = f["E"] and f["C"] and f["W"] and f["dE"] and f["dC"] and f["ldE"] and f["ldC"]
    L3 = f["E"] and f["C"] and f["W"] and f["dE"] and f["dC"] and f["lE"] and f["lC"]
    L2 = f["E"] and f["C"] and f["W"] and not L3
    # level 1 as printed: "names one event" (read literally, the episode) or "names two without saying which"
    L1_event = (f["E"] and not f["C"]) or (f["E"] and f["C"] and not f["W"])  # 'event' read as the episode
    L1_either_item = (f["E"] != f["C"]) or (f["E"] and f["C"] and not f["W"])  # 'event' read as episode or condition
    return {"4": bool(L4), "3": bool(L3), "2": bool(L2), "1": bool(L1_event)}, {"4": bool(L4), "3": bool(L3), "2": bool(L2), "1": bool(L1_either_item)}


overlap, nolevel, event_dep = [], [], []
for vals in product([False, True], repeat=len(FACTS)):
    f = dict(zip(FACTS, vals))
    if f["ldE"] and not f["dE"] or f["ldC"] and not f["dC"]:
        continue  # a locator for every date needs a date
    if f["lE"] and False:
        continue
    lit, either = levels(f)
    hit_lit = [k for k, v in lit.items() if v]
    hit_either = [k for k, v in either.items() if v]
    if len(hit_lit) >= 2 and hit_lit != ["4", "3"]:
        overlap.append((vals, hit_lit))
    if not hit_lit:
        nolevel.append(vals)
    if hit_lit != hit_either:
        event_dep.append((vals, hit_lit, hit_either))
print("combinations checked:", sum(1 for vals in product([False, True], repeat=len(FACTS)) if not (dict(zip(FACTS, vals))["ldE"] and not dict(zip(FACTS, vals))["dE"] or dict(zip(FACTS, vals))["ldC"] and not dict(zip(FACTS, vals))["dC"])))
print("overlap other than 4 with 3 (highest level applies): ", len(overlap))
print("no level (literal reading, score 0):", len(nolevel))
print("literal vs 'names one item' reading differ on:", len(event_dep))
for vals, lit, either in event_dep[:6]:
    print("  facts", {k: v for k, v in zip(FACTS, vals) if v}, "literal", lit, "either-item", either)
print("L4 and L3 differ only when a date has no locator of its own (ldE/ldC false, lE/lC true):")
d = [vals for vals in product([False, True], repeat=len(FACTS)) if (lambda f: f["E"] and f["C"] and f["W"] and f["dE"] and f["dC"] and f["lE"] and f["lC"] and not (f["ldE"] and f["ldC"]))(dict(zip(FACTS, vals)))]
print("  such combinations:", len(d))
