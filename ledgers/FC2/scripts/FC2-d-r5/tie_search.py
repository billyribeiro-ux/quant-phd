"""Round 5 FC2-d: search exact half-cent parity ties where the float mutant differs from the exact reference."""
import importlib.util
from fractions import Fraction
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/course/modules/FC/FC2/grader/reference.py", "ref")
mut = load("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/ledgers/FC2/mutants/r5_a_float_discount_ties.py", "mut")
hits = []
for df in (950000, 930000, 970000, 990000, 960000, 940000, 980000, 920000, 910000, 850000, 750000, 870000):
    for K in range(1, 400):
        x = Fraction(K * df, 10**6)
        if (2 * x).denominator == 1 and (2 * x).numerator % 2 == 1 or True:
            # gap = C - P - (S - K df) with C=P=0 and S = 0 gives gap = K df; use S chosen so gap = k + 1/2 exactly
            for base in (0,):
                g = Fraction(0) - (Fraction(0) - x)  # = x
                if (2 * g).denominator == 1 and (2 * g).numerator % 2 == 1:
                    a = ref.parity_gap_cents(0, 0, 0, K, df)
                    b = mut.parity_gap_cents(0, 0, 0, K, df)
                    if a != b:
                        hits.append((df, K, a, b))
print("mismatches:", len(hits))
for h in hits[:8]: print("df_ppm, strike, ref, mutant =", h)
