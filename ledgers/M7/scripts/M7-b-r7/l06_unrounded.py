import sys
from fractions import Fraction
src = open(sys.argv[1], encoding="utf-8").read().rsplit("\nmain()", 1)[0]
ns = {"__name__": "lab_noexec"}
exec(compile(src, sys.argv[1], "exec"), ns)
_m, mu, sigma = ns["simulate_inputs"]()
N = ns["N_ASSETS"]
for gamma in (Fraction(16), Fraction(4)):
    w, _ = ns["equality_frontier_point"](sigma, mu, gamma, list(range(N)))
    eq = ns["objective"](sigma, mu, gamma, w)
    kept = ns["nonnegative_candidates"](sigma, mu, gamma)
    best = min(kept, key=lambda it: ns["objective"](sigma, mu, gamma, it[1]))
    nn = ns["objective"](sigma, mu, gamma, best[1])
    print("gamma", gamma, "eq_obj", float(eq), "nn_obj", float(nn), "diff", float(nn - eq), "diff_exact", nn - eq)
    if gamma == 4:
        t = [abs(best[1][i] - Fraction(1, 4)) for i in range(N)]
        print("turnover_gamma4", float(sum(t, Fraction(0))), sum(t, Fraction(0)))
