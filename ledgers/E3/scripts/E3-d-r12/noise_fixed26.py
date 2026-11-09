import math, sys
import elicit as sol
import test_project as tp
responses = [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS]
parsed = [sol._parse(r) for r in responses]
xi = sol._maximise(parsed)
f = lambda t: sol._objective(t, parsed)
f0 = f(list(xi))
print("f0", f0, "ulp(f0)", math.ulp(f0))
h = sol._H
up = f([xi[0] + h, xi[1], xi[2]]); down = f([xi[0] - h, xi[1], xi[2]])
num = up - 2*f0 + down
print("zeta second difference numerator", num, "hess entry", num/(h*h), "FD noise scale ~ ulp/h^2", math.ulp(f0)/(h*h))
print("up-f0, f0-down", up-f0, f0-down)
