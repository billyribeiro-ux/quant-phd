import sys, random, time
sys.path.insert(0, "/Users/billyribeiro/dev/quant-phd/ledgers/E3/scripts/E3-d-r15")
from sim_participants_r15 import sim
import reference as ref
rng = random.Random(int(sys.argv[2]))
trials = int(sys.argv[1]); side = sys.argv[3]
res = []
t0=time.time()
for t in range(trials):
    g = rng.choice([rng.uniform(0.9, 0.999), rng.uniform(0.001, 0.05), rng.uniform(0.05, 0.9)])
    l = rng.choice([rng.uniform(0.3, 3.0), rng.uniform(3.0, 12.0)])
    k = rng.choice([0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 100.0])
    n = rng.choice([12, 16, 20, 26])
    seed = rng.randrange(10**6)
    recs = sim(seed, g, l, k, n)
    try:
        r = ref.estimate(recs)
    except Exception as e:
        continue
    gh = r["gamma_hat"]
    if (side=="HIGH" and gh > 0.999) or (side=="LOW" and gh < 0.001):
        res.append((gh, g, l, k, n, seed, r["lambda_hat"], r["kappa_hat"], r["se_gamma"], r["se_lambda"], r["se_kappa"]))
print(side, "hits", len(res), "time", round(time.time()-t0))
for x in res: print(x)
