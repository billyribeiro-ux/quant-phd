"""Instance validity over seeds 0-49 and materiality over a 20-seed sample (answers, not labels, differ).
Usage: python -I instances_r14.py (run from the checkout root)."""

from __future__ import annotations

import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/CS/CS2/grader"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


inst = load("instance_r14b", GRADER / "instance.py")
ref = load("reference_r14b", GRADER / "reference.py")
bad: list[str] = []
answers: dict[int, tuple[float, float, float, float]] = {}
for seed in range(50):
    d = inst.make_instance(seed)
    p = json.loads(d["payload"])
    inv = json.loads(d["invalid"])
    vals = p["values"]
    if not (20 <= len(vals) <= 400 and all(math.isfinite(x) for x in vals)):
        bad.append(f"{seed}: length/finite")
    if not (2 <= p["window"] <= 30) or p["epsilon"] not in (0.05, 0.1, 0.2):
        bad.append(f"{seed}: window/epsilon")
    if len(p["probes"]) != 10 or not all(0.0 <= q <= 1.0 for q in p["probes"]):
        bad.append(f"{seed}: probes")
    if "SIMULATED" not in d["label"] or inv["kind"] not in inst.INVALID_KINDS:
        bad.append(f"{seed}: label/invalid")
    for x in vals:
        s = repr(float(x))
        dec = len(s.split(".")[1]) if "." in s else 0
        if dec > 6:
            bad.append(f"{seed}: value with >6 decimals {x}")
            break
    if inst.make_instance(seed) != d:
        bad.append(f"{seed}: not deterministic")
    acc = ref.WelfordAccumulator()
    for x in vals:
        acc.update(float(x))
    sk = ref.QuantileSketch(p["epsilon"])
    for x in vals:
        sk.add(float(x))
    answers[seed] = (acc.mean(), acc.variance(1), sk.quantile(0.5), float(max(vals)))
print("validity problems:", bad if bad else "none")
sample = list(range(20))
print("20-seed sample (seed: mean, sample var, median-sketch answer, max):")
for s in sample:
    m, v, med, mx = answers[s]
    print(f"  {s}: {m:.6f} {v:.6f} {med:.6f} {mx:.6f}")
print("distinct (mean, variance) pairs over seeds 0-19:", len({(round(answers[s][0], 9), round(answers[s][1], 9)) for s in sample}), "of 20")
print("distinct sketch medians over seeds 0-49:", len({answers[s][2] for s in range(50)}), "of 50")
