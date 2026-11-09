"""Probe one-strike boundary behaviour of the round-17 mutants and the reference (verifier round 17)."""
import importlib.util
import sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ROOT = sys.argv[1]
paths = {
    "reference": f"{ROOT}/course/modules/FC/FC2/grader/reference.py",
    "r17_a": f"{ROOT}/ledgers/FC2/mutants/r17_a_convexity_one_strike_returns_before_validation.py",
    "r17_b": f"{ROOT}/ledgers/FC2/mutants/r17_b_scan_skips_df_check_for_one_strike_chain.py",
    "r17_c": f"{ROOT}/ledgers/FC2/mutants/r17_c_convexity_skips_length_check_for_one_strike.py",
}

def outcome(fn):
    try:
        return "returned " + repr(fn())
    except ValueError as e:
        return "ValueError: " + str(e)

for name, path in paths.items():
    m = load(path, "m_" + name.replace("-", "_"))
    chain = {"spot_cents": 100, "df_ppm": 0, "strikes_cents": [100], "call_cents": [5], "put_cents": [1],
             "cost": {"fee_cents_per_contract": 0, "half_spread_cents": 0}}
    print(name)
    print("  convexity_violations([100],[5],df=0):", outcome(lambda: m.convexity_violations([100], [5], 0)))
    print("  convexity_violations([100],[5,5],PPM):", outcome(lambda: m.convexity_violations([100], [5, 5], 1_000_000)))
    print("  convexity_violations([0],[5],PPM):", outcome(lambda: m.convexity_violations([0], [5], 1_000_000)))
    print("  scan(one strike, df=0):", outcome(lambda: m.scan(chain)))
