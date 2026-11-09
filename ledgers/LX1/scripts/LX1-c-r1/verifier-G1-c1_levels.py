"""Verifier G1: enumerates every fact vector of an essay's episode-and-condition element against the CURRENT C1 cell
(project.html line 473, read from the checkout, not retyped) and reports overlaps and uncovered vectors.
Predicates follow the cell text: names episode/condition (nE, nC); says which is which (lab); dates for each (dE, dC);
a locator for each date (lE, lC); every locator of a listed type (typed; level 4 only)."""
import itertools
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
line = page.splitlines()[472]
assert 'data-criterion="C1"' in line, "line 473 is not the C1 row"
cells = re.findall(r"<td>(.*?)</td>", line)
assert len(cells) == 4, cells
print("cell text 4 (level 1):", cells[3])
print("cell text 3 (level 2):", cells[2])
print("cell text 2 (level 3):", cells[1])
print("cell text 1 (level 4):", cells[0])


def levels(nE, nC, lab, dE, dC, lE, lC, typed):
    both = nE and nC
    met = set()
    if both and lab and dE and dC and lE and lC and typed:
        met.add(4)
    if both and lab and dE and dC and lE and lC:
        met.add(3)
    if both and lab and not (dE and dC and lE and lC):
        met.add(2)
    if (nE != nC) or (both and not lab):
        met.add(1)
    return met


counts = Counter()
bad = []
zero_named = 0
for v in itertools.product([False, True], repeat=8):
    nE, nC, lab, dE, dC, lE, lC, typed = v
    if not typed and not (lE and lC):
        pass
    if not (nE or nC):
        zero_named += 1
        continue
    met = levels(*v)
    counts[len(met)] += 1
    if len(met) == 0:
        bad.append(v)
    if len(met) > 1:
        top = max(met)
        counts["overlap_vectors"] += 1
        if not (top == 4 or top == 3):
            bad.append(("overlap-at-top", v, sorted(met)))
# Overlaps between the level-1 clause and level 2-4 cells (all met levels, not only the top one)
ov1 = [v for v in itertools.product([False, True], repeat=8) if (lambda m: 1 in m and len(m - {1}) > 0)(levels(*v))]
print("vectors with more than one level met:", counts["overlap_vectors"])
print("vectors meeting level 1 and a level 2-4 cell:", len(ov1))
# Reachability of each level as the highest level met
top = Counter(max(levels(*v)) for v in itertools.product([False, True], repeat=8) if levels(*v))
print("highest-level counts:", dict(sorted(top.items())))
print("vectors naming neither episode nor condition (no level text applies):", zero_named)
print("vectors with no level met (naming at least one):", len(bad))
print("example level-3 vector (not typed):", (True, True, True, True, True, True, True, False), max(levels(True, True, True, True, True, True, True, False)))
print("example level-4 vector (typed):", (True, True, True, True, True, True, True, True), max(levels(True, True, True, True, True, True, True, True)))
