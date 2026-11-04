"""Probe the three new survivors: each chain is one the specification says must raise ValueError (or is clean)."""

import importlib.util
import sys
from pathlib import Path

grader = Path(sys.argv[1]).resolve()
mutants = Path(sys.argv[2]).resolve()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def outcome(fn, *args):
    try:
        return "returned " + repr(fn(*args))
    except ValueError as exc:
        return f"ValueError: {exc}"
    except Exception as exc:  # noqa: BLE001
        return f"{type(exc).__name__}: {exc}"


ref = load(grader / "reference.py", "ref")
# negative fee with a positive total cost (3 * (-1 + 4) = 9): the one parity gap is 0, gross 0, net -9, so no finding
chain_fee = {"spot_cents": 100, "df_ppm": 1_000_000, "strikes_cents": [100], "call_cents": [0], "put_cents": [0],
             "cost": {"fee_cents_per_contract": -1, "half_spread_cents": 4}}
chain_2 = ([100, 110], [5, 5])
# one strike, two puts: convexity_violations does not look at puts, so only scan's own put check can reject it
chain_1 = {"spot_cents": 100, "df_ppm": 1_000_000, "strikes_cents": [100], "call_cents": [5], "put_cents": [0, 0],
           "cost": {"fee_cents_per_contract": 0, "half_spread_cents": 0}}
for name in ["x8_a_cost_checked_only_when_a_parity_finding_is_kept.py", "x8_b_short_chain_skips_validation_in_convexity.py",
             "x8_c_one_strike_chain_skips_quote_length_check.py"]:
    mod = load(mutants / name, name.split(".")[0])
    print(name)
    print("  scan, negative fee, no finding kept:  reference:", outcome(ref.scan, chain_fee), "| mutant:", outcome(mod.scan, chain_fee))
    print("  convexity, 2 strikes, df_ppm=0:       reference:", outcome(ref.convexity_violations, [100, 110], [5, 5], 0),
          "| mutant:", outcome(mod.convexity_violations, [100, 110], [5, 5], 0))
    print("  scan, 1 strike, 2 puts:               reference:", outcome(ref.scan, chain_1), "| mutant:", outcome(mod.scan, chain_1))
