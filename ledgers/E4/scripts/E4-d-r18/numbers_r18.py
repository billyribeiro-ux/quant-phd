"""Round 18: re-derive the numbers in prose and docstrings of slice d that the delta could affect, plus the Lab 1 claim
about the 53rd halving. Oracle and closed form imported from the suite (solver = reference copy in the probe dir)."""
import math, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E4-d-r18/probe")
import solver as ref
import test_project as tp

print("A. docstring test_gap_at_zero_fraction_is_the_limit_to_full_precision (test_project.py:386-390)")
for sd, cost in [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]:
    lim = ref.gap_at_zero(sd, cost)
    g1e12 = ref.indifference_gap(1e-12, sd, cost)
    orc = tp.oracle_gap(0.0, sd, cost)
    print(f"  sd={sd} c={cost}: |gap(1e-12)-limit|={abs(g1e12-lim):.3e}  |oracle(0)-limit|={abs(orc-lim):.3e} "
          f"|reported-limit|={abs(ref.solve_model(sd,cost)['indifference_gap']-lim):.1e}")

print("B. test_corner_root (test_project.py:568-571): root and 200- vs 240-halving widths")
sd, cost = 1e-50, 0.1707691121
exact = tp.closed_form_root(sd, cost)
print(f"  closed-form root={exact:.6e}  1e-10*root={1e-10*exact:.3e}  2^-200={2.0**-200:.3e}  2^-240={2.0**-240:.3e}")
print(f"  tau-bar at cost={2*math.exp(-4*cost)-1:.8f} (must be >= 1e-2)")
print("  reference lambda at corner:", ref.solve_model(sd, cost)["informed_fraction"], "rel err", abs(ref.solve_model(sd,cost)["informed_fraction"]-exact)/exact)

print("C. Lab 1 claim: bracket width after k halvings (page line 170: 2^-53 at the 53rd halving)")
A, TV, TE, SD, COST = 2.0, 1.0, 1.0, 0.60, 0.13
def ty(lam): return lam*lam*TE*TE/(lam*lam*TE + A*A*SD*SD)
def gap(lam):
    t = ty(lam); bd = lam*(TV+TE)+(1-lam)*(TV+t); bs = (lam*TE+(1-lam)*t)/bd; bu = -A*bs/(lam*TE)
    r = t/(TV+t)-bs; fu = (1+r*r*(TV+t)*(1/TV+1/t))**-0.5
    sl = TE/(TV+TE)-bs; fi = (1+(TV+TE)*(sl*sl*(1/TV+1/TE)+bu*bu*SD*SD))**-0.5
    return fu - math.exp(A*COST)*fi
low, high = 0.0, 1.0
first_eq = None
for k in range(1, 61):
    mid = 0.5*(low+high)
    if gap(mid) > 0: low = mid
    else: high = mid
    if k in (1,2,3,52,53,54,60):
        print(f"  halving {k}: width={high-low:.6e}")
print("  2^-53 =", 2.0**-53)
