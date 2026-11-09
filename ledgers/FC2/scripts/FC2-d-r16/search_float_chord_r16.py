"""Search small chains for an exact convexity tie that the float-weight mutant (r16_c) rounds differently.

Zero cost, df = 1, puts chosen so every parity gap is zero, so only convexity findings can appear.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ref = load(ROOT / "course/modules/FC/FC2/grader/reference.py", "ref_search")
mut = load(ROOT / "ledgers/FC2/mutants/r16_c_convexity_chord_weights_as_float_fractions.py", "mut_search")

found = []
checked = 0
for low in range(1, 40):
    for mid in range(low + 1, low + 30):
        for high in range(mid + 1, mid + 30):
            if (high - low) % 2 == 0 and (high - low) < 4:
                continue
            for c_low in range(0, 12):
                for c_high in range(0, 12):
                    for c_mid in range(0, 12):
                        calls = [c_low, c_mid, c_high]
                        strikes = [low, mid, high]
                        spot = 0
                        puts = [c - spot + k for c, k in zip(calls, strikes)]
                        chain = {
                            "spot_cents": spot,
                            "df_ppm": 1_000_000,
                            "strikes_cents": strikes,
                            "call_cents": calls,
                            "put_cents": puts,
                            "cost": {"fee_cents_per_contract": 0, "half_spread_cents": 0},
                        }
                        checked += 1
                        a = [(r["kind"], r["strike_cents"], r["gross_cents"]) for r in ref.scan(chain)]
                        b = [(r["kind"], r["strike_cents"], r["gross_cents"]) for r in mut.scan(chain)]
                        if a != b:
                            found.append((strikes, calls, a, b))
                            if len(found) >= 3:
                                break
                    if len(found) >= 3:
                        break
                if len(found) >= 3:
                    break
            if len(found) >= 3:
                break
        if len(found) >= 3:
            break
    if len(found) >= 3:
        break

print("checked", checked, "mismatches", len(found))
for item in found:
    print("strikes", item[0], "calls", item[1], "reference", item[2], "mutant", item[3])
