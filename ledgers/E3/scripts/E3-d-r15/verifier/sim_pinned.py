import sys, math, random, json, time
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD15-E3-d/course/modules/E/E3/grader")
import reference as ref
from fractions import Fraction

def lottery(rng, mixed):
    count = rng.choice((2, 3))
    d = rng.choice((4, 5, 10, 20))
    cuts = sorted(rng.sample(range(1, d), count - 1))
    b = [0, *cuts, d]
    probs = [Fraction(b[k+1]-b[k], d) for k in range(count)]
    mags = [rng.randrange(500, 50001) for _ in range(count)]
    if mixed:
        signs = [1, -1, *(rng.choice((1, -1)) for _ in range(count-2))]
        rng.shuffle(signs)
    else:
        signs = [1]*count
    return [s*m for s, m in zip(signs, mags)], probs

def sim(seed, gamma, lam, kappa, n):
    rng = random.Random(seed)
    recs = []
    for i in range(n):
        pa, qa = lottery(rng, rng.random() < 0.6)
        ce_a = ref._prospect_ce(pa, qa, gamma, lam)
        cands = [lottery(rng, rng.random() < 0.6) for _ in range(30)]
        target = ce_a + rng.uniform(-5000, 5000)
        pb, qb = min(cands, key=lambda c: abs(ref._prospect_ce(c[0], c[1], gamma, lam) - target))
        ce_b = ref._prospect_ce(pb, qb, gamma, lam)
        z = kappa*(ce_a-ce_b)/10000.0
        p = 1/(1+math.exp(-z))
        choice = "A" if rng.random() < p else "B"
        recs.append({"pair_id": i, "choice": choice, "prizes_a": pa, "probs_a": [str(q) for q in qa], "prizes_b": pb, "probs_b": [str(q) for q in qb]})
    return recs

if __name__ == "__main__":
    gamma, lam, kappa, n, seed = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    recs = sim(seed, gamma, lam, kappa, n)
    t = time.time()
    try:
        r = ref.estimate(recs)
        print(f"g={gamma} l={lam} k={kappa} n={n} seed={seed} -> gamma_hat={r['gamma_hat']:.6f} lam={r['lambda_hat']:.4f} kap={r['kappa_hat']:.4f} seg={r['se_gamma']:.4g} t={time.time()-t:.1f}s")
    except Exception as e:
        print(f"g={gamma} l={lam} k={kappa} n={n} seed={seed} -> ERR {type(e).__name__}: {e} t={time.time()-t:.1f}s")
