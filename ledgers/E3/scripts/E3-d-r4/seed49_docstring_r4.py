"""Round-4 verifier (E3-d): re-derive the seed-49 numbers in test_project.py's docstring (lines 876-884).

Uses the suite's own oracle functions (imported from the pinned test file in a scratch copy, with the reference as elicit)
for the forward-order likelihood; the reverse-order variant is computed here with its own loop. Run as: python3 <this> <root>
"""
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
work = Path(tempfile.mkdtemp(prefix="e3d_r4_s49_"))
try:
    for f in ("test_project.py", "instance.py"):
        shutil.copy(ROOT / "course/modules/E/E3/grader" / f, work / f)
    shutil.copy(ROOT / "course/modules/E/E3/grader/reference.py", work / "elicit.py")
    os.environ["QF_SEED"] = "49"
    sys.path.insert(0, str(work))
    import elicit  # noqa: E402
    import test_project as tp  # noqa: E402

    est = elicit.estimate(json.loads(str(tp.INST["responses_json"])))
    g, lam, kap = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    theta = [math.log(g / (1 - g)), math.log(lam), math.log(kap)]
    for h in (1e-5, 1e-6):
        cov = tp._invert3(tp._observed_information(theta, h))
        se_g = g * (1 - g) * math.sqrt(cov[0][0])
        se_l = lam * math.sqrt(cov[1][1])
        print(f"forward order, step {h:g}: se_gamma {se_g:.5f}  se_lambda {se_l:.2f}")
    # Reverse-order summation of the likelihood terms (same terms, reversed order), central differences of the same steps.
    def ll_rev(t):
        gam = 1.0 / (1.0 + math.exp(-t[0]))
        la, ka = math.exp(t[1]), math.exp(t[2])
        total = 0.0
        for pa, qa, pb, qb, choice in reversed(tp.PARSED):
            z = ka * (tp.oracle_prospect(pa, qa, gam, la) - tp.oracle_prospect(pb, qb, gam, la)) / 10_000.0
            total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
        return total
    def info_rev(t, h):
        f0 = ll_rev(t)
        H = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            up = list(t); up[i] += h
            dn = list(t); dn[i] -= h
            H[i][i] = -(ll_rev(up) - 2 * f0 + ll_rev(dn)) / (h * h)
            for j in range(i + 1, 3):
                pp = list(t); pp[i] += h; pp[j] += h
                pm = list(t); pm[i] += h; pm[j] -= h
                mp = list(t); mp[i] -= h; mp[j] += h
                mm = list(t); mm[i] -= h; mm[j] -= h
                H[i][j] = H[j][i] = -(ll_rev(pp) - ll_rev(pm) - ll_rev(mp) + ll_rev(mm)) / (4 * h * h)
        return H
    for h in (1e-5, 1e-6):
        cov_f = tp._invert3(tp._observed_information(theta, h))
        cov_r = tp._invert3(info_rev(theta, h))
        f_l = lam * math.sqrt(cov_f[1][1]); r_l = lam * math.sqrt(cov_r[1][1])
        print(f"step {h:g}: reverse vs forward se_lambda {r_l:.2f} vs {f_l:.2f} ({100 * (r_l - f_l) / f_l:+.2f}%)")
    print("docstring claims: se_lambda 135.05 (1e-5), 97.67 (1e-6); se_gamma 0.09474 (1e-5), 0.07983 (1e-6);"
          " reverse +1.3% (135.05 to 136.78) and +0.4% (97.67 to 98.09); -27.7% and -15.7%")
    s1 = lam * math.sqrt(tp._invert3(tp._observed_information(theta, 1e-5))[1][1])
    s6 = lam * math.sqrt(tp._invert3(tp._observed_information(theta, 1e-6))[1][1])
    g5 = g * (1 - g) * math.sqrt(tp._invert3(tp._observed_information(theta, 1e-5))[0][0])
    g6 = g * (1 - g) * math.sqrt(tp._invert3(tp._observed_information(theta, 1e-6))[0][0])
    print(f"relative change of se_lambda from 1e-5 to 1e-6: {100 * (s6 - s1) / s1:+.2f}%; se_gamma: {100 * (g6 - g5) / g5:+.2f}%")
finally:
    shutil.rmtree(work, ignore_errors=True)
