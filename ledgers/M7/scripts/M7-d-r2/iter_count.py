"""Round-2 check of the reference comment (grader/reference.py, active-set loop): 'a cap far above the iterations the
search uses on seeds 0 to 49 (at most 12)'. Counts loop iterations by re-running the reference loop body verbatim."""
import sys, json, pathlib, re
G = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/course/modules/M/M7/grader")
sys.path.insert(0, str(G))
import reference as R
from instance import make_instance
src = (G / "reference.py").read_text(encoding="utf-8")
# instrument: count iterations of the 'for _ in range(200)' loop in _active_set
src = src.replace("    for _ in range(200):", "    global ITER\n    for _ in range(200):\n        ITER += 1", 1)
src = src.replace("from __future__ import annotations", "from __future__ import annotations\nITER = 0", 1)
import types
mod = types.ModuleType("ref_instrumented")
sys.modules["ref_instrumented"] = mod
exec(compile(src, "ref_instrumented", "exec"), mod.__dict__)
ns = mod.__dict__
worst = 0
for seed in range(50):
    ns["ITER"] = 0
    case = json.loads(make_instance(seed)["payload"])
    ns["allocate"](case)
    worst = max(worst, ns["ITER"])
print("max loop iterations (counting every pass of the loop body) over seeds 0-49:", worst)
