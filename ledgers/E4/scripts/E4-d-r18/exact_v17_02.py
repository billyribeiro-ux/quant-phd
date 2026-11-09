"""Round 18: 60-digit decimal evaluation of the Proposition 3 gap at the reported fraction, to decide whether the
double-precision reference formula or the mutant is the one off by ~1e-14 at tiny noise volumes."""
import importlib.util, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 80
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E4-d-r18/probe")
import solver as ref
spec = importlib.util.spec_from_file_location("mut", "/Users/billyribeiro/.fanout/wt/verifyE18-E4-d/ledgers/E4/equivalent/mutant_v17_02_price_slope_drops_uninformed_term.py")
mut = importlib.util.module_from_spec(spec); spec.loader.exec_module(mut)
A, TV, TE = D(2), D(1), D(1)

def exact_gap(lam, sd, c, which="ref"):
    lam = D(lam); sd = D(sd); c = D(c)
    ty = lam*lam*TE*TE/(lam*lam*TE + A*A*sd*sd)
    den = lam*(TV+TE) + (1-lam)*(TV+ty)
    bs = (lam*TE + (1-lam)*ty)/den if which == "ref" else (lam*TE)/den
    bu = -A*bs/(lam*TE)
    r = ty/(TV+ty) - bs
    fu = (1 + r*r*(TV+ty)*(1/TV + 1/ty)) ** D("-0.5")
    P = TV+TE
    slope = TE/P - bs
    vg = slope*slope*(1/TV + 1/TE) + bu*bu*sd*sd
    fi = (1 + P*vg) ** D("-0.5")
    return fu - (A*c).exp()*fi

for sd, c in [(3.3245979322709314e-22, 0.059130434782608696), (1e-22, 0.0598), (1e-40, 0.0598), (1e-50, 0.0598), (0.1, 0.0598)]:
    m = mut.solve_model(sd, c); r = ref.solve_model(sd, c)
    lam = m["informed_fraction"]
    ex = exact_gap(D(lam), sd, c, "ref")
    ex_mut = exact_gap(D(lam), sd, c, "mut")
    print(f"sd={sd:.3e} c={c}: lam={lam:.6e} exact_ref_gap={float(ex):+.6e} "
          f"ref_double-exact={float(D(r['indifference_gap'])-ex):+.3e} mut_double-exact={float(D(m['indifference_gap'])-ex):+.3e} "
          f"exact_mutant_formula-exact_ref={float(ex_mut-ex):+.3e}")
