"""Round 1 (LX1-c): enumerates the C1 facts an essay can show and the levels of project.html C1 (pin 95f3f8cb cells).
Facts: nE, nC = number of episodes / conditions named (0..2); labelled = says which item is the episode and which the
condition; dE, dC = date given for the episode / condition; lE, lC = some locator for it; tE, tC = locator of a type the
L4 cell lists (page, table, section, title field, MANIFEST row). Reports, for the 'lenient' reading (levels 2-4 do not
require labelling) and the 'strict' reading (they do), the combinations matched by level 1 and by a level 2-4, and the
score the highest-level rule gives. Usage: python -I c1_levels_r1.py"""
from itertools import product

def levels(f, strict):
    nE, nC, lab, dE, dC, lE, lC, tE, tC = f
    names_both = nE > 0 and nC > 0 and (lab or not strict)
    L1 = ((nE > 0) != (nC > 0)) or (nE + nC >= 2 and not lab)
    L4 = names_both and dE and dC and tE and tC
    L3 = names_both and dE and dC and lE and lC
    L2 = names_both and not (dE and dC and lE and lC)
    return {1: L1, 2: L2, 3: L3, 4: L4}

def score(m):
    best = 0
    for lvl in (1, 2, 3, 4):
        if m[lvl]:
            best = lvl
    return best

for strict in (False, True):
    overlap = 0
    l1_only = 0
    none = 0
    ex = []
    for nE, nC, lab, dE, dC, lE, lC, tE, tC in product((0, 1, 2), (0, 1, 2), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)):
        if tE and not lE or tC and not lC:
            continue
        f = (nE, nC, lab, dE, dC, lE, lC, tE, tC)
        m = levels(f, strict)
        if m[1] and (m[2] or m[3] or m[4]):
            overlap += 1
            if len(ex) < 3:
                ex.append((f, score(m)))
        if score(m) == 0:
            none += 1
        if m[1] and score(m) == 1:
            l1_only += 1
    print(f"reading={'strict' if strict else 'lenient'}: combos level1 and level2-4 both match={overlap}; "
          f"score 1 by highest-level rule={l1_only}; score 0={none}; examples (nE,nC,labelled,dE,dC,lE,lC,tE,tC; score)={ex}")
