import os, math, sys
os.environ["QF_SEED"] = "49"
sys.path.insert(0, "/tmp/e3e_r3/suite2")
import importlib
tp = importlib.import_module("test_project")
est = tp.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1 - gamma)), math.log(lam), math.log(kappa)]
fwd = list(tp.PARSED)
rev = list(reversed(fwd))
def ses(parsed, h):
    tp.PARSED = parsed
    cov = tp._invert3(tp._observed_information(theta, h))
    if not all(cov[i][i] > 0 for i in range(3)):
        return None
    return (gamma * (1 - gamma) * math.sqrt(cov[0][0]), lam * math.sqrt(cov[1][1]), kappa * math.sqrt(cov[2][2]))
print("estimate", gamma, lam, kappa, "reported", est["se_gamma"], est["se_lambda"], est["se_kappa"])
for h in (1e-5, 1e-6):
    f = ses(fwd, h); r = ses(rev, h)
    print("h", h, "forward", f, "\n     reverse", r)
    if f and r:
        print("   se_lambda change reverse vs forward: %.4f%%" % (100 * (r[1] - f[1]) / f[1]))
        print("   se_gamma  forward %.5f reverse %.5f" % (f[0], r[0]))
# reversal of the sum with math.fsum-free python sum: the oracle sums in order; check oracle_loglik itself
tp.PARSED = fwd
print("loglik fwd", tp.oracle_loglik(fwd, gamma, lam, kappa), "rev", tp.oracle_loglik(rev, gamma, lam, kappa))
