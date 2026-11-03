"""Round-4 verifier (E3-d): sample instance validity over seeds (20 sampled seeds; parameter spread for seeds 0-49).

For seeds 0, 3, 7, 11, 19, 23, 31, 37, 42, 49 and 4 more (20 total), checks: probabilities are exact, positive, sum to 1;
prizes are whole cents within 500-50000 magnitude; 2-3 prizes; at least 100 of 200 pairs mixed; the answers differ.
Also lists the true kappa of every seed 0-49 (for the mutant design).
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
from instance import make_instance  # noqa: E402

SAMPLE = [0, 3, 7, 11, 19, 23, 31, 37, 42, 49, 1, 2, 5, 8, 13, 17, 26, 33, 40, 45]
rows = []
for seed in SAMPLE:
    inst = make_instance(seed)
    recs = json.loads(inst["responses_json"])
    ok = True
    mixed = 0
    for r in recs:
        for prizes, probs in ((r["prizes_a"], r["probs_a"]), (r["prizes_b"], r["probs_b"])):
            qs = [Fraction(s) for s in probs]
            ok &= len(prizes) in (2, 3) and len(prizes) == len(qs)
            ok &= all(isinstance(x, int) and 500 <= abs(x) <= 50000 for x in prizes)
            ok &= all(q > 0 for q in qs) and sum(qs) == 1
        a = any(x > 0 and Fraction(p) > 0 for x, p in zip(r["prizes_a"], r["probs_a"]))
        b = any(x < 0 and Fraction(p) > 0 for x, p in zip(r["prizes_a"], r["probs_a"]))
        c = any(x > 0 and Fraction(p) > 0 for x, p in zip(r["prizes_b"], r["probs_b"]))
        d = any(x < 0 and Fraction(p) > 0 for x, p in zip(r["prizes_b"], r["probs_b"]))
        mixed += (a and b) or (c and d)
    choices = "".join(r["choice"] for r in recs)
    ok &= len(recs) == 200 and mixed >= 100
    rows.append((seed, inst["gamma"], inst["lambda"], inst["kappa"], inst["wealth_cents"], len(recs), mixed,
                 choices.count("A"), ok))
print("seed gamma lambda kappa wealth n mixed nA valid")
for row in rows:
    print(*row)
print("all sampled instances valid:", all(r[-1] for r in rows))
print("distinct (gamma,lambda,kappa) among sample:", len({(r[1], r[2], r[3]) for r in rows}), "of", len(rows))
print("distinct answer strings among sample:", len({make_instance(s)["responses_json"] for s in SAMPLE}), "of", len(SAMPLE))
kap = {s: make_instance(s)["kappa"] for s in range(50)}
print("seeds 0-49 with kappa < 1:", sorted(s for s, k in kap.items() if k < 1.0))
print("count kappa<1 among 0-49:", sum(1 for k in kap.values() if k < 1.0))
print("count kappa<1 among seeds 0-9:", sum(1 for s in range(10) if kap[s] < 1.0))
