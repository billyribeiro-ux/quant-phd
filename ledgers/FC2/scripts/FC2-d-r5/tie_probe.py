"""Round 5 FC2-d: exact half-cent ties at df = 950000 (K*0.95 has fraction .5 when K = 110), reference vs float mutant."""
import importlib.util, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/course/modules/FC/FC2/grader/reference.py", "ref")
mut = load("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/ledgers/FC2/mutants/r5_a_float_discount_ties.py", "mut")
print("parity_gap_cents(0,0,0,110,950000): ref", ref.parity_gap_cents(0, 0, 0, 110, 950000), "mutant", mut.parity_gap_cents(0, 0, 0, 110, 950000), "exact gap = 104.5 -> expected 105")
print("parity_gap_cents(0,0,0,30,950000)  : ref", ref.parity_gap_cents(0, 0, 0, 30, 950000), "mutant", mut.parity_gap_cents(0, 0, 0, 30, 950000), "exact gap = 28.5 -> expected 29")
chain = {"spot_cents": 0, "df_ppm": 950000, "strikes_cents": [110], "call_cents": [0], "put_cents": [0], "cost": {"fee_cents_per_contract": 0, "half_spread_cents": 0}}
print("scan gross, ref:", [f["gross_cents"] for f in ref.scan(chain)], "mutant:", [f["gross_cents"] for f in mut.scan(chain)])
