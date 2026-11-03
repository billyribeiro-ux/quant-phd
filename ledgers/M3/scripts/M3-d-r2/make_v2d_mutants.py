"""Write the verifier's round-2 student-error mutants (v2d_01..v2d_05) from the M3 reference, one edit each."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-M3-d")
SRC = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"

MUTANTS = {
    "v2d_01_clip_repair_floor_applied_to_first_eigenvalue_only.py": (
        "clip_repair applies the floor to the first computed eigenvalue only, leaving every other negative one in place.",
        "    x = _rebuild([max(value, floor) for value in values], vectors)\n",
        "    x = _rebuild([max(values[0], floor)] + values[1:], vectors)\n",
    ),
    "v2d_02_comparison_weights_solves_for_volatilities.py": (
        "comparison_weights solves Sigma x = vols instead of Sigma x = ones, so the weights follow the volatilities.",
        "    aug = [[*sigma[i], 1.0] for i in range(n)]\n",
        "    aug = [[*sigma[i], float(vols[i])] for i in range(n)]\n",
    ),
    "v2d_03_clip_repair_refuses_non_psd_input.py": (
        "clip_repair raises ValueError whenever the input has a negative eigenvalue, so it refuses the matrices it repairs.",
        "    x = _rebuild([max(value, floor) for value in values], vectors)\n",
        '    if min(values) < 0.0:\n        raise ValueError("the matrix is not positive semidefinite")\n'
        "    x = _rebuild([max(value, floor) for value in values], vectors)\n",
    ),
    "v2d_04_comparison_weights_refuses_negative_weight.py": (
        "comparison_weights raises ValueError when any weight is negative, although the formula allows negative weights.",
        "    total = sum(solution)\n",
        "    total = sum(solution)\n"
        '    if any(x / total < 0.0 for x in solution):\n        raise ValueError("a weight is negative")\n',
    ),
    "v2d_05_min_eigenvalue_gershgorin_bound.py": (
        "min_eigenvalue returns the Gershgorin lower bound (least diagonal entry minus its absolute off-diagonal row sum).",
        "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)\n",
        "    a = _as_matrix(matrix)\n    n = len(a)\n"
        "    return min(a[i][i] - sum(abs(a[i][j]) for j in range(n) if j != i) for i in range(n))\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    body = SRC.replace(old, new, 1)
    start = body.index('"""')
    end = body.index('"""', start + 3) + 3
    body = f'"""{doc}"""\n' + body[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)

# Round 2, second batch: a student who uses NumPy although the page requires the standard library only.
NUMPY_OLD = '    n = len(a)\n    m = [row[:] for row in a]\n    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]\n    for _ in range(100):'
NUMPY_NEW = (
    '    import numpy as np\n'
    '    w, vec = np.linalg.eigh(np.array(a, dtype=float))\n'
    '    return [float(x) for x in w], [[float(x) for x in row] for row in vec]\n'
    '    n = len(a)\n    m = [row[:] for row in a]\n    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]\n    for _ in range(100):'
)
name = "v2d_06_eigh_uses_numpy_not_standard_library.py"
assert SRC.count(NUMPY_OLD) == 1, SRC.count(NUMPY_OLD)
body = SRC.replace(NUMPY_OLD, NUMPY_NEW, 1)
start = body.index('"""')
end = body.index('"""', start + 3) + 3
body = '"""_eigh uses numpy.linalg.eigh, although the page requires the standard library only."""\n' + body[end:]
(OUT / name).write_text(body, encoding="utf-8")
print("wrote", name)
