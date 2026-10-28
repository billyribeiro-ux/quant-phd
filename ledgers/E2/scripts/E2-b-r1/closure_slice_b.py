"""E2 slice b verifier script: prerequisite closure of E2 and the owners of the concepts the slice names.

Usage: <checkout>/.venv/bin/python -I <checkout>/ledgers/E2/scripts/E2-b-r1/closure_slice_b.py <checkout>
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import yaml

root = Path(sys.argv[1]).resolve()
mods: dict[str, dict] = {}


def walk(obj: object) -> None:
    if isinstance(obj, dict):
        if "id" in obj and "prereqs" in obj:
            mods[obj["id"]] = obj
        for value in obj.values():
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)


for f in sorted(glob.glob(str(root / "curriculum" / "0*.yaml"))):
    walk(yaml.safe_load(Path(f).read_text(encoding="utf-8")))


def closure(mid: str, seen: set[str]) -> set[str]:
    for p in mods[mid].get("prereqs", []):
        if p not in seen:
            seen.add(p)
            closure(p, seen)
    return seen


print("E2 prerequisites:", mods["E2"]["prereqs"])
print("E2 prerequisite closure:", sorted(closure("E2", set())))
concepts = json.loads((root / "curriculum" / "curriculum.json").read_text(encoding="utf-8"))["concepts"]
for name in ["expectation", "conditional-expectation-elementary", "envelope-theorem", "derivative", "partial-derivative",
             "hessian", "expected-utility", "bayesian-inference", "first-welfare-theorem", "risk-neutral-probability",
             "adverse-selection", "signaling", "screening", "moral-hazard", "principal-agent", "concave-function"]:
    print(f"concept {name}: owner {concepts.get(name, {}).get('module', 'NOT IN curriculum.json concepts')}")
