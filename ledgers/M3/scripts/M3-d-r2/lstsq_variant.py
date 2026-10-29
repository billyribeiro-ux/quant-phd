"""Round-2 witness: the reference module with comparison_weights replaced by numpy.linalg.lstsq (minimum-norm
solution, a standard way to handle a singular Sigma). Used only to show the Lab 3 test's dependence on the solver."""
import re, sys
src = open("/tmp/verifyB2-M3-d/course/modules/M/M3/grader/reference.py", encoding="utf-8").read()
new = '''def comparison_weights(corr, vols):
    import numpy as _np
    c = _as_matrix(corr)
    n = len(c)
    if len(vols) != n:
        raise ValueError("the volatilities must have one entry per row of the correlation matrix")
    if any(float(v) <= 0.0 for v in vols):
        raise ValueError("every volatility must be strictly positive")
    d = _np.diag([float(v) for v in vols])
    sol = _np.linalg.lstsq(d @ _np.array(c) @ d, _np.ones(n), rcond=None)[0]
    return [float(x) for x in sol / sol.sum()]
'''
idx = src.index("def comparison_weights")
open(sys.argv[1], "w", encoding="utf-8").write(src[:idx] + new)
