# Recomputes the seed-49 standard errors quoted in the grader docstring (test_project.py lines 924-928), with own code.
import json, math, sys
from fractions import Fraction as F
G = "/Users/billyribeiro/.fanout/wt/verifyD6-E3-e/course/modules/E/E3/grader"
sys.path.insert(0, G)
from instance import make_instance
import reference as ref  # the course reference engine, used only to obtain the estimate
inst = make_instance(49)
resp = json.loads(str(inst["responses_json"]))
rows = []
for r in resp:
    rows.append(([int(x) for x in r["prizes_a"]], [F(s) for s in r["probs_a"]], [int(x) for x in r["prizes_b"]], [F(s) for s in r["probs_b"]], r["choice"]))
est = ref.estimate(resp)
gh, lh, kh = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
print("estimate", gh, lh, kh)
def v(x, g, l):
    return math.pow(x, 1-g) if x >= 0 else -l*math.pow(-x, 1-g)
def ce(pr, qr, g, l):
    t = sum(float(p)*v(x, g, l) for x, p in zip(pr, qr))
    return math.pow(t, 1/(1-g)) if t >= 0 else -math.pow(-t/l, 1/(1-g))
def ll(th, order):
    g = 1/(1+math.exp(-th[0])); l = math.exp(th[1]); k = math.exp(th[2])
    terms = []
    for pa, qa, pb, qb, c in rows:
        z = k*(ce(pa,qa,g,l)-ce(pb,qb,g,l))/10000.0
        terms.append(-math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z)))
    if order == "rev": terms = terms[::-1]
    return math.fsum(terms) if order == "fsum" else sum(terms)
def se(h, order="fwd"):
    th = [math.log(gh/(1-gh)), math.log(lh), math.log(kh)]
    f0 = ll(th, order)
    H = [[0.0]*3 for _ in range(3)]
    def at(*moves):
        y = list(th)
        for i, a in moves: y[i] += a
        return ll(y, order)
    for i in range(3):
        H[i][i] = -(at((i,h)) - 2*f0 + at((i,-h)))/(h*h)
    for i in range(3):
        for j in range(i+1,3):
            val = -(at((i,h),(j,h)) - at((i,h),(j,-h)) - at((i,-h),(j,h)) + at((i,-h),(j,-h)))/(4*h*h)
            H[i][j] = H[j][i] = val
    # invert 3x3 via cofactors
    a = H
    det = (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0]) + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    inv = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            minor = [[a[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            cof = (minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]) * (-1 if (i+j) % 2 else 1)
            inv[j][i] = cof/det
    g = gh; l = lh; k = kh
    return (g*(1-g)*math.sqrt(inv[0][0]), l*math.sqrt(inv[1][1]), k*math.sqrt(inv[2][2]))
for h in (1e-5, 1e-6):
    for order in ("fwd", "rev"):
        s = se(h, order)
        print("step", h, "order", order, "se_gamma %.5f se_lambda %.2f se_kappa %.4f" % s)
s5 = se(1e-5); s6 = se(1e-6); r5 = se(1e-5,"rev"); r6 = se(1e-6,"rev")
print("lambda se step1e-5 -> 1e-6 change %.1f%%" % (100*(s6[1]-s5[1])/s5[1]))
print("gamma se step1e-5 -> 1e-6 change %.1f%%" % (100*(s6[0]-s5[0])/s5[0]))
print("reverse-order change at 1e-5 for lambda %.1f%%, at 1e-6 %.1f%%" % (100*(r5[1]-s5[1])/s5[1], 100*(r6[1]-s6[1])/s6[1]))
