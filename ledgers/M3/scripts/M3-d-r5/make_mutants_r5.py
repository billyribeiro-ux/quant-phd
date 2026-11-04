"""Round-5 verifier: new student-error mutants of the M3 reference, written to ledgers/M3/mutants/.

Each mutant is the reference with one edit to projection_repair. The edit is asserted to match exactly once.
"""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD5-M3-d")
REF = ROOT / "course/modules/M/M3/grader/reference.py"
OUT = ROOT / "ledgers/M3/mutants"
src = REF.read_text(encoding="utf-8")

MUTANTS = {
    "v5d_01_projection_drops_unit_diagonal_correction.py": (
        "projection_repair drops the unit-diagonal correction term (plain alternating projections, not Dykstra).",
        "        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]\n",
        "        corr_u = [[0.0 for j in range(n)] for i in range(n)]\n",
    ),
    "v5d_02_projection_starts_psd_correction_at_input.py": (
        "projection_repair starts the PSD correction term at the input instead of at the zero matrix.",
        "    corr_s = [[0.0] * n for _ in range(n)]\n",
        "    corr_s = [row[:] for row in a]\n",
    ),
    "v5d_03_projection_projects_unit_diagonal_first.py": (
        "projection_repair projects onto the unit-diagonal matrices before the positive semidefinite ones, the reverse of the page's order.",
        "    x = a\n    corr_s = [[0.0] * n for _ in range(n)]\n    corr_u = [[0.0] * n for _ in range(n)]\n    for _ in range(max_iter):\n        y = _psd_projection([[x[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])\n        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]\n        new_x = [[y[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]\n        for i in range(n):\n            new_x[i][i] = 1.0\n        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]\n        gap = _frobenius(new_x, y)\n        step = _frobenius(new_x, x)\n        x = new_x\n        if gap <= tol and step <= tol:\n            break\n    return x\n",
        "    x = a\n    corr_s = [[0.0] * n for _ in range(n)]\n    corr_u = [[0.0] * n for _ in range(n)]\n    for _ in range(max_iter):\n        w = [[x[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]\n        for i in range(n):\n            w[i][i] = 1.0\n        corr_u = [[x[i][j] + corr_u[i][j] - w[i][j] for j in range(n)] for i in range(n)]\n        new_x = _psd_projection([[w[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])\n        corr_s = [[w[i][j] + corr_s[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]\n        gap = _frobenius(new_x, w)\n        step = _frobenius(new_x, x)\n        x = new_x\n        if gap <= tol and step <= tol:\n            break\n    return x\n",
    ),
    "v5d_04_projection_stops_when_either_gap_or_change_is_small.py": (
        "projection_repair stops early when either the gap or the change is at most tol, not only when both are.",
        "        if gap <= tol and step <= tol:\n",
        "        if gap <= tol or step <= tol:\n",
    ),
    "v5d_05_projection_drops_psd_correction_term.py": (
        "projection_repair drops the positive semidefinite correction term (corr_s stays zero at every step).",
        "        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]\n",
        "        corr_s = [[0.0 for j in range(n)] for i in range(n)]\n",
    ),
    "v5d_06_projection_returns_rescaled_psd_iterate.py": (
        "projection_repair returns the rescaled positive semidefinite iterate of the last step instead of the last unit-diagonal iterate.",
        "    return x\n\n\ndef comparison_weights",
        "    d = [y[i][i] for i in range(n)]\n    return [[y[i][j] / math.sqrt(d[i] * d[j]) for j in range(n)] for i in range(n)]\n\n\ndef comparison_weights",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    if src.count(old) != 1:
        raise SystemExit(f"{name}: anchor found {src.count(old)} times")
    head_old = src.split('"""', 2)
    body = src.replace(old, new, 1)
    first_doc_end = body.index('"""', 3) + 3
    body = '"""' + doc + '\n\nMutant of the reference. Not shipped to learners.\n"""' + body[body.index('"""', 3) + 3 :]
    body = body.replace("Reference solution for the M3 project", "Mutant of the M3 reference for the M3 project", 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name, len(body))
