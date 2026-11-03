"""Probe: the delta-method oracle at both steps for the alt2 estimate on seed 49 (verifier E3-e round 2 scratch)."""

import math

import test_project as t

est = t.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
print("alt2 estimate:", f"{gamma:.6f} {lam:.6f} {kappa:.6f}", "se:", f"{est['se_gamma']:.5f} {est['se_lambda']:.5f} {est['se_kappa']:.5f}")
for h in (1e-5, 1e-6):
    info = t._observed_information(theta, h)
    cov = t._invert3(info)
    diag = [cov[i][i] for i in range(3)]
    print(f"step {h:g}: inverse diagonal {['%.4g' % d for d in diag]}")
    if all(d > 0 for d in diag):
        want = [gamma * (1 - gamma) * math.sqrt(diag[0]), lam * math.sqrt(diag[1]), kappa * math.sqrt(diag[2])]
        print("   oracle se:", ["%.5f" % w for w in want])
    else:
        print("   oracle cannot take sqrt of a non-positive diagonal entry")
