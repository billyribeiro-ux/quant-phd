"""Sample seeds 0-49 of grader/instance.py: validity of each instance and whether the answers differ across seeds.
Usage: python -I instance_validity.py <grader_dir>"""
import json, math, sys
from fractions import Fraction
sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402
bad = []
answers = set()
for seed in range(50):
    inst = make_instance(seed)
    p = json.loads(inst["payload"])
    vals = p["values"]
    ok = (20 <= len(vals) <= 400 and all(math.isfinite(v) for v in vals) and 2 <= p["window"] <= 30
          and p["epsilon"] in (0.05, 0.1, 0.2) and len(p["probes"]) == 10 and all(0 <= q <= 1 for q in p["probes"])
          and "SIMULATED" in inst["label"] and make_instance(seed) == inst)
    if not ok:
        bad.append(seed)
    fr = [Fraction(v) for v in vals]
    mean = sum(fr) / len(fr)
    answers.add((float(mean), p["window"], p["epsilon"]))
    decs = {len(repr(v).split('.')[1]) if '.' in repr(v) and 'e' not in repr(v) else 0 for v in vals}
print(f"invalid seeds: {bad}; distinct (mean, window, epsilon) answers over 50 seeds: {len(answers)}")
