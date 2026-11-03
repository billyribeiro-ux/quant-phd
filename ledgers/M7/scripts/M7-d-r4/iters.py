"""Count active-set loop iterations of the reference per seed (0-49): an instrumented copy of reference.py is written
to a scratch directory and imported as a module."""
import sys, json, os
grader = sys.argv[1]
src = open(os.path.join(grader, "reference.py"), encoding="utf-8").read()
marker = "    for _ in range(200):  # a cap far above the iterations the search uses on seeds 0 to 49 (at most 12)\n"
assert src.count(marker) == 1, src.count(marker)
src = src.replace(marker, marker + "        STATS['it'] += 1\n")
src = src.replace("from __future__ import annotations\n", "from __future__ import annotations\nSTATS = {'it': 0}\n", 1)
scratch = "/tmp/m7d-r4-floor/instr"
os.makedirs(scratch, exist_ok=True)
open(os.path.join(scratch, "ref_instr.py"), "w", encoding="utf-8").write(src)
sys.path.insert(0, scratch)
sys.path.insert(1, grader)
import ref_instr as ref
from instance import make_instance
best = []
for s in range(50):
    ref.STATS["it"] = 0
    case = json.loads(make_instance(s)["payload"])
    ref.allocate(case)
    best.append((ref.STATS["it"], s))
print("max iterations seeds 0-49:", max(best), "distinct counts:", sorted({b for b, _ in best}))
