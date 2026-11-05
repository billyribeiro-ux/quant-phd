"""Generate five round-11 alternative correct M7 solvers (constrained_allocator.py) from the reference.

Validation, certificate and the multiplier mapping are the reference's (so the named refusals are the same code path);
only the active-set search differs: exact rule variants, and float searches with exact polishing or pure float.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")

def sub(text, old, new):
    assert text.count(old) == 1, (text.count(old), old[:70])
    return text.replace(old, new, 1)

def header(name, doc):
    return REF.replace('"""Reference solution', f'"""{doc}\n\nReference solution', 1)

# --- exact variants -------------------------------------------------------------------------------------------
alt1 = header("alt1", "Alt-1 (verifier r11): exact Fraction active set, drops the LAST negative multiplier and breaks ratio ties at the last index.")
alt1 = sub(alt1, "            working.pop(min(negative)[1])\n", "            working.pop(max(k for _, k in negative))\n")
alt1 = sub(alt1, "        for j, (a, b, _) in enumerate(rows):\n            if j in working:\n                continue\n            rate = _dot(a, p)\n            if rate > 0:\n                ratio = max(b - _dot(a, x), Fraction(0)) / rate\n                if ratio < step:",
           "        for j, (a, b, _) in enumerate(rows):\n            if j in working:\n                continue\n            rate = _dot(a, p)\n            if rate > 0:\n                ratio = max(b - _dot(a, x), Fraction(0)) / rate\n                if ratio <= step:")

alt2 = header("alt2", "Alt-2 (verifier r11): exact Fraction active set from an EMPTY working set (no constraint is pre-activated) with a last-in-first-out drop rule.")
alt2 = sub(alt2, "    for j, (a, b, _) in enumerate(rows):\n        if b - _dot(a, x) <= TOL and _rank([budget, *(rows[k][0] for k in working), a]) > len(working) + 1:\n            working.append(j)\n", "")
alt2 = sub(alt2, "            working.pop(min(negative)[1])\n",
           "            last = len(working) - 1\n            working.pop(last if any(k == last for _, k in negative) else min(negative)[1])\n")

# --- float variants -------------------------------------------------------------------------------------------
FLOAT_BLOCK = '''
def _fdot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def _fsolve(matrix, rhs):
    size = len(rhs)
    rows = [[*matrix[i], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
        if abs(rows[pivot][col]) == 0.0:
            raise RuntimeError("singular float system")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0.0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _fkkt(hessian, gradient, active):
    n, m = len(gradient), len(active)
    size = n + m
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
    for k, a in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    solution = _fsolve(matrix, [-g for g in gradient] + [0.0] * m)
    return solution[:n], solution[n:]


def _polish(problem, rows, working):
    """Exact KKT solve on the float working set: H x + A' lambda = mu and A_active x = b. Returns None if not valid."""
    n = problem.n
    active = [([Fraction(1)] * n, Fraction(1))] + [(rows[j][0], rows[j][1]) for j in working]
    size = n + len(active)
    matrix = [[Fraction(0)] * size for _ in range(size)]
    rhs = [Fraction(0)] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = problem.gamma * problem.sigma[i][j]
        for c, (a, _) in enumerate(active):
            matrix[i][n + c] = a[i]
        rhs[i] = problem.mu[i]
    for c, (a, b) in enumerate(active):
        for j in range(n):
            matrix[n + c][j] = a[j]
        rhs[n + c] = b
    try:
        solution = _solve_linear(matrix, rhs)
    except (StopIteration, ZeroDivisionError):
        return None
    x, lam = solution[:n], solution[n:]
    if any(_dot(a, x) - b > 0 for a, b, _ in rows):
        return None
    if any(lam[1 + k] < 0 for k in range(len(working))):
        return None
    return x, lam


