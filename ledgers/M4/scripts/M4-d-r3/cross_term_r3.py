"""Round-3 verifier D (M4 slice d): re-derive the cross-term claims in test_project.py (lines 43-48) and project.html.

Setup exactly as test_student_t_cross_term_matches_matched_covariance: w1 = w2 = 1e6, cov [[4e-4, 4.8e-4], [4.8e-4, 9e-4]],
nu = 5, 100,000 draws, target = 4 w1 w2 cov12. Seeds 0..49 for the reference (the suite's own claim), and seeds 0..9 for
the two variants the comment names: (a) the matched factor applied to asset 1 only; (b) one chi-square variable per asset.
Usage: python -I cross_term_r3.py <checkout_root>
"""
import importlib.util
import math
import random
import sys

root = sys.argv[1]
spec = importlib.util.spec_from_file_location("ref", root + "/course/modules/M/M4/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

W1, W2 = 1_000_000, 1_000_000
COV = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
NU, DRAWS = 5, 100_000
TARGET = 4.0 * W1 * W2 * COV[0][1]


def sv(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def cross_error(sim):
    plus = sim([W1, W2])
    minus = sim([W1, -W2])
    measured = sv(plus) - sv(minus)
    return measured / TARGET - 1.0


def variant_matched_one_asset(seed):
    # Asset 1 carries the matched factor; asset 2 is scaled by sqrt(nu / W) only (no matched factor).
    def sim(pos):
        factor = ref._cholesky(COV, 2)
        rng = random.Random(seed)
        matched = (NU - 2) / NU
        losses = []
        for _ in range(DRAWS):
            z = [rng.gauss(0.0, 1.0) for _ in range(2)]
            chi = rng.gammavariate(NU / 2, 2.0)
            r1 = math.sqrt(matched * NU / chi) * factor[0][0] * z[0]
            r2 = math.sqrt(NU / chi) * (factor[1][0] * z[0] + factor[1][1] * z[1])
            losses.append(round(-(pos[0] * r1 + pos[1] * r2)))
        return losses
    return sim


def variant_chi_per_asset(seed):
    def sim(pos):
        factor = ref._cholesky(COV, 2)
        rng = random.Random(seed)
        matched = (NU - 2) / NU
        losses = []
        for _ in range(DRAWS):
            z = [rng.gauss(0.0, 1.0) for _ in range(2)]
            chi1 = rng.gammavariate(NU / 2, 2.0)
            chi2 = rng.gammavariate(NU / 2, 2.0)
            r1 = math.sqrt(matched * NU / chi1) * factor[0][0] * z[0]
            r2 = math.sqrt(matched * NU / chi2) * (factor[1][0] * z[0] + factor[1][1] * z[1])
            losses.append(round(-(pos[0] * r1 + pos[1] * r2)))
        return losses
    return sim


ref_errs = []
for s in range(50):
    ref_errs.append((abs(cross_error(lambda p, s=s: ref.simulate_losses(p, COV, DRAWS, s, "student_t", NU))), s))
print("reference seeds 0-49: max |rel err| =", f"{max(ref_errs)[0]:.4f}", "at seed", max(ref_errs)[1], flush=True)

for label, make in (("matched factor on asset 1 only", variant_matched_one_asset),
                    ("one chi-square per asset", variant_chi_per_asset)):
    shifts = []
    for s in range(10):
        e = cross_error(make(s))
        shifts.append(e)
    print(label, "seeds 0-9: cross-term rel error per seed:", " ".join(f"{e:+.4f}" for e in shifts), flush=True)
    print(label, "seeds 0-9: mean rel error", f"{sum(shifts) / len(shifts):+.4f}", flush=True)
