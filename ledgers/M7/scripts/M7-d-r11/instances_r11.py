"""Sample the M7 instances on seeds 0-49: validity (reference refuses none), distinct answers, binding constraints."""
import importlib.util, json, sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve()
G = ROOT / "course/modules/M/M7/grader"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod); return mod
inst = load("inst", G / "instance.py")
ref = load("ref", G / "reference.py")
answers = {}
rows = []
for seed in range(50):
    case = json.loads(inst.make_instance(seed)["payload"])
    out = ref.allocate(case)
    w = [round(x, 6) for x in out["weights"]]
    answers.setdefault(tuple(w), []).append(seed)
    m = out["multipliers"]
    binding = []
    if any(abs(x) > 1e-12 for x in m["lower"]): binding.append("lower")
    if any(abs(x) > 1e-12 for x in m["upper"]): binding.append("upper")
    if any(abs(x) > 1e-12 for x in m["sector"]): binding.append("sector")
    if any(abs(x) > 1e-12 for x in m["turnover_plus"]) or any(abs(x) > 1e-12 for x in m["turnover_minus"]): binding.append("turnover")
    rows.append((seed, len(case["mu"]), len(case["sector_caps"]), ",".join(binding) or "none", round(m["turnover_total"], 6), w))
for r in rows[:50]:
    print(r)
print("distinct answers:", len(answers), "of 50")
print("n counts:", {n: sum(1 for r in rows if r[1] == n) for n in (3, 4, 5)})
print("binding sets:", {b: sum(1 for r in rows if r[3] == b) for b in sorted({r[3] for r in rows})})
