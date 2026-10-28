import sys, random, math
sys.path.insert(0, "/tmp/cf1-v/c17")
import l06_lib as L
rng = random.Random(L.SEED)
npvs = [L.npv_of([rng.randint(L.LOW, L.HIGH) for _ in range(L.YEARS)]) for _ in range(L.N_MAX)]
print("exact_zero_draws", sum(1 for x in npvs if x == 0), "min_abs_npv_cents", min(abs(x) for x in npvs))
