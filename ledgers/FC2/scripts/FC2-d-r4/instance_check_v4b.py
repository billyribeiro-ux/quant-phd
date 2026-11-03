"""Check the FC2 instance generator against its docstring and the reference scanner (round 4, this verifier).

Usage: python -I instance_check_v4b.py <grader_dir>   (run with the grader directory as argument; it adds it to sys.path)
Checks seeds 0..999 for the documented ranges, half-cent gaps, clean chains and planted gross, and prints the
findings of 20 sample seeds.
"""

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

grader = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(grader))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("reference_mod", grader / "reference.py")
ref = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(ref)  # type: ignore[union-attr]


def scan_of(inst: dict) -> list:
    return ref.scan(
        {
            "spot_cents": inst["spot_cents"],
            "df_ppm": inst["df_ppm"],
            "strikes_cents": inst["strikes_cents"],
            "call_cents": inst["call_cents"],
            "put_cents": inst["put_cents"],
            "cost": {"fee_cents_per_contract": inst["fee_cents_per_contract"],
                     "half_spread_cents": inst["half_spread_cents"]},
        }
    )


problems: list[str] = []
kinds: dict[str, int] = {}
for seed in range(1000):
    inst = make_instance(seed)
    kinds[inst["planted_kind"]] = kinds.get(inst["planted_kind"], 0) + 1
    if not 8000 <= inst["spot_cents"] <= 20000:
        problems.append(f"seed {seed}: spot out of 80.00-200.00")
    if not 930000 <= inst["df_ppm"] <= 999000:
        problems.append(f"seed {seed}: df out of 0.930000-0.999000")
    if not 0 <= inst["fee_cents_per_contract"] <= 40 or not 1 <= inst["half_spread_cents"] <= 150:
        problems.append(f"seed {seed}: cost out of documented range")
    s = inst["strikes_cents"]
    if len(s) != 6 or any(s[i + 1] - s[i] != s[1] - s[0] for i in range(5)):
        problems.append(f"seed {seed}: strikes not evenly spaced")
    calls = inst["call_cents"]
    if min(calls) <= 0:
        problems.append(f"seed {seed}: non-positive call")
    for k in range(6):
        if inst["planted_kind"] == "parity" and k == inst["planted_index"]:
            continue  # the planted put is moved on purpose; every other strike is within half a cent
        gap = (Fraction(calls[k]) - Fraction(inst["put_cents"][k])
               - (Fraction(inst["spot_cents"]) - Fraction(s[k] * inst["df_ppm"], 1_000_000)))
        if abs(gap) > Fraction(1, 2):
            problems.append(f"seed {seed}: clean parity residual above half a cent at strike {k}")
        if gap.denominator == 2:
            problems.append(f"seed {seed}: half-cent gap present")
    if any(calls[j - 1] - 2 * calls[j] + calls[j + 1] < 0 for j in range(1, 5)) and inst["planted_kind"] != "convexity":
        problems.append(f"seed {seed}: unplanted convexity violation")
    findings = scan_of(inst)
    if inst["planted_kind"] == "none" and findings:
        problems.append(f"seed {seed}: clean chain has findings")
    if inst["planted_kind"] in ("parity", "convexity") and inst["planted_amount_cents"] > 0:
        cost = 3 * (inst["fee_cents_per_contract"] + inst["half_spread_cents"])
        if inst["planted_amount_cents"] - cost > 0:
            match = [f for f in findings if f["strike_cents"] == s[inst["planted_index"]]]
            if not match or match[0]["gross_cents"] != inst["planted_amount_cents"]:
                problems.append(f"seed {seed}: planted gross not reported")

print("seeds checked: 1000; planted kinds:", kinds)
print("problems:", len(problems))
for p in problems[:20]:
    print("  ", p)
print("20 sample seeds: findings (kind, strike, gross, net)")
signatures = set()
for seed in [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]:
    inst = make_instance(seed)
    rows = [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in scan_of(inst)]
    signatures.add(tuple(rows))
    print(f"  seed {seed}: planted={inst['planted_kind']} findings={rows}")
print("distinct finding lists among the 20 sample seeds:", len(signatures))
