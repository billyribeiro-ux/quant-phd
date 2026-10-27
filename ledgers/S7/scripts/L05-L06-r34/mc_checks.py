"""Round-34 Monte Carlo and quadrature checks for S7 L05-L06 (verifier-written; seeds stated).

1. Proposition 3.2 (L06): independent K = 36 p-values: P(min <= 0.05) vs 1-(1-alpha)^K, mean of min vs 1/(K+1),
   and dependent (equicorrelated normal) FWER inside [alpha, min(1, K alpha)]. Tolerance: 6 standard errors.
2. Lemma 7.6 (L05): P(union) <= t * sum (beta_l - beta_{l-1})/l for random valid dependent p-values, 6 SE.
3. Definition 6.6 / line 499 (L05): FCR = E[V/max(R,1)] <= alpha for a Bonferroni simultaneous band and several
   selection rules, 6 SE (the page states no tolerance; six standard errors used, as the coordinator asked).
4. L06 bracket 3.7760-3.7928 at M = 316, alpha = 5%, from the two sides of the Mills-ratio bounds (Lemma 2.2),
   solved by root finding.
5. L05 reversal sentence (max(X,-X) = |X|): quantile 1.960 by Monte Carlo.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/mc_checks.py
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize
from scipy.stats import norm

rng = np.random.default_rng(34)
SIX = 6.0
lines: list[str] = []


def report(label: str, ok: bool, detail: str) -> None:
    lines.append(f"{'OK      ' if ok else 'FAILED  '} {label}: {detail}")


# 1. Proposition 3.2
alpha, K, n = 0.05, 36, 200_000
p = rng.random((n, K))
pmin = p.min(axis=1)
est = float(np.mean(pmin <= alpha))
exact = 1 - (1 - alpha) ** K
se = math.sqrt(exact * (1 - exact) / n)
report("Prop3.2 iid P(min<=alpha), K=36", abs(est - exact) <= SIX * se, f"MC {est:.5f} vs {exact:.5f}, SE {se:.5f}")
mean_est = float(pmin.mean())
mean_exact = 1 / (K + 1)
se_m = float(pmin.std(ddof=1) / math.sqrt(n))
report("Prop3.2 iid mean of min = 1/(K+1)", abs(mean_est - mean_exact) <= SIX * se_m, f"MC {mean_est:.6f} vs {mean_exact:.6f}, SE {se_m:.6f}")
for rho in (0.0, 0.5, 0.9, 0.99):
    z = math.sqrt(rho) * rng.standard_normal((n, 1)) + math.sqrt(1 - rho) * rng.standard_normal((n, K))
    pv = 2 * norm.sf(np.abs(z))
    f = float(np.mean(pv.min(axis=1) <= alpha))
    lo, hi = alpha, min(1.0, K * alpha)
    s = math.sqrt(f * (1 - f) / n)
    ok = (lo - SIX * s <= f <= hi + SIX * s)
    report(f"Prop3.2 dependent FWER rho={rho}", ok, f"MC {f:.4f} (SE {s:.4f}) in [{lo:.2f}, {hi:.2f}]")

# 2. Lemma 7.6: P(union_l {p_(l) <= beta_l}) <= t * sum_l (beta_l - beta_{l-1}) / l
def lemma_case(t: int, M: int, beta: np.ndarray, rho: float, n_draws: int) -> tuple[float, float, float]:
    z = math.sqrt(rho) * rng.standard_normal((n_draws, 1)) + math.sqrt(1 - rho) * rng.standard_normal((n_draws, t))
    pv = norm.sf(z)  # valid p-values under the null (uniform marginally)
    ps = np.sort(pv, axis=1)[:, :M]
    hit = np.any(ps <= beta[None, 1:], axis=1)
    f = float(hit.mean())
    rhs = t * float(np.sum(np.diff(beta) / np.arange(1, M + 1)))
    return f, rhs, math.sqrt(f * (1 - f) / n_draws)


worst = -1e9
for case in range(40):
    t = int(rng.integers(1, 12))
    M = int(rng.integers(1, t + 1))
    raw = np.sort(rng.random(M))
    beta = np.concatenate([[0.0], raw])
    rho = float(rng.choice([0.0, 0.3, 0.8]))
    f, rhs, s = lemma_case(t, M, beta, rho, 100_000)
    worst = max(worst, f - rhs)
    if f > min(rhs, 1.0) + SIX * s and rhs < 1.0:
        report(f"Lemma7.6 case {case}", False, f"LHS {f:.4f} > RHS {rhs:.4f}")
report("Lemma7.6 random cases (40, 100k draws, t<=11, rho in {0,.3,.8})", worst <= 6 * 0.002 + 1e-12, f"largest LHS-RHS over cases {worst:.5f}; any case with RHS<1 and LHS > RHS + 6 SE would be listed above")
t_h, M_h = 20, 20
beta_h = np.array([0.0] + [l * 0.05 / t_h for l in range(1, M_h + 1)])
f, rhs, s = lemma_case(t_h, M_h, beta_h, 0.0, 200_000)
report("Lemma7.6 Hommel case t=M=20, beta_l = l*alpha/t", f <= rhs + 6 * s, f"LHS {f:.5f} <= RHS {rhs:.5f} (exact RHS = alpha*H_20 = {0.05 * sum(1 / l for l in range(1, 21)):.5f}); SE {s:.5f}")

# 3. FCR of a simultaneous band restricted to a selection (Definition 6.6, line 499)
K3, n3, a3 = 20, 200_000, 0.05
c = norm.ppf(1 - a3 / (2 * K3))
mu = np.zeros(K3)
mu[:8] = 3.0
z = mu + rng.standard_normal((n3, K3))
miss = np.abs(z - mu) > c  # interval z +/- c misses mu_k
for name, select in (
    ("R largest |z|, R=1", lambda zz: np.argsort(-np.abs(zz), axis=1)[:, :1]),
    ("R largest |z|, R=3", lambda zz: np.argsort(-np.abs(zz), axis=1)[:, :3]),
    ("R largest |z|, R=10", lambda zz: np.argsort(-np.abs(zz), axis=1)[:, :10]),
    ("R largest |z|, R=20", lambda zz: np.argsort(-np.abs(zz), axis=1)[:, :20]),
):
    sel = select(z)
    R = np.full(n3, sel.shape[1], dtype=float)
    V = np.take_along_axis(miss, sel, axis=1).sum(axis=1)
    ratio = V / np.maximum(R, 1)
    fcr = float(ratio.mean())
    s = float(ratio.std(ddof=1) / math.sqrt(n3))
    report(f"FCR band selection {name}", fcr <= a3 + SIX * s, f"FCR {fcr:.5f} vs alpha {a3}; SE {s:.5f}; P(V>=1) {float(np.mean(V >= 1)):.5f}")

# 4. Bracket of the Mills-ratio bounds at M = 316, alpha = 0.05 (line 95 of L06)
M4 = 316
q = 0.05 / (2 * M4)
phi = norm.pdf
t_hi = optimize.brentq(lambda x: phi(x) / x - q, 1.0, 10.0, xtol=1e-14)  # right bound: Q(x) <= phi(x)/x
t_lo = optimize.brentq(lambda x: phi(x) * x / (1 + x * x) - q, 1.0, 10.0, xtol=1e-14)  # left: Q(x) >= x phi/(1+x^2)
t_exact = norm.ppf(1 - q)
report("L06 line 95 t* from (1)", abs(round(t_exact, 4) - 3.7778) < 1e-9, f"Phi^-1(1-0.05/632) = {t_exact:.10f}")
report("L06 line 95 bracket lower root", round(t_lo, 4) == 3.7760, f"{t_lo:.10f} -> {t_lo:.4f} (page 3.7760)")
report("L06 line 95 bracket upper root", round(t_hi, 4) == 3.7928, f"{t_hi:.10f} -> {t_hi:.4f} (page 3.7928)")

# 5. Reversal: 95% quantile of max(X, -X) = |X| (X ~ N(0,1))
x = rng.standard_normal(4_000_000)
qmc = float(np.quantile(np.maximum(x, -x), 0.95))
se5 = math.sqrt(0.95 * 0.05 / x.size) / float(norm.pdf(norm.ppf(0.975)) / 1.0) / 1.0
report("reversal: 95% quantile of max(X,-X) ~ 1.960", abs(qmc - 1.960) <= 6 * 0.0003, f"MC {qmc:.4f} vs 1.9600 (tolerance 6 x 0.0003 quantile SE approx)")

print("\n".join(lines))
print("failures:", sum(1 for ln in lines if ln.startswith("FAILED")))
