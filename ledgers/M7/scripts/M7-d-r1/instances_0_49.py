"""Sample check of the generator over seeds 0-49: validity, determinism, and whether the answers and active sets differ.

Usage: python3 -I instances_0_49.py <grader_dir>
Validity is checked by the reference's own parser (which refuses invalid cases) and by a direct check of the bounds,
caps and the starting portfolio. Active sets are the inequality multipliers the reference reports as non-zero.
"""
import importlib.util
import json
import sys
from pathlib import Path

g = Path(sys.argv[1])


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


inst = load("inst_chk", g / "instance.py")
ref = load("ref_chk", g / "reference.py")
patterns = {}
answers = {}
bad = []
for seed in range(50):
    a = inst.make_instance(seed)
    b = inst.make_instance(seed)
    if a != b:
        bad.append((seed, "nondeterministic"))
    case = json.loads(a["payload"])
    n = len(case["mu"])
    if any(case["lower"][i] > case["upper"][i] for i in range(n)):
        bad.append((seed, "lower above upper"))
    if any(not (case["lower"][i] <= case["w0"][i] <= case["upper"][i]) for i in range(n)):
        bad.append((seed, "start outside box"))
    if abs(sum(case["w0"]) - 1) > 1e-12:
        bad.append((seed, "start does not sum to one"))
    for k, cap in enumerate(case["sector_caps"]):
        if sum(case["w0"][i] for i in range(n) if case["sector"][i] == k) > cap + 1e-12:
            bad.append((seed, "start breaks cap"))
    out = ref.allocate(case)
    m = out["multipliers"]
    active = tuple(
        [f"lower{i}" for i in range(n) if m["lower"][i] != 0]
        + [f"upper{i}" for i in range(n) if m["upper"][i] != 0]
        + [f"sector{k}" for k, v in enumerate(m["sector"]) if v != 0]
        + (["turnover"] if m["turnover_total"] != 0 else [])
    )
    patterns.setdefault(active, []).append(seed)
    answers[seed] = tuple(round(x, 9) for x in out["weights"])
print("validity problems:", bad)
print("distinct active sets over seeds 0-49:", len(patterns))
print("distinct answers over seeds 0-49:", len(set(answers.values())))
print("asset counts:", {n: sum(1 for s in range(50) if len(json.loads(inst.make_instance(s)['payload'])['mu']) == n) for n in (3, 4, 5)})
for pat, seeds in sorted(patterns.items(), key=lambda kv: -len(kv[1]))[:8]:
    print(len(seeds), "seeds, e.g.", seeds[:6], "active:", pat)
