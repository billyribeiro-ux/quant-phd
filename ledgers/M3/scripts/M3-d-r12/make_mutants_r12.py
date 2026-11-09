"""Round-12 verifier (M3 slice d): writes three new student-error mutants of grader/reference.py (verifier-written).

Each mutant is a complete solution module; the first docstring line names the student error. v12d_01/v12d_02 go to
ledgers/M3/mutants/ (killed by the suite). v12d_03 is a candidate survivor and is written to
ledgers/M3/scripts/M3-d-r12/survivors/ so that the gate's mutants directory stays free of survivors.
Run from the checkout root."""

import os

ROOT = os.getcwd()
REF = os.path.join(ROOT, "course/modules/M/M3/grader/reference.py")
ref = open(REF, encoding="utf-8").read()
HEADER_OLD = '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.'


def write(path: str, first_line: str, edits: list[tuple[str, str]]) -> None:
    text = ref
    assert text.count(HEADER_OLD) == 1
    text = text.replace(HEADER_OLD, f'"""{first_line}\n\nRound-12 verifier-written student-error mutant of grader/reference.py.', 1)
    for old, new in edits:
        assert text.count(old) == 1, (path, old)
        text = text.replace(old, new)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote", path)


write(
    os.path.join(ROOT, "ledgers/M3/mutants/v12d_01_projection_psd_step_reflects_negative_eigenvalues.py"),
    "_psd_projection reflects negative eigenvalues to their absolute values instead of setting them to zero.",
    [("return _rebuild([max(x, 0.0) for x in values], vectors)", "return _rebuild([abs(x) for x in values], vectors)")],
)
write(
    os.path.join(ROOT, "ledgers/M3/mutants/v12d_02_projection_unit_correction_from_previous_iterate.py"),
    "projection_repair forms the unit-diagonal correction term from the previous iterate instead of the new one.",
    [
        (
            "corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]",
            "corr_u = [[y[i][j] + corr_u[i][j] - x[i][j] for j in range(n)] for i in range(n)]",
        )
    ],
)
write(
    os.path.join(ROOT, "ledgers/M3/mutants/v12d_04_clip_clips_the_rescaled_matrix_not_the_input.py"),
    "clip_repair rescales first and clips the eigenvalues of the rescaled matrix, so the diagonal is no longer unit.",
    [
        (
            "    a = _as_matrix(matrix)\n    values, vectors = _eigh(a)\n    x = _rebuild([max(value, floor) for value in values], vectors)\n    return _rescale(x)",
            "    a = _as_matrix(matrix)\n    values, vectors = _eigh(a)\n    y = _rescale(_rebuild(values, vectors))\n    yvalues, yvectors = _eigh(y)\n    return _rebuild([max(value, floor) for value in yvalues], yvectors)",
        )
    ],
)
os.makedirs(os.path.join(ROOT, "ledgers/M3/scripts/M3-d-r12/survivors"), exist_ok=True)
write(
    os.path.join(ROOT, "ledgers/M3/scripts/M3-d-r12/survivors/v12d_03_clip_validates_symmetry_only_for_default_floor.py"),
    "clip_repair checks symmetry only when the floor is the default, so an asymmetric input with another floor is not refused.",
    [
        (
            "    a = _as_matrix(matrix)\n    values, vectors = _eigh(a)\n    x = _rebuild([max(value, floor) for value in values], vectors)\n    return _rescale(x)",
            "    a = _as_matrix(matrix) if floor == 0.0 else [[float(x) for x in row] for row in matrix]\n    values, vectors = _eigh(a)\n    x = _rebuild([max(value, floor) for value in values], vectors)\n    return _rescale(x)",
        )
    ],
)
