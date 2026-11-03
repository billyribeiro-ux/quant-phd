"""Round-3 verifier D (M4 slice d): re-derive the tolerance comments of grader/test_project.py (lines 31-48).

For each seed s in the window, the instance is make_instance(s) from the checkout's grader/instance.py. Only seeds whose
instance nu equals the nu under test are counted, which is how the suite uses them (the suite's Student-t variance check
runs at the instance's own nu). The reference is the checkout's grader/reference.py. The unmatched family is the same
simulation with the matched factor (nu - 2) / nu replaced by 1 (the omission the comment describes), reproduced here
line for line so the RNG stream is identical.
Usage: python -I ledgers/M4/scripts/M4-d-r3/sweep_tolerance_r3.py <checkout_root> <seed_lo> <seed_hi>
"""
import importlib.util
import math
import random
import sys

root, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
grader = root + "/course/modules/M/M4/grader"
sys.path.insert(0, grader)
import instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", grader + "/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def sim_unmatched(position_cents, cov, n_draws, seed, nu):
    n = len(position_cents)
    factor = ref._cholesky(cov, n)
    rng = random.Random(seed)
    losses = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        chi_square = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt(1.0 * nu / chi_square)
        total = 0.0
        for i in range(n):
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
            total += position_cents[i] * ret
        losses.append(round(-total))
    return losses


def sv(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def target_of(pos, cov):
    return math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(len(pos)) for j in range(len(pos)))


stats = {nu: {"seeds": 0, "ref_max": 0.0, "ref_max_seed": None, "unmatched_fail": 0} for nu in (3, 4, 5, 6, 7, 8)}
for s in range(lo, hi):
    inst = instance.make_instance(s)
    nu = inst["nu"]
    pos, cov, nd = inst["positions_cents"], inst["cov"], inst["n_draws"]
    tgt = target_of(pos, cov)
    st = stats[nu]
    st["seeds"] += 1
    if nu >= 5:
        err = abs(sv(ref.simulate_losses(pos, cov, nd, s, "student_t", nu)) / tgt - 1.0)
        if err > st["ref_max"]:
            st["ref_max"], st["ref_max_seed"] = err, s
        ue = abs(sv(sim_unmatched(pos, cov, nd, s, nu)) / tgt - 1.0)
        st["unmatched_fail"] += ue > 0.30
    else:
        err = abs(sv(ref.simulate_losses(pos, cov, nd, s, "student_t", nu)) / tgt - 1.0)
        if err > st["ref_max"]:
            st["ref_max"], st["ref_max_seed"] = err, s
        ue = abs(sv(sim_unmatched(pos, cov, nd, s, nu)) / tgt - 1.0)
        st["unmatched_fail"] += ue > 0.30
for nu in sorted(stats):
    st = stats[nu]
    print(f"nu={nu} seeds_with_this_nu={st['seeds']} ref_max_rel_err={st['ref_max']:.4f} at_seed={st['ref_max_seed']} "
          f"unmatched_variance_check_fails={st['unmatched_fail']}/{st['seeds']}", flush=True)
