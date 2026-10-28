"""Verifier round 2: seed-1093 Student-t failure and the unmatched-factor detection margin (seeds 0-1999).

Usage (from the checkout root): .venv/bin/python -I ledgers/M4/scripts/M4-d-r2/claims_r2.py
"""
import math, sys
sys.path.insert(0, "course/modules/M/M4/grader")
import reference as sol
from instance import make_instance
def sv(xs):
    m = math.fsum(xs)/len(xs); return math.fsum((x-m)**2 for x in xs)/(len(xs)-1)
# 1. seed 1093 claim
inst = make_instance(1093); pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
n=len(pos); tgt=math.fsum(pos[i]*pos[j]*cov[i][j] for i in range(n) for j in range(n))
t = sol.simulate_losses(pos, cov, nd, 1093, "student_t", nu)
print("seed1093 nu", nu, "rel err", abs(sv(t)/tgt-1), "tol 0.30")
# 2. unmatched inflation detection over seeds 0..1999 for nu 5..8 (a missing matched factor = scale sqrt(nu/W))
import random
miss = {}
for seed in range(0, 2000):
    inst = make_instance(seed); pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    if nu < 5: continue
    n=len(pos); tgt=math.fsum(pos[i]*pos[j]*cov[i][j] for i in range(n) for j in range(n))
    # unmatched: reference with matched factor removed: losses scaled by 1/sqrt(matched)
    m = (nu-2)/nu
    t = sol.simulate_losses(pos, cov, nd, seed, "student_t", nu)
    # reconstruct unmatched losses approximately is not exact (rounding); use exact scaling of unrounded instead
    d = miss.setdefault(nu, [0,0,1.0])
    d[0]+=1
    e = abs(sv(t)/(tgt*m)-1)  # unmatched variance equals matched sample var / m
    if e <= 0.30: d[1]+=1
    d[2]=min(d[2], e)
for nu,(tot,ok,mn) in sorted(miss.items()): print("nu",nu,"seeds",tot,"unmatched NOT caught (rel err<=0.30):",ok, "min rel err", round(mn,4))
