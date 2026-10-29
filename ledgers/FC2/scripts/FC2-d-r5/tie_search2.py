"""Round 5 FC2-d: exhaustive-by-residue search for exact half-cent parity ties (K*df/1e6 has fraction 1/2) where the
float mutant disagrees with the exact reference. Gap = C - P - (S - K df) with C=P=0, S=0 gives gap = K df."""
import importlib.util, math
from fractions import Fraction
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/course/modules/FC/FC2/grader/reference.py", "ref")
mut = load("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/ledgers/FC2/mutants/r5_a_float_discount_ties.py", "mut")
PPM = 10**6
hits = []; tested = 0
for K in range(1, 400):
    g = math.gcd(K, PPM)
    if 500000 % g: continue
    mod = PPM // g
    d0 = (500000 // g) * pow(K // g, -1, mod) % mod if math.gcd(K // g, mod) == 1 else None
    if d0 is None: continue
    for df in range(d0, 1_000_001, mod):
        if not (1 <= df <= PPM): continue
        tested += 1
        a = ref.parity_gap_cents(0, 0, 0, K, df); b = mut.parity_gap_cents(0, 0, 0, K, df)
        if a != b: hits.append((df, K, a, b))
print("tie cases tested:", tested, "mismatches:", len(hits))
for h in hits[:6]: print("df_ppm, strike, ref, mutant =", h)
