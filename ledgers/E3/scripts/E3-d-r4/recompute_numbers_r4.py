"""Round-4 verifier (E3-d): independent recomputation of the numbers on project.html.

Written from the specification text (not from reference.py or the lab twins). Uses only the standard library.
Checks Lab 1 (CRRA and prospect CEs, probabilities, log-likelihood), Lab 2 (log contributions), Lab 3 (estimate, SEs,
score, mixed-sign count, prize range) and the exemplar prize facts.
"""
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
HALF = Fraction(1, 2)


def nearest_cent(x: float) -> int:
    return math.floor(x + 0.5)


# ---- Lab 1 -------------------------------------------------------------------------------------------------------------
G1, L1, K1, W1 = 0.40, 2.00, 1.50, 100_000


def crra_ce(prizes, probs, gamma, wealth):
    finals = [wealth + x for x in prizes]
    if gamma == 1.0:
        return math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, finals))) - wealth
    e = sum(float(p) * w ** (1.0 - gamma) for p, w in zip(probs, finals))
    return e ** (1.0 / (1.0 - gamma)) - wealth


def pros_value(x, gamma, lam):
    return float(x) ** (1.0 - gamma) if x >= 0 else -lam * float(-x) ** (1.0 - gamma)


def pros_ce(prizes, probs, gamma, lam):
    w = sum(float(p) * pros_value(x, gamma, lam) for x, p in zip(prizes, probs))
    return w ** (1.0 / (1.0 - gamma)) if w >= 0 else -((-w / lam) ** (1.0 / (1.0 - gamma)))


def logit_pa(ca, cb, kappa):
    return 1.0 / (1.0 + math.exp(-kappa * (ca - cb) / 10_000.0))


pairs1 = [
    ([2000, -1000], [HALF, HALF], [500], [Fraction(1)], "A"),
    ([3000], [Fraction(1)], [4000, -2000], [Fraction(1, 4), Fraction(3, 4)], "B"),
    ([1500, 2500], [Fraction(1, 3), Fraction(2, 3)], [-500, 3000], [HALF, HALF], "A"),
]
tot = 0.0
out1 = []
for pa, qa, pb, qb, ch in pairs1:
    cra = (nearest_cent(crra_ce(pa, qa, G1, W1)), nearest_cent(crra_ce(pb, qb, G1, W1)))
    pro = (nearest_cent(pros_ce(pa, qa, G1, L1)), nearest_cent(pros_ce(pb, qb, G1, L1)))
    p = logit_pa(pros_ce(pa, qa, G1, L1), pros_ce(pb, qb, G1, L1), K1)
    lp = math.log(p if ch == "A" else 1 - p)
    tot += lp
    out1.append((cra, pro, round(p, 6), round(lp, 6)))
print("LAB1 pairs (CRRA A,B; prospect A,B; P(A); log P(chosen)):")
for row in out1:
    print("  ", row)
print("  total log-likelihood:", f"{tot:.6f}")
ce_b2 = pros_ce([4000, -2000], [Fraction(1, 4), Fraction(3, 4)], G1, L1)
print("  prospect CE of pair-2 B (unrounded):", f"{ce_b2:.4f}", "rounded", nearest_cent(ce_b2))
print("  printed-sum check -0.733658 + -1.014598 + -0.554059 =", f"{-0.733658 - 1.014598 - 0.554059:.6f}")

# ---- Lab 2 -------------------------------------------------------------------------------------------------------------
z = 2.0 * (1500.0 - 2200.0) / 10_000.0
print("LAB2 z =", z, "| logA =", f"{-math.log1p(math.exp(-z)):.9f}", "| logB =", f"{-math.log1p(math.exp(z)):.9f}",
      "| sigmoid =", f"{1.0 / (1.0 + math.exp(-z)):.9f}")

# ---- Lab 3 -------------------------------------------------------------------------------------------------------------
src = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
block = re.search(r'<section class="lab" id="lab-E3-project-3".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', src, flags=re.S).group(1)
import html as _h
block = _h.unescape(block)
ns: dict = {}
ans_src = re.search(r"ANSWERS: list\[.*?\] = (\[.*?\n\])", block, flags=re.S).group(1)
ANSWERS = eval(ans_src, {})  # literal list of tuples, from the page's own data
print("LAB3 answers:", len(ANSWERS), "| prize min/max:", min(min(a[2] + a[4]) for a in ANSWERS), max(max(a[2] + a[4]) for a in ANSWERS))
sizes = sorted({len(a[2]) for a in ANSWERS} | {len(a[4]) for a in ANSWERS})
print("LAB3 lottery sizes:", sizes)


def mixed(prizes, probs_text):
    ps = [Fraction(s) for s in probs_text]
    return any(x > 0 and p > 0 for x, p in zip(prizes, ps)) and any(x < 0 and p > 0 for x, p in zip(prizes, ps))


