import sys, json, math
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import elicit as sol
import test_project as tp
from instance import make_instance

def obs_info(parsed, theta, h):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves:
            y[idx] += amt
        g = 1.0/(1.0+math.exp(-y[0]))
        return tp.oracle_loglik(parsed, g, math.exp(y[1]), math.exp(y[2]))
    f0 = at()
    info = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i,h)) - 2*f0 + at((i,-h)))/(h*h)
        for j in range(i+1,3):
            v = -(at((i,h),(j,h)) - at((i,h),(j,-h)) - at((i,-h),(j,h)) + at((i,-h),(j,-h)))/(4*h*h)
            info[i][j] = info[j][i] = v
    return info

def se_oracle(parsed, est, h):
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    theta = [math.log(g/(1-g)), math.log(l), math.log(k)]
    info = obs_info(parsed, theta, h)
    cov = tp._invert3(info)
    diag = [cov[i][i] for i in range(3)]
    out = {}
    out["diag_cov"] = [round(x, 6) for x in diag]
    if diag[0] > 0: out["se_gamma"] = round(g*(1-g)*math.sqrt(diag[0]), 5)
    if diag[1] > 0: out["se_lambda"] = round(l*math.sqrt(diag[1]), 3)
    if diag[2] > 0: out["se_kappa"] = round(k*math.sqrt(diag[2]), 4)
    return out

inst49 = make_instance(49)
r49 = json.loads(inst49["responses_json"])
p49 = [tp.parse(r) for r in r49]
est = sol.estimate(r49)
print("ref est49", est)
for h in (1e-5, 1e-6):
    print("fwd h", h, se_oracle(p49, est, h))
    print("rev h", h, se_oracle(list(reversed(p49)), est, h))
# also the 'is the ref estimate a maximum' via test helper with parsed
print("score49 1e-5/1e-6", tp._largest_score_component(p49, est["gamma_hat"], est["lambda_hat"], est["kappa_hat"], 1e-5), tp._largest_score_component(p49, est["gamma_hat"], est["lambda_hat"], est["kappa_hat"], 1e-6))
# derivative-factor mutation claim: missing factor on SE at seed 0 and seed 49
for label, pr, e in (("seed49", p49, est),):
    for h in (1e-5,1e-6):
        g,l,k = e["gamma_hat"], e["lambda_hat"], e["kappa_hat"]
        theta=[math.log(g/(1-g)), math.log(l), math.log(k)]
        cov=tp._invert3(obs_info(pr,theta,h))
        se_g=g*(1-g)*math.sqrt(cov[0][0]); se_l=l*math.sqrt(cov[1][1]); se_k=k*math.sqrt(cov[2][2])
        print(label,h,"missing gamma(1-gamma) factor ratio", math.sqrt(cov[0][0])/se_g, "missing lambda factor ratio", math.sqrt(cov[1][1])/ (se_l/l), "missing kappa", math.sqrt(cov[2][2])/(se_k/k))
