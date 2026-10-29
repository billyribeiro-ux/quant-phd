# Round-10: reproduce the seed-49 standard-error numbers quoted in test_standard_errors_match_the_delta_method_oracle.
import math
import sys

sys.path.insert(0, sys.argv[1])
import test_project as t  # noqa: E402

est = t.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
out = {}
for label, order in (("forward", t.PARSED), ("reversed", t.PARSED[::-1])):
    t.PARSED = order
    for h in (1e-5, 1e-6):
        cov = t._invert3(t._observed_information(theta, h))
        out[(label, h)] = (
            gamma * (1.0 - gamma) * math.sqrt(cov[0][0]),
            lam * math.sqrt(cov[1][1]),
            kappa * math.sqrt(cov[2][2]),
        )
    t.PARSED = t.PARSED  # no-op
for k, v in out.items():
    print(k, "se_gamma %.5f se_lambda %.2f se_kappa %.4f" % v)
a, b = out[("forward", 1e-5)][1], out[("forward", 1e-6)][1]
print("lambda SE change 1e-5 -> 1e-6: %.2f%%" % (100 * (b - a) / a))
print("gamma SE change 1e-5 -> 1e-6: %.2f%%" % (100 * (out[("forward", 1e-6)][0] - out[("forward", 1e-5)][0]) / out[("forward", 1e-5)][0]))
print("order effect on lambda SE at 1e-5: %.2f%%" % (100 * (out[("reversed", 1e-5)][1] - a) / a))
print("order effect on lambda SE at 1e-6: %.2f%%" % (100 * (out[("reversed", 1e-6)][1] - b) / b))
print("gamma_hat", gamma, "lambda_hat", lam, "kappa_hat", kappa, "seed", t.SEED)
