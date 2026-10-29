import sys, math, importlib.util
sys.path.insert(0, "/tmp/verifyB3-M4-d/course/modules/M/M4/grader")
import instance
spec = importlib.util.spec_from_file_location("ref", "/tmp/verifyB3-M4-d/course/modules/M/M4/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
mut_spec = importlib.util.spec_from_file_location("mut", "/tmp/verifyB3-M4-d/ledgers/M4/mutants/m01_student_t_not_rescaled.py")
mut = importlib.util.module_from_spec(mut_spec); mut_spec.loader.exec_module(mut)
def sv(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)
NS = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
for nu in (5, 6, 7, 8):
    worst_ref = 0.0; fail_mut = 0; total = 0
    for s in range(NS):
        inst = instance.make_instance(s)
        pos, cov, nd = inst["positions_cents"], inst["cov"], inst["n_draws"]
        target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
        losses = ref.simulate_losses(pos, cov, nd, s, "student_t", nu)
        e = abs(sv(losses) / target - 1.0); worst_ref = max(worst_ref, e)
        ml = mut.simulate_losses(pos, cov, nd, s, "student_t", nu)
        em = abs(sv(ml) / target - 1.0)
        total += 1; fail_mut += em > 0.30
    print(f"nu={nu} seeds={total} ref_max_rel_err={worst_ref:.4f} mutant_fails={fail_mut}/{total}", flush=True)
