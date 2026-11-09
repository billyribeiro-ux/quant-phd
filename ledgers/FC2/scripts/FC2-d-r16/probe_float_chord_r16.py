"""Probe: exact convexity half-cent tie at a non-dyadic chord weight (ratio 5/6, 1/6), zero cost, no parity finding."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/FC/FC2/grader/reference.py"
MUTANT = ROOT / "ledgers/FC2/mutants/r16_c_convexity_chord_weights_as_float_fractions.py"


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ref = load(GRADER, "ref_probe")
mut = load(MUTANT, "mut_probe")

# chord at 101 from strikes 100 and 106 with calls 0 and 3: (5*0 + 1*3)/6 = 1/2 exactly; the call at 101 is 1,
# so the violation is 1 - 1/2 = 1/2 cent, an exact half-cent tie. Parity gaps are zero: put = call - spot + strike.
strikes = [100, 101, 106]
calls = [0, 1, 3]
spot = 100
df = 1_000_000
puts = [c - spot + k for c, k in zip(calls, strikes)]
chain = {
    "spot_cents": spot,
    "df_ppm": df,
    "strikes_cents": strikes,
    "call_cents": calls,
    "put_cents": puts,
    "cost": {"fee_cents_per_contract": 0, "half_spread_cents": 0},
}
print("reference:", [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in ref.scan(chain)])
print("mutant   :", [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in mut.scan(chain)])
print("mutant second difference is float:", repr(mut._second_difference(strikes, calls, 1)))
print("reference second difference exact:", repr(ref._second_difference(strikes, calls, 1)))
sys.exit(0)
