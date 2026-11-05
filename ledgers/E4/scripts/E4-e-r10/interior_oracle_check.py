import sys, math
W = sys.argv[1]
sys.path.insert(0, W)
import reference as ref
import test_project as tp
worst = 0.0
rows = []
for sd in (0.5, 0.6, 0.75):
    for cost in (0.12, 0.15, 0.30):
        for lam in (0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
            r = ref.indifference_gap(lam, sd, cost)
            o = tp.oracle_gap(lam, sd, cost)
            d = abs(r - o)
            worst = max(worst, d)
            rows.append((sd, cost, lam, d))
print("max |reference - oracle| at interior/unit fractions:", f"{worst:.3e}")
print("rows above 1e-13:", sum(1 for r in rows if r[3] > 1e-13), "of", len(rows))
# effect of a 1e-12 relative error in the cost factor on the gap at lam=0.5
for sd, cost in ((0.5, 0.12), (0.75, 0.15)):
    base = ref.indifference_gap(0.5, sd, cost)
    perturbed = ref.uninformed_term(0.5, sd) - math.exp(2.0 * cost * (1 + 1e-12)) * ref.informed_term(0.5, sd)
    print(f"sd={sd} cost={cost}: gap shift from cost factor 1e-12 relative = {perturbed - base:.3e}")
