"""Witness for the nine equivalent M7 mutants in ledgers/M7/equivalent/ (proofs in ledgers/M7/equivalent/README.md).

Run from the repository root:
    .venv/bin/python -I ledgers/M7/scripts/M7-d-r14/equiv.py

1. Exact check: on seeds 0-299 (generator cases, decimal inputs read exactly), allocate() of each mutant is compared
   with the reference allocate() field by field (weights, all multipliers, all four certificate fields).
2. Boundary sweep: the same seeds 0-49 in two families. (a) The starting portfolio moved on asset 0 by each delta in
   DELTAS. (b) The turnover limit set to each value in TAUS (0 and two values inside 1e-9). The page states the starting
   tolerance of 1e-9 (project.html, Conventions) and reference.py accepts starts within it (lines 102-107); a turnover
   limit of zero is valid. Refused cases are counted, not compared. The sweep reports the largest absolute difference
   per field. It is a measurement on these two families, not a proof.
3. Structural count: how many reference answers have a smallest inequality multiplier exactly zero (the claim the
   README's arguments rest on).
"""

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
GRADER = REPO / "course/modules/M/M7/grader"
EQUIVALENT = REPO / "ledgers/M7/equivalent"
sys.path.insert(0, str(GRADER))
import instance  # noqa: E402
import reference  # noqa: E402

DELTAS = [9e-10, -9e-10, 5e-10, -5e-10, 1e-10, -1e-10]
TAUS = [0.0, 1e-10, 9e-10]


def load(path: Path, index: int):
    spec = importlib.util.spec_from_file_location(f"equivalent_mutant_{index}", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def flat(obj):
    if isinstance(obj, dict):
        for key in sorted(obj):
            yield from flat(obj[key])
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from flat(value)
    else:
        yield float(obj)


def max_diff(a, b) -> float:
    fa, fb = list(flat(a)), list(flat(b))
    if len(fa) != len(fb):
        return float("inf")
    return max((abs(x - y) for x, y in zip(fa, fb, strict=True)), default=0.0)


def case_of(seed: int) -> dict:
    return json.loads(instance.make_instance(seed)["payload"])


def inequality_entries(out: dict) -> list[float]:
    m = out["multipliers"]
    return [*m["lower"], *m["upper"], *m["sector"], *m["turnover_plus"], *m["turnover_minus"], m["turnover_total"]]


names = sorted(p.name for p in EQUIVALENT.glob("*.py"))
mutants = [(name, load(EQUIVALENT / name, i)) for i, name in enumerate(names)]
print(f"equivalent mutants found: {len(mutants)}")

exact_cases = [case_of(s) for s in range(300)]
reference_exact = [reference.allocate(json.loads(json.dumps(c))) for c in exact_cases]
zero_min = sum(1 for out in reference_exact if min(inequality_entries(out)) == 0)
print(f"reference, seeds 0-299: smallest inequality multiplier exactly 0 on {zero_min} of 300")

for name, module in mutants:
    differing = [
        s
        for s, case in enumerate(exact_cases)
        if max_diff(reference_exact[s], module.allocate(json.loads(json.dumps(case)))) != 0.0
    ]
    print(f"{name}: differs from reference on {len(differing)} of 300 exact seeds {differing[:5]}")

perturbed_answered = 0
perturbed_refused = 0
perturbed_zero_min = 0
worst: dict[str, dict[str, float]] = {name: {"certificate": 0.0, "all": 0.0} for name, _ in mutants}
for seed in range(50):
    variants = [("start", delta) for delta in DELTAS] + [("turnover", tau) for tau in TAUS]
    for kind, value in variants:
        case = case_of(seed)
        if kind == "start":
            case["w0"][0] = round(case["w0"][0] + value, 12)
        else:
            case["turnover_limit"] = value
        try:
            ref = reference.allocate(json.loads(json.dumps(case)))
        except ValueError:
            perturbed_refused += 1
            continue
        perturbed_answered += 1
        if min(inequality_entries(ref)) == 0:
            perturbed_zero_min += 1
        for name, module in mutants:
            out = module.allocate(json.loads(json.dumps(case)))
            worst[name]["certificate"] = max(
                worst[name]["certificate"], max_diff(ref["certificate"], out["certificate"])
            )
            worst[name]["all"] = max(worst[name]["all"], max_diff(ref, out))

print(
    f"boundary sweep: seeds 0-49 x (deltas {DELTAS}, turnover limits {TAUS}): "
    f"answered {perturbed_answered}, refused {perturbed_refused}"
)
print(
    f"boundary sweep: smallest inequality multiplier exactly 0 on {perturbed_zero_min} of {perturbed_answered} answers"
)
for name, _ in mutants:
    print(
        f"{name}: largest |difference| certificate {worst[name]['certificate']:.3e}, "
        f"all output fields {worst[name]['all']:.3e}"
    )