mixed_ids = [a[0] for a in ANSWERS if mixed(a[2], a[3]) or mixed(a[4], a[5])]
print("LAB3 mixed pairs:", len(mixed_ids), mixed_ids, "| pure pairs:", [a[0] for a in ANSWERS if a[0] not in mixed_ids])


def ce(prizes, probs_text, gamma, lam):
    return pros_ce(prizes, [Fraction(s) for s in probs_text], gamma, lam)


def ll(xi):
    g = 1.0 / (1.0 + math.exp(-xi[0]))
    lam, kap = math.exp(xi[1]), math.exp(xi[2])
    t = 0.0
    for _, c, pa, qa, pb, qb in ANSWERS:
        z = kap * (ce(pa, qa, g, lam) - ce(pb, qb, g, lam)) / 10_000.0
        t += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return t


# Independent optimiser: coordinate-wise golden-section search, restarted from several starts, then a Newton polish
# with a fresh finite-difference Hessian at step 1e-4 (not the page's steps) to check the optimum is stable.
def golden(f, a, b, tol=1e-12):
    gr = (math.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    while abs(b - a) > tol:
        if f(c) > f(d):
            b = d
        else:
            a = c
        c, d = b - gr * (b - a), a + gr * (b - a)
    return (a + b) / 2


def coord_max(xi, sweeps=400):
    xi = list(xi)
    best = ll(xi)
    for _ in range(sweeps):
        for i in range(3):
            def f(v, i=i):
                t = list(xi)
                t[i] = v
                return ll(t)
            xi[i] = golden(f, xi[i] - 3.0, xi[i] + 3.0, tol=1e-11)
        new = ll(xi)
        if abs(new - best) < 1e-15:
            break
        best = new
    return xi


starts = [[math.log(g / (1 - g)), math.log(l), math.log(k)] for g in (0.2, 0.6, 0.85) for l in (1.0, 4.0) for k in (0.7, 3.0)]
cands = [coord_max(s) for s in starts]
xi_best = max(cands, key=ll)
spread = max(abs(ll(c) - ll(xi_best)) for c in cands)
print("LAB3 coordinate-search optimum: loglik", f"{ll(xi_best):.6f}", "| max loglik spread across starts", f"{spread:.2e}")
g_hat = 1.0 / (1.0 + math.exp(-xi_best[0]))
l_hat, k_hat = math.exp(xi_best[1]), math.exp(xi_best[2])
print("LAB3 gamma_hat", f"{g_hat:.4f}", "lambda_hat", f"{l_hat:.4f}", "kappa_hat", f"{k_hat:.4f}")


def hessian_neg(xi, h):
    n = 3
    H = [[0.0] * n for _ in range(n)]
    f0 = ll(xi)
    for i in range(n):
        for j in range(i, n):
            if i == j:
                up = list(xi); up[i] += h
                dn = list(xi); dn[i] -= h
                H[i][i] = -(ll(up) - 2 * f0 + ll(dn)) / (h * h)
            else:
                pp = list(xi); pp[i] += h; pp[j] += h
                pm = list(xi); pm[i] += h; pm[j] -= h
                mp = list(xi); mp[i] -= h; mp[j] += h
                mm = list(xi); mm[i] -= h; mm[j] -= h
                H[i][j] = H[j][i] = -(ll(pp) - ll(pm) - ll(mp) + ll(mm)) / (4 * h * h)
    return H


def inv3(M):
    A = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(M)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        d = A[c][c]
        A[c] = [x / d for x in A[c]]
        for r in range(3):
            if r != c:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [r[3:] for r in A]


for h in (1e-4, 1e-5):
    cov = inv3(hessian_neg(xi_best, h))
    se_g = g_hat * (1 - g_hat) * math.sqrt(cov[0][0])
    se_l = l_hat * math.sqrt(cov[1][1])
    se_k = k_hat * math.sqrt(cov[2][2])
    print(f"LAB3 SE at step {h:g}: se_gamma {se_g:.2f} se_lambda {se_l:.2f} se_kappa {se_k:.2f}")
hstep = 1e-5
score = max(abs((ll([x + (hstep if k == i else 0) for k, x in enumerate(xi_best)]) -
                 ll([x - (hstep if k == i else 0) for k, x in enumerate(xi_best)])) / (2 * hstep)) for i in range(3))
print("LAB3 largest score component (step 1e-5, my code):", f"{score:.2e}")
print("LAB3 log-likelihood at the estimate (my code):", f"{ll(xi_best):.4f}")

# ---- Exemplar B facts (prize range, pair 0 and pair 3 quoted on the page) -----------------------------------------
print("EXB pair 0 A prizes", ANSWERS[0][2], ANSWERS[0][3], "B prizes", ANSWERS[0][4], ANSWERS[0][5])
print("EXB pair 3 A prizes", ANSWERS[3][2], ANSWERS[3][3], "B prizes", ANSWERS[3][4], ANSWERS[3][5])
