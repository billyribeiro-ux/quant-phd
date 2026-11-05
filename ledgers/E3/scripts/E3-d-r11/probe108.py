"""Round-11: why the reference stalls at seed 108. Prints the reference estimate, the oracle and engine gradients (they must agree),
the instrumented exit of the maximiser, and the finite-difference derivative in log-lambda at several steps.
usage: probe108.py <dir containing elicit.py, instance.py, test_project.py>"""
import json
import math
import sys
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
import elicit  # noqa: E402
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402

r = json.loads(str(make_instance(108)["responses_json"]))
est = elicit.estimate(r)
g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
parsed_e = [elicit._parse(x) for x in r]
parsed_t = [tp.parse(x) for x in r]
xi = [math.log(g / (1 - g)), math.log(l), math.log(k)]
f_engine = lambda t: elicit._objective(t, parsed_e)  # noqa: E731
f_oracle = lambda t: tp.oracle_loglik(parsed_t, 1 / (1 + math.exp(-t[0])), math.exp(t[1]), math.exp(t[2]))  # noqa: E731
print("estimate", {x: round(v, 6) for x, v in est.items()})
print("score at the estimate: 1e-5 %.4e, 1e-6 %.4e" % (tp._largest_score_component(parsed_t, g, l, k, 1e-5), tp._largest_score_component(parsed_t, g, l, k, 1e-6)))
for i, name in enumerate(("zeta", "log lambda", "log kappa")):
    up, dn = list(xi), list(xi)
    up[i] += 1e-5
    dn[i] -= 1e-5
    print(f"grad {name}: engine {(f_engine(up) - f_engine(dn)) / 2e-5:+.6f} oracle {(f_oracle(up) - f_oracle(dn)) / 2e-5:+.6f}")
base = f_engine(xi)
for h in (1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
    up, dn = list(xi), list(xi)
    up[1] += h
    dn[1] -= h
    print(f"central derivative in log lambda at step {h:g}: {(f_engine(up) - f_engine(dn)) / (2 * h):+.6f}")
