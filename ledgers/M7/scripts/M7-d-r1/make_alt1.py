"""Build alternative 1 (round-1 verifier): the reference's validation and certificate, with a different solver.

Solver: Caratheodory's theorem puts an optimal KKT multiplier vector on a linearly independent set of generators drawn
from {+1, -1 (the budget row, either sign)} and the active inequality rows. So the search tries every independent
working set of at most n inequality rows, with the budget row or without it (budget multiplier zero). Each candidate is
screened by a float KKT solve, then the first one that is exactly primal- and dual-feasible is confirmed in exact
Fraction arithmetic. The ordering only changes speed; the enumeration is complete.
Usage: python3 -I make_alt1.py <checkout-root> <output-path>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
inequalities = ref[ref.index("def _inequalities(") : ref.index("def _active_set(")]
head = ref[: ref.index("def _kkt_step(")]
tail = ref[ref.index("def _solve(problem: Problem)") :]
head = head.replace(ref[: ref.index('"""', 3) + 3], '"""Alternative 1 (round-1 verifier): reference validation and certificate; enumerated working-set solver."""', 1)

solver = '''
import itertools


def _float_solve(matrix, rhs):
    size = len(rhs)
    a = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for c in range(size):
        p = max(range(c, size), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-13:
            return None
        a[c], a[p] = a[p], a[c]
        for r in range(size):
            if r != c and a[r][c] != 0.0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c], strict=True)]
    return [a[i][size] / a[i][i] for i in range(size)]


def _active_set(problem, rows):
    n = problem.n
    hessian = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]
    hess_f = [[float(hessian[i][j]) for j in range(n)] for i in range(n)]
    mu_f = [float(m) for m in problem.mu]
    budget_row = [Fraction(1)] * n

    def float_candidate(subset, with_budget):
        rows_f = ([([1.0] * n, 1.0)] if with_budget else []) + [([float(x) for x in rows[j][0]], float(rows[j][1])) for j in subset]
        m = len(rows_f)
        size = n + m
        matrix = [[0.0] * size for _ in range(size)]
        rhs = [0.0] * size
        for i in range(n):
            for j in range(n):
                matrix[i][j] = hess_f[i][j]
            rhs[i] = mu_f[i]
        for k, (a, b) in enumerate(rows_f):
            for i in range(n):
                matrix[i][n + k] = a[i]
                matrix[n + k][i] = a[i]
            rhs[n + k] = b
        return _float_solve(matrix, rhs), m

    def exact_confirm(subset, with_budget):
        rows_s = ([budget_row] if with_budget else []) + [rows[j][0] for j in subset]
        rhs_rows = ([Fraction(1)] if with_budget else []) + [rows[j][1] for j in subset]
        m = len(rows_s)
        size = n + m
        matrix = [[Fraction(0)] * size for _ in range(size)]
        for i in range(n):
            for j in range(n):
                matrix[i][j] = hessian[i][j]
        for k, a in enumerate(rows_s):
            for i in range(n):
                matrix[i][n + k] = a[i]
                matrix[n + k][i] = a[i]
        sol = _solve_linear(matrix, [*problem.mu, *rhs_rows])
        x, lam = sol[:n], sol[n:]
        offset = 1 if with_budget else 0
        if any(lam[offset + k] < 0 for k in range(len(subset))):
            return None
        if any(_dot(rows[j][0], x) > rows[j][1] for j in range(len(rows))) or sum(x) != 1:
            return None
        multipliers = {rows[j][2]: lam[offset + k] for k, j in enumerate(subset)}
        return x, multipliers, (lam[0] if with_budget else Fraction(0))

    for k in range(0, n + 1):
        for subset in itertools.combinations(range(len(rows)), k):
            for with_budget in ((True, False) if k < n else (False,)):
                if with_budget and k > n - 1:
                    continue
                cand, m = float_candidate(list(subset), with_budget)
                if cand is None:
                    continue
                x_f, lam_f = cand[:n], cand[n:]
                offset = 1 if with_budget else 0
                if any(lam_f[offset + q] < -1e-12 for q in range(len(subset))):
                    continue
                if any(sum(float(v) * x_f[i] for i, v in enumerate(rows[j][0])) > float(rows[j][1]) + 1e-12
                       for j in range(len(rows))):
                    continue
                result = exact_confirm(list(subset), with_budget)
                if result is not None:
                    return result
    raise RuntimeError("no KKT working set was found")


'''
out = Path(sys.argv[2])
out.write_text(head + inequalities + solver + tail, encoding="utf-8")
print("wrote", out)
