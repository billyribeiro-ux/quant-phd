"""Verifier scratch: the two proposed grader tests that kill vd3_01..vd3_04 (appended to a copy of test_project.py; not in the repository)."""

# --- verifier scratch: proposed fix checks (not in the repository)


def test_fix_inputs_not_mutated_by_scalar_functions() -> None:
    near = symmetric_pair(CORR_AT_IMPORT, 0, 1, 1e-10)
    before = copy.deepcopy(near)
    sol.min_eigenvalue(near)
    assert near == before, "min_eigenvalue must not change its argument"
    sol.is_psd(near)
    assert near == before, "is_psd must not change its argument"
    sol.comparison_weights(near, VOLS_AT_IMPORT)
    assert near == before, "comparison_weights must not change its correlation matrix"


def test_fix_std_lib_and_numpy_imports_only() -> None:
    import ast
    import sys

    with open(sol.__file__, encoding="utf-8") as fh:
        src = fh.read()
    allowed = set(sys.stdlib_module_names) | {"numpy"}
    bad = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            bad |= {a.name.split(".")[0] for a in node.names} - allowed
        elif isinstance(node, ast.ImportFrom) and node.module:
            bad |= {node.module.split(".")[0]} - allowed
    assert not bad, "only the standard library and NumPy may be imported"
