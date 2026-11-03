import json, math, sys
sys.path.insert(0, '.')
import elicit as sol
from instance import make_instance
import test_project as tp  # imports elicit + instance; SEED from env QF_SEED
inst = make_instance(49)
resp = json.loads(str(inst["responses_json"]))
fit = sol.estimate(resp)
print("seed49 estimate", {k: round(v, 6) for k, v in fit.items()})
parsed = [tp.parse(r) for r in resp]
gamma, lam, kappa = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
theta = [math.log(gamma / (1 - gamma)), math.log(lam), math.log(kappa)]
for h in (1e-5, 1e-6):
    cov = tp._invert3(tp._observed_information(theta, h))
    se = (gamma * (1 - gamma) * math.sqrt(cov[0][0]), lam * math.sqrt(cov[1][1]), kappa * math.sqrt(cov[2][2]))
    print("step", h, "se_gamma %.5f se_lambda %.3f se_kappa %.4f" % se)
# evaluation order: reverse the response order in the likelihood sum
rev = list(reversed(parsed))
def ll_rev(t):
    g = 1 / (1 + math.exp(-t[0]))
    return tp.oracle_loglik(rev, g, math.exp(t[1]), math.exp(t[2]))
def info_rev(theta, h):
    f0 = ll_rev(theta)
    info = [[0.0]*3 for _ in range(3)]
    def at(*moves):
        y = list(theta)
        for idx, a in moves: y[idx] += a
        return ll_rev(y)
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2*f0 + at((i, -h))) / (h*h)
        for j in range(i+1, 3):
            v = -(at((i,h),(j,h)) - at((i,h),(j,-h)) - at((i,-h),(j,h)) + at((i,-h),(j,-h))) / (4*h*h)
            info[i][j] = info[j][i] = v
    return info
for h in (1e-5, 1e-6):
    cov = tp._invert3(info_rev(theta, h))
    print("reversed order step", h, "se_lambda %.3f" % (lam * math.sqrt(cov[1][1])), "se_gamma %.5f" % (gamma*(1-gamma)*math.sqrt(cov[0][0])))
