"""For seeds 0-49: the reference answer's weights are distinct across seeds, and the instances' dimensions vary.

Usage: python -I -W error instances_answers_r12.py <repo-root>
"""

import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
grader = root / "course/modules/M/M7/grader"
sys.path.insert(0, str(grader))
import instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref_under_test", grader / "reference.py")
assert spec is not None and spec.loader is not None
ref = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ref
spec.loader.exec_module(ref)

answers = {}
sizes = {}
for seed in range(50):
    case = json.loads(instance.make_instance(seed)["payload"])
    out = ref.allocate(case)
    answers[seed] = tuple(round(w, 9) for w in out["weights"])
    sizes[seed] = len(case["mu"])
print("distinct answers over seeds 0-49:", len(set(answers.values())), "of 50")
print("asset counts over seeds 0-49:", {n: sum(1 for v in sizes.values() if v == n) for n in sorted(set(sizes.values()))})
print("seeds with a weight at a bound (|w-l|<=1e-9 or |u-w|<=1e-9):", sum(
    1 for seed in range(50)
    if any(abs(w - json.loads(instance.make_instance(seed)["payload"])["lower"][i]) <= 1e-9
           or abs(json.loads(instance.make_instance(seed)["payload"])["upper"][i] - w) <= 1e-9
           for i, w in enumerate(ref.allocate(json.loads(instance.make_instance(seed)["payload"]))["weights"]))
))
print("seeds with an active turnover limit:", sum(
    1 for seed in range(50)
    if abs(sum(abs(w - w0) for w, w0 in zip(ref.allocate(json.loads(instance.make_instance(seed)["payload"]))["weights"],
                                           json.loads(instance.make_instance(seed)["payload"])["w0"]))
           - json.loads(instance.make_instance(seed)["payload"])["turnover_limit"]) <= 1e-9
))
