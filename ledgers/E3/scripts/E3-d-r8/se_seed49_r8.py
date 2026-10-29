# Verifier r8: recompute seed-49 SEs at steps 1e-5 and 1e-6, plus a reordered-sum log-likelihood, from the grader oracles.
import math, os, sys
sys.path.insert(0, os.getcwd())
os.environ["QF_SEED"] = "49"
import test_project as tp
import elicit as sol

est = sol.estimate(tp.RESPONSES)
g, lam, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
print("estimate", round(g, 4), round(lam, 4), round(k, 4), "SE", round(est["se_gamma"], 5), round(est["se_lambda"], 3), round(est["se_kappa"], 4))
theta = [math.log(g / (1 - g)), math.log(lam), math.log(k)]
ses = {}
for h in (1e-5, 1e-6):
    cov = tp._invert3(tp._observed_information(theta, h))
    ses[h] = (g * (1 - g) * math.sqrt(cov[0][0]), lam * math.sqrt(cov[1][1]), k * math.sqrt(cov[2][2]))
    print("oracle h=%g" % h, "se_gamma %.5f se_lambda %.2f se_kappa %.4f" % ses[h])
print("lambda change 1e-6 vs 1e-5: %.2f%%" % (100 * (ses[1e-6][1] / ses[1e-5][1] - 1)))
print("gamma change 1e-6 vs 1e-5: %.2f%%" % (100 * (ses[1e-6][0] / ses[1e-5][0] - 1)))

# Reordered summation: the same log-likelihood with the responses summed in reverse order.
def rev_loglik(gam, l, kap):
    total = 0.0
    for pa, qa, pb, qb, choice in reversed(tp.PARSED):
        z = kap * (tp.oracle_prospect(pa, qa, gam, l) - tp.oracle_prospect(pb, qb, gam, l)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total

def obs_info_with(f, theta, h):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves:
            y[idx] += amt
        return f(1.0 / (1.0 + math.exp(-y[0])), math.exp(y[1]), math.exp(y[2]))
    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            info[i][j] = info[j][i] = v
    return info

for h in (1e-5,):
    cov_f = tp._invert3(obs_info_with(tp.oracle_loglik.__wrapped__ if False else (lambda a, b, c: tp.oracle_loglik(tp.PARSED, a, b, c)), theta, h))
    cov_r = tp._invert3(obs_info_with(rev_loglik, theta, h))
    se_lam_f = lam * math.sqrt(cov_f[1][1]); se_lam_r = lam * math.sqrt(cov_r[1][1])
    print("order: forward %.4f reversed %.4f diff %.2f%%" % (se_lam_f, se_lam_r, 100 * (se_lam_r / se_lam_f - 1)))
