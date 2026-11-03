"""Write the verifier's round-3 student-error mutants (v3d_01..05) as complete modules under ledgers/M3/mutants/.

Each mutant is the reference solution with one plausible student error applied by an exact string replacement, which
this script asserts happens exactly once. Run from the checkout root: python3 <this file>.
"""

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"

MUTANTS = {
    "v3d_01_projection_repair_runs_one_extra_step.py": (
        '"""projection_repair runs max_iter + 1 alternating steps, one more than the page allows (an off-by-one).\n\n'
        'Mutant of the reference. Not shipped to learners.\n"""\n',
        "    for _ in range(max_iter):\n",
        "    for _ in range(max_iter + 1):\n",
    ),
    "v3d_02_clip_floor_scaled_by_largest_eigenvalue.py": (
        '"""clip_repair treats the floor as relative: it clips at floor times the largest eigenvalue, not at the floor.\n\n'
        'Mutant of the reference. Not shipped to learners.\n"""\n',
        "    x = _rebuild([max(value, floor) for value in values], vectors)\n",
        "    x = _rebuild([max(value, floor * max(values)) for value in values], vectors)\n",
    ),
    "v3d_03_projection_repair_warm_starts_from_previous_call.py": (
        '"""projection_repair caches its last answer and warm-starts from it, so repeated calls on one matrix differ.\n\n'
        'Mutant of the reference. Not shipped to learners.\n"""\n',
        "    x = a\n",
        "    key = tuple(tuple(row) for row in a)\n    x = _WARM.get(key, a)\n",
    ),
    "v3d_04_clip_repair_rounds_output_to_six_decimals.py": (
        '"""clip_repair rounds its returned entries to six decimals, so the repaired matrix can fail the PSD test.\n\n'
        'Mutant of the reference. Not shipped to learners.\n"""\n',
        "    return _rescale(x)\n",
        "    return [[round(v, 6) for v in row] for row in _rescale(x)]\n",
    ),
    "v3d_05_min_eigenvalue_of_the_repaired_matrix.py": (
        '"""min_eigenvalue returns the smallest eigenvalue of clip_repair(matrix), not of the matrix it is given.\n\n'
        'Mutant of the reference. Not shipped to learners.\n"""\n',
        "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)\n",
        "    values, _ = _eigh(_as_matrix(clip_repair(matrix)))\n    return min(values)\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    body = REF.split('"""', 2)[2]  # drop the reference's module docstring, keep everything after it
    text = doc + body
    if name.startswith("v3d_03"):
        text = text.replace(
            "Matrix = list[list[float]]\n", "Matrix = list[list[float]]\n\n_WARM: dict = {}\n", 1
        )
    assert text.count(old) == 1, (name, text.count(old))
    text = text.replace(old, new, 1)
    if name.startswith("v3d_03"):
        # store the answer for the next call with the same argument
        assert text.count("    return x\n") == 1
        text = text.replace("    return x\n", "    _WARM[key] = x\n    return x\n", 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
