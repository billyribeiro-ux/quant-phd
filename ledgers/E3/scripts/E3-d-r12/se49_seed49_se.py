import math
import test_project as tp
fit = tp.est()
g, l, k = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]
for h in (1e-5, 1e-6):
    cov = tp._invert3(tp._observed_information(theta, h))
    se_g = g * (1 - g) * math.sqrt(cov[0][0]); se_l = l * math.sqrt(cov[1][1])
    print(f"h={h:g} se_gamma={se_g:.5f} se_lambda={se_l:.4f}")
print("gamma_hat", g, "lambda_hat", l, "kappa_hat", k)
