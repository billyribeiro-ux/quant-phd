"""Re-derive the grader comment's seed sweep (test_project.py lines 31-39) with the reference and an unmatched variant."""
import sys, math, time, importlib.util, collections
sys.path.insert(0, "/tmp/M4-d-r10-scratch/ref")
import instance as inst_mod
spec = importlib.util.spec_from_file_location("ref", "/tmp/M4-d-r10-scratch/ref/tail_risk.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)

def fsum_var(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)

def unmatched_losses(positions, cov, n, seed, nu):
    # reference with matched factor replaced by 1: scale = sqrt(nu / chi)
    import random
    factor = ref._cholesky(cov, len(positions))
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        z = [rng.gauss(0.0, 1.0) for _ in positions]
        chi = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt(nu / chi)
        total = 0.0
        for i in range(len(positions)):
            total += positions[i] * scale * sum(factor[i][k] * z[k] for k in range(i + 1))
        out.append(round(-total))
    return out

lo, hi = int(sys.argv[1]), int(sys.argv[2])
rows = []
for seed in range(lo, hi):
    I = inst_mod.make_instance(seed)
    pos, cov, nu, n = I["positions_cents"], I["cov"], I["nu"], I["n_draws"]
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
    ref_losses = ref.simulate_losses(pos, cov, n, seed, "student_t", nu)
    rel = abs(fsum_var(ref_losses) / target - 1.0)
    unm = unmatched_losses(pos, cov, n, seed, nu)
    rel_unm = abs(fsum_var(unm) / target - 1.0)
    rows.append((seed, nu, rel, rel_unm))
for r in rows:
    print(f"{r[0]} {r[1]} {r[2]:.6f} {r[3]:.6f}")
