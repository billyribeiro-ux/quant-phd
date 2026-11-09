import sys, random, time
sys.path.insert(0, "/Users/billyribeiro/dev/quant-phd/ledgers/E3/scripts/E3-d-r15")
from sim_participants_r15 import sim
import reference as ref
rng = random.Random(int(sys.argv[2]))
trials = int(sys.argv[1])
res = []
for t in range(trials):
    g = rng.uniform(0.5, 0.999)
    l = rng.uniform(0.3, 6.0)
    k = rng.choice([0.5, 1.0, 2.0, 5.0, 10.0, 30.0])
    n = rng.choice([12, 16, 20, 26])
    seed = rng.randrange(10**6)
    recs = sim(seed, g, l, k, n)
    try:
        r = ref.estimate(recs)
    except Exception as e:
        continue
    res.append((r["gamma_hat"], g, l, k, n, seed, r["lambda_hat"], r["kappa_hat"]))
res.sort()
print("converged", len(res))
print("top 8 gamma_hat:")
for x in res[-8:]: print(x)
hi = [x for x in res if x[0] > 0.95]
print("count gamma_hat>0.95:", len(hi))
