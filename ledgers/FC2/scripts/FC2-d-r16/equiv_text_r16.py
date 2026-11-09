"""Equivalence check for the three wording-only mutants (ruling 34): over seeds 0-49, the reference and each mutant
must give identical records except the explanation text, and each explanation must name the same P-labels and the
same rule word as the reference. Also checks the convexity sign and the findings list on the second chain.
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/FC/FC2/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

RULE_WORDS = {"parity": "parity", "convexity": "convex"}


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chain_of(inst: dict) -> dict:  # type: ignore[type-arg]
    return {
        "spot_cents": inst["spot_cents"],
        "df_ppm": inst["df_ppm"],
        "strikes_cents": list(inst["strikes_cents"]),
        "call_cents": list(inst["call_cents"]),
        "put_cents": list(inst["put_cents"]),
        "cost": {
            "fee_cents_per_contract": inst["fee_cents_per_contract"],
            "half_spread_cents": inst["half_spread_cents"],
        },
    }


ref = load(GRADER / "reference.py", "ref_equiv")
mutants = {
    "r15_a": ROOT / "ledgers/FC2/mutants/r15_a_parity_explanation_reverses_the_positive_gap_trade.py",
    "r15_c": ROOT / "ledgers/FC2/equivalent/r15_c_parity_explanation_prints_gross_where_net_belongs.py",
    "r15_d": ROOT / "ledgers/FC2/equivalent/r15_d_convexity_explanation_reverses_the_chord_side.py",
}
modules = {k: load(v, "m_" + k) for k, v in mutants.items()}
bad = 0
texts = 0
for seed in range(50):
    for inst in (make_instance(seed), make_instance(seed + 7_919)):
        chain = chain_of(inst)
        expected = ref.scan(chain)
        for name, mod in modules.items():
            got = mod.scan(chain)
            strip = lambda rs: [{k: v for k, v in r.items() if k != "explanation"} for r in rs]  # noqa: E731
            if strip(got) != strip(expected) or len(got) != len(expected):
                bad += 1
                print("RECORD DIFF", name, seed)
                continue
            for g, e in zip(got, expected):
                texts += 1
                gl = set(re.findall(r"\bP[1-6]\b", g["explanation"]))
                el = set(re.findall(r"\bP[1-6]\b", e["explanation"]))
                if gl != el or not re.search(RULE_WORDS[g["kind"]], g["explanation"], re.IGNORECASE):
                    bad += 1
                    print("LABEL/RULE DIFF", name, seed, sorted(gl), sorted(el))
print("compared explanation texts:", texts, "differences:", bad)
