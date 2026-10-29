import pathlib
ref = pathlib.Path("course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path("ledgers/M4/mutants")
specs = [
    ("r12_01_cov_symmetry_tolerance_1e3.py",
     "Verifier round-12 student-error mutant: the symmetry check accepts an asymmetry up to 1e-3 absolute.",
     "            if cov[i][j] != cov[j][i]:", "            if abs(cov[i][j] - cov[j][i]) > 1e-3:"),
    ("r12_02_student_t_chi_square_scale_one.py",
     "Verifier round-12 student-error mutant: the chi-square draw uses scale 1 instead of 2 (wrong gamma scale).",
     "rng.gammavariate(nu / 2, 2.0)", "rng.gammavariate(nu / 2, 1.0)"),
    ("r12_03_quantile_index_floor_not_ceiling.py",
     "Verifier round-12 student-error mutant: the 99% index is floor(0.99 n), not its ceiling.",
     "index = (99 * len(losses_cents) + 99) // 100", "index = (99 * len(losses_cents)) // 100"),
    ("r12_04_pivot_tolerance_rejects_small_variance.py",
     "Verifier round-12 student-error mutant: a Cholesky pivot must exceed 1e-12, so a tiny positive variance is rejected.",
     "if not pivot > 0.0:", "if not pivot > 1e-12:"),
]
for name, doc, old, new in specs:
    assert ref.count(old) == 1, name
    head, body = ref.split('"""', 2)[1], ref.split('"""', 2)[2]
    src = '"""' + doc + "\n\nReference solution for the M4 project. All inputs are SIMULATED.\n" + '"""' + body
    src = src.replace(old, new)
    assert src != ref
    (out / name).write_text(src, encoding="utf-8")
    print("wrote", name)
