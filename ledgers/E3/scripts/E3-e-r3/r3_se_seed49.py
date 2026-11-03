"""Round 3 check: the seed-49 standard-error numbers in the test_standard_errors docstring, recomputed with the suite's own oracle."""
import math, os, sys
os.environ["QF_SEED"] = "49"
sys.path.insert(0, os.getcwd())
import test_project as tp  # imports elicit (= reference copy) and instance
est = tp.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
print("estimate:", gamma, lam, kappa, "se (reference):", est["se_gamma"], est["se_lambda"], est["se_kappa"])
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
fwd = tp.PARSED
rev = list(reversed(fwd))
def se_at(parsed, h):
    tp.PARSED = parsed
    cov = tp._invert3(tp._observed_information(theta, h))
    return gamma * (1 - gamma) * math.sqrt(cov[0][0]), lam * math.sqrt(cov[1][1]), kappa * math.sqrt(cov[2][2])
out = {}
for h in (1e-5, 1e-6):
    f = se_at(fwd, h); r = se_at(rev, h)
    print(f"step {h:g}: forward se_gamma={f[0]:.5f} se_lambda={f[1]:.3f} se_kappa={f[2]:.5f} | reverse se_gamma={r[0]:.5f} se_lambda={r[1]:.3f} se_kappa={r[2]:.5f}")
    print(f"   reverse vs forward, % change: gamma {100*(r[0]/f[0]-1):+.2f}  lambda {100*(r[1]/f[1]-1):+.2f}  kappa {100*(r[2]/f[2]-1):+.2f}")
tp.PARSED = fwd
print("lambda change 1e-6 vs 1e-5 (forward), %:", f"{100*(se_at(fwd,1e-6)[1]/se_at(fwd,1e-5)[1]-1):+.2f}")
print("gamma change 1e-6 vs 1e-5 (forward), %:", f"{100*(se_at(fwd,1e-6)[0]/se_at(fwd,1e-5)[0]-1):+.2f}")
