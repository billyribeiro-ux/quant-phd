import sys, importlib.util, math
W = sys.argv[1]
sys.path.insert(0, W)
import reference as ref  # the reference solver, the same content as solver.py
import test_project as tp  # imports solver and instance by name from W (solver == reference via copy)
pairs = [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]
for sd, cost in pairs:
    lim = ref.gap_at_zero(sd, cost)
    g_small = ref.indifference_gap(1e-12, sd, cost)
    o0 = tp.oracle_gap(0.0, sd, cost)
    o_small = tp.oracle_gap(1e-12, sd, cost)
    print(f"sd={sd} cost={cost}: ref_limit={lim!r} gap(1e-12)-limit={g_small-lim:.3e} "
          f"oracle(0)-ref_limit={o0-lim:.3e} oracle(1e-12)-oracle(0)={o_small-o0:.3e} "
          f"tol14={1e-14*max(1.0,abs(lim)):.3e} solver_gap0={ref.indifference_gap(0.0,sd,cost)!r}")
