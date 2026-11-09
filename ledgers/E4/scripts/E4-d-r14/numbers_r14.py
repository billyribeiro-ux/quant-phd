"""Re-derive the numbers cited in project.html, the grader docstrings and the E4 equivalent README (round 14)."""
import importlib.util, math, sys
REF = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d/course/modules/E/E4/grader/reference.py"
spec = importlib.util.spec_from_file_location("ref", REF)
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
A, TV, TE = 2.0, 1.0, 1.0
def taubar(c): return (TV + TE) * math.exp(-2 * A * c) - TV
print("taubar(0.150) =", f"{taubar(0.150):.8f}", " taubar(0.120) =", f"{taubar(0.120):.8f}")
print("tau_y(1) min over sd in [0.5,0.75] =", f"{1/(1+4*0.75**2):.8f}")
print("2^-240 =", f"{2.0**-240:.4e}", " 2^-200 =", f"{2.0**-200:.4e}", " 2^-53 =", f"{2.0**-53:.4e}")
print("2^-240/1e-12 =", f"{2.0**-240/1e-12:.4e}")
print("sd max in domain 1e-50*(1+0.002*299) =", f"{1e-50*(1+0.002*299):.6e}")
print("cost lo/hi =", 0.1702992124, 0.1707992124, " taubar lo/hi =", f"{taubar(0.1702992124):.6f}", f"{taubar(0.1707992124):.6f}")
print("test cost 0.1707691121 taubar =", f"{taubar(0.1707691121):.10f}")
print("README cost 0.17076911209224613 taubar =", f"{taubar(0.17076911209224613):.10f}")
print("README cost 0.17076911209 taubar =", f"{taubar(0.17076911209):.10f}")
# reference root at corner
def root(sd, c):
    return ref.solve_model(sd, c)["informed_fraction"]
def closed(sd, c):
    t = taubar(c)
    if t <= 0: return 0.0
    if t >= TE*TE/(TE+A*A*sd*sd): return 1.0
    return A*sd*math.sqrt(t/(TE*(TE-t)))
for sd, c in [(1e-50, 0.17076911209224613), (1e-50, 0.1707691121), (1e-50, 0.17076911209), (1e-50, 1e-6), (1e-40, 1e-4), (1e-12, 0.15), (1e-40, 0.15)]:
    r = root(sd, c); e = closed(sd, c)
    print(f"sd={sd:g} cost={c!r} taubar={taubar(c):.7f} root_ref={r:.6e} closed={e:.6e} relerr={abs(r-e)/e:.4e}")
