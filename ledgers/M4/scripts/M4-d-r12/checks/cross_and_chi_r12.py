"""Re-derive the cross-term and chi-square sharing numbers quoted in test_project.py (lines 43-47, 207-216) and in
project.html (lines 215, 228), over seeds 0-49 (verifier round 12). Reference solution used for the cross term."""
import importlib.util
import math
import random
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d")
G = ROOT / "course/modules/M/M4/grader"
spec = importlib.util.spec_from_file_location("ref", G / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
orig_chol = ref._cholesky


def var(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def cross_error(seed, eps, mod=None):
    w1 = w2 = 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    if eps is not None:
        def patched(c, n):
            f = orig_chol(c, n)
            f[1][0] = f[1][0] * (1 + eps)
            return f
        ref._cholesky = patched
    try:
        plus = ref.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
        minus = ref.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
    finally:
        ref._cholesky = orig_chol
    return (var(plus) - var(minus)) / target - 1


if "cross" in sys.argv:
    res = {}
    for eps in (None, 0.03, -0.03, 0.05, -0.05):
        res[eps] = [cross_error(s, eps) for s in range(50)]
        print("eps", eps, "fails(|n+eps|>0.05):", sum(1 for x in res[eps] if abs(x) > 0.05), flush=True)
    base = res[None]
    print("reference signed cross-term error over seeds 0-49: max", max(base), "min", min(base))
    print("reference max abs error", max(abs(x) for x in base))
    for eps in (0.03, -0.03, 0.05, -0.05):
        bad = [s for s, x in enumerate(res[eps]) if abs(x) > 0.05]
        print("eps", eps, "failing seeds", bad)
    print("reference failing seeds at tol 0.05:", [s for s, x in enumerate(base) if abs(x) > 0.05])


# ---- chi-square sharing probes (the check of test_student_t_draws_do_not_share_chi_square) ----
def sharing_losses(seed, group_of, n=40_000, nu=3):
    rng = random.Random(seed)
    chi = {}
    out = []
    for i in range(n):
        z = rng.gauss(0.0, 1.0)
        g = group_of(i)
        if g not in chi:
            chi[g] = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt((nu - 2) / chi[g])
        out.append(round(-(1_000_000 * scale * 0.02 * z)))
    return out


def fails(losses, n=40_000):
    mags = [abs(x) for x in losses]
    median = sorted(mags)[n // 2]
    above = [m > median for m in mags]
    for lag in (1, 2, 3):
        for offset in range(2 * lag):
            pairs = [(above[i], above[i + lag]) for i in range(offset, n - lag, 2 * lag)]
            share = sum(a and b for a, b in pairs) / len(pairs)
            se = math.sqrt(0.25 * 0.75 / len(pairs))
            if abs(share - 0.25) > 5 * se:
                return True
    return False


DESIGNS = {
    "independent": lambda i: i,
    "lag1_2k_2k+1": lambda i: ("s", i // 2),
    "lag2_4j_4j+2": lambda i: ("s", i // 4) if i % 4 in (0, 2) else ("o", i),
    "lag3_6j_6j+3": lambda i: ("s", i // 6) if i % 6 in (0, 3) else ("o", i),
    "even_all_one": lambda i: "even" if i % 2 == 0 else ("o", i),
    "chain4_4j_4j+4": lambda i: "chain" if i % 4 == 0 else ("o", i),
    "disjoint4_8k_8k+4": lambda i: ("p", i // 8) if i % 8 in (0, 4) else ("o", i),
}

if "chi" in sys.argv:
    for name, g in DESIGNS.items():
        f = [s for s in range(50) if fails(sharing_losses(s, g))]
        print(f"{name}: fails on {len(f)} of 50 seeds", flush=True)