def _active_set_float(problem, rows, tol, polish):
    n = problem.n
    hessian = [[float(problem.gamma * problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [float(v) for v in problem.mu]
    dense = [[float(v) for v in a] for a, _, _ in rows]
    bounds = [float(b) for _, b, _ in rows]
    budget = [1.0] * n
    x = [float(v) for v in problem.w0]
    working: list[int] = []
    for j in range(len(rows)):
        if bounds[j] - _fdot(dense[j], x) <= tol and _rank([budget, *(rows[k][0] for k in working), rows[j][0]]) > len(working) + 1:
            working.append(j)
    for _ in range(500):
        gradient = [_fdot(hessian[i], x) - mu[i] for i in range(n)]
        p, lam = _fkkt(hessian, gradient, [budget] + [dense[j] for j in working])
        if max(abs(v) for v in p) <= tol:
            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -tol]
            if not negative:
                if polish:
                    exact = _polish(problem, rows, working)
                    if exact is not None:
                        xe, le = exact
                        mult = {rows[j][2]: le[1 + k] for k, j in enumerate(working)}
                        return xe, mult, le[0]
                mult = {rows[j][2]: Fraction(lam[1 + k]) for k, j in enumerate(working)}
                return [Fraction(v) for v in x], mult, Fraction(lam[0])
            working.pop(min(negative)[1])
            continue
        step, blocking = 1.0, None
        for j in range(len(rows)):
            if j in working:
                continue
            rate = _fdot(dense[j], p)
            if rate > tol:
                ratio = max(bounds[j] - _fdot(dense[j], x), 0.0) / rate
                if ratio < step:
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if blocking is not None:
            working.append(blocking)
    raise RuntimeError("the float active-set search did not converge")


def _active_set(problem, rows):
    return _active_set_float(problem, rows, TOL_F, POLISH)


'''

def float_alt(name, doc, tol, polish):
    text = header(name, doc)
    start = text.index("def _active_set(")
    end = text.index("def _solve(")
    text = text[:start] + FLOAT_BLOCK.replace("TOL_F", repr(tol)).replace("POLISH", repr(polish)) + text[end:]
    return text

alt3 = float_alt("alt3", "Alt-3 (verifier r11): float active set with tolerance 1e-9, then an exact Fraction KKT polish of the final active set.", 1e-9, True)
alt4 = float_alt("alt4", "Alt-4 (verifier r11): pure float active set with tolerance 1e-12 and float multipliers, no exact polish.", 1e-12, False)
alt5 = float_alt("alt5", "Alt-5 (verifier r11): float active set with tolerance 1e-10, then an exact Fraction KKT polish of the final active set.", 1e-10, True)

for name, text in [("alt1_exact_last_drop.py", alt1), ("alt2_exact_empty_start_lifo.py", alt2),
                   ("alt3_float_1e-9_exact_polish.py", alt3), ("alt4_float_1e-12_pure.py", alt4),
                   ("alt5_float_1e-10_exact_polish.py", alt5)]:
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", OUT / name)

# --- scale-aware float variants (verifier r11 follow-up): thresholds relative to the size of the iterate and step ---
SCALED = (FLOAT_BLOCK
          .replace("        if max(abs(v) for v in p) <= tol:\n",
                   "        if max(abs(v) for v in p) <= tol * max(1.0, max(abs(v) for v in x)):\n")
          .replace("            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -tol]\n",
                   "            scale = max(1.0, max(abs(v) for v in lam))\n            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -tol * scale]\n")
          .replace("        step, blocking = 1.0, None\n",
                   "        pnorm = max(abs(v) for v in p)\n        step, blocking = 1.0, None\n")
          .replace("            if rate > tol:\n", "            if rate > tol * pnorm:\n"))
assert SCALED.count("tol * pnorm") == 1 and SCALED.count("scale = max") == 1 and SCALED.count("tol * max(1.0") == 1

def scaled_alt(name, doc, tol, polish):
    text = header(name, doc)
    start = text.index("def _active_set(")
    end = text.index("def _solve(")
    text = text[:start] + SCALED.replace("TOL_F", repr(tol)).replace("POLISH", repr(polish)) + text[end:]
    return text

alt6 = scaled_alt("alt6", "Alt-6 (verifier r11): scale-aware float active set (tolerances relative to the iterate and the step), tolerance 1e-9, then an exact Fraction KKT polish.", 1e-9, True)
alt7 = scaled_alt("alt7", "Alt-7 (verifier r11): scale-aware pure float active set (tolerances relative to the iterate and the step), tolerance 1e-12, no exact polish.", 1e-12, False)
for name, text in [("alt6_scaled_float_1e-9_exact_polish.py", alt6), ("alt7_scaled_float_1e-12_pure.py", alt7)]:
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", OUT / name)

# --- two more correct solvers so that five pass: exact with reversed constraint order, scale-aware float at 1e-10 ---
alt8 = header("alt8", "Alt-8 (verifier r11): exact Fraction active set with the constraint rows searched in reverse order (ties go to the last row).")
alt8 = sub(alt8, "    for j, (a, b, _) in enumerate(rows):\n        if b - _dot(a, x) <= TOL and _rank(",
           "    for j, (a, b, _) in reversed(list(enumerate(rows))):\n        if b - _dot(a, x) <= TOL and _rank(")
alt8 = sub(alt8, "        for j, (a, b, _) in enumerate(rows):\n            if j in working:",
           "        for j, (a, b, _) in reversed(list(enumerate(rows))):\n            if j in working:")
alt9 = scaled_alt("alt9", "Alt-9 (verifier r11): scale-aware float active set (tolerances relative to the iterate and the step), tolerance 1e-10, then an exact Fraction KKT polish.", 1e-10, True)
for name, text in [("alt8_exact_reversed_rows.py", alt8), ("alt9_scaled_float_1e-10_exact_polish.py", alt9)]:
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", OUT / name)
