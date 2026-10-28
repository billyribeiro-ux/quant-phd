import sys, math, importlib.util, time
ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/course/modules/M/M4/grader")
import instance
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ref = load("ref", ROOT + "/course/modules/M/M4/grader/reference.py")
mut = load("mut", ROOT + "/ledgers/M4/mutants/m01_student_t_not_rescaled.py")
def sv(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)
NS = 2000
mode = sys.argv[2]
t0 = time.time()
if mode == "forced":
    for nu in (5, 6, 7, 8):
        worst = 0.0; worst_s = None; fm = 0
        for s in range(NS):
            inst = instance.make_instance(s)
            pos, cov, nd = inst["positions_cents"], inst["cov"], inst["n_draws"]
            target = math.fsum(pos[i]*pos[j]*cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
            e = abs(sv(ref.simulate_losses(pos, cov, nd, s, "student_t", nu)) / target - 1.0)
            if e > worst: worst, worst_s = e, s
            em = abs(sv(mut.simulate_losses(pos, cov, nd, s, "student_t", nu)) / target - 1.0)
            fm += em > 0.30
        print(f"forced nu={nu} ref_max={worst:.6f} at_seed={worst_s} mutant_fails={fm}/{NS}", flush=True)
else:
    from collections import Counter
    cnt = Counter(); ref_max = {}; mfail = Counter(); worst_seed = {}
    for s in range(NS):
        inst = instance.make_instance(s)
        nu = inst["nu"]; cnt[nu] += 1
        if nu < 5: continue
        pos, cov, nd = inst["positions_cents"], inst["cov"], inst["n_draws"]
        target = math.fsum(pos[i]*pos[j]*cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
        e = abs(sv(ref.simulate_losses(pos, cov, nd, s, "student_t", nu)) / target - 1.0)
        if e > ref_max.get(nu, 0.0): ref_max[nu] = e; worst_seed[nu] = s
        em = abs(sv(mut.simulate_losses(pos, cov, nd, s, "student_t", nu)) / target - 1.0)
        mfail[nu] += em > 0.30
    print("instance nu counts over seeds 0-1999:", dict(sorted(cnt.items())))
    for nu in sorted(ref_max):
        print(f"instance nu={nu} seeds={cnt[nu]} ref_max={ref_max[nu]:.6f} at_seed={worst_seed[nu]} mutant_fails={mfail[nu]}/{cnt[nu]}")
    # seed 1093
    inst = instance.make_instance(1093); print("seed1093 nu", inst["nu"])
print("elapsed", round(time.time()-t0,1))
