"""Round-14 witness for the eight removed M7 equivalent mutants (ledgers/M7/mutant_equivalence_r14.json).

Run: python -I ledgers/M7/scripts/M7-d-r14/equiv_witness_r14.py <repo_root>
For each removed mutant (sources recovered from git at d2b4a874^ into equiv_removed_r14/): exact allocate() output
equals the reference output on seeds 0-49 and on the six hand cases of the suite. Also counts, per seed, the zero
inequality multipliers of the reference (the structural claim: at least one is always zero).
"""

import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
here = Path(__file__).resolve().parent / "equiv_removed_r14"
sys.path.insert(0, str(root / "course/modules/M/M7/grader"))
import instance  # noqa: E402
import reference as R  # noqa: E402

sys.path.insert(0, str(root / "course/modules/M/M7/grader"))
spec_test = importlib.util.spec_from_file_location("tp_hand", root / "course/modules/M/M7/grader/test_project.py")
names = sorted(p.name for p in here.glob("*.py"))
cases = [json.loads(instance.make_instance(s)["payload"]) for s in range(50)]
min_zero = sum(1 for c in cases if min(
    [*R.allocate(c)["multipliers"]["lower"], *R.allocate(c)["multipliers"]["upper"],
     *R.allocate(c)["multipliers"]["sector"], *R.allocate(c)["multipliers"]["turnover_plus"],
     *R.allocate(c)["multipliers"]["turnover_minus"], R.allocate(c)["multipliers"]["turnover_total"]]) == 0)
print("reference: seeds 0-49 whose smallest inequality multiplier is exactly 0:", min_zero, "of 50")
for i, name in enumerate(names):
    spec = importlib.util.spec_from_file_location(f"mut_{i}", here / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    diff = [s for s, c in enumerate(cases) if R.allocate(json.loads(json.dumps(c))) != mod.allocate(json.loads(json.dumps(c)))]
    print(name, "differs from reference on", len(diff), "of 50 seeds", diff[:5])
