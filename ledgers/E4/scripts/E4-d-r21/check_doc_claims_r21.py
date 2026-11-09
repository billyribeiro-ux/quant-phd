import sys
sys.path.insert(0, "/tmp/e4d21/gc")
import solver as R
import test_project as T
pairs = [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]
for sd, cost in pairs:
    lim = R.gap_at_zero(sd, cost)
    g1e12 = R.indifference_gap(1e-12, sd, cost)
    orc = T.oracle_gap(0.0, sd, cost)
    print(f"sd {sd} c {cost}: gap(1e-12)-limit {g1e12-lim:+.3e}  oracle(0)-limit {orc-lim:+.3e}  oracle(0)-limit rel(max1) {(orc-lim)/max(1,abs(lim)):+.3e}")
# ratio claim
f = {}
for sd in (0.5, 0.625, 0.75):
    f[sd] = R.solve_model(sd, 0.120)["informed_fraction"]
print(repr(f[0.625]), repr(f[0.5]), repr(f[0.75]))
print("ratio 0.625/0.5", repr(f[0.625] / f[0.5]), " ratio 0.75/0.5", repr(f[0.75] / f[0.5]))
print("ratio using page's literals", 0.6977534100112734 / 0.5582027280090642, 0.8373040920139374 / 0.5582027280090642)
# domain-point root and corner
print("domain point root", repr(R.solve_model(3.3245979322709314e-22, 0.059130434782608696)["informed_fraction"]))
c = 0.1707691121
print("corner tau_bar", 2*2.718281828459045**(-4*c)-1, "root", repr(R.solve_model(1e-50, c)["informed_fraction"]))
print("corner exact", T.closed_form_root(1e-50, c))
