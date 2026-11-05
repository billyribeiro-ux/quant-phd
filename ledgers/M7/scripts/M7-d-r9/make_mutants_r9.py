"""Round 9: write five new student-error mutants (complete modules) into ledgers/M7/mutants/, each from the reference solution."""
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-M7-d")
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"

ALLOCATE_OLD = """def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    sol = _solve(problem)
"""
assert REF.count(ALLOCATE_OLD) == 1
RETURN_OLD = """    return {
        "weights": [float(v) for v in sol["w"]],"""
assert REF.count(RETURN_OLD) == 1


def build(name: str, doc: str, head_insert: str = "", after_solve: str = "", imports: str = "") -> None:
    text = REF
    if imports:
        text = text.replace("from __future__ import annotations\n", "from __future__ import annotations\n" + imports, 1)
    text = text.replace(
        ALLOCATE_OLD,
        ALLOCATE_OLD.replace("    problem = _parse(instance)\n", head_insert + "    problem = _parse(instance)\n") + after_solve,
        1,
    )
    text = '"""' + doc + '"""\n' + text.split('"""', 2)[2]
    (OUT / name).write_text(text, encoding="utf-8")


build(
    "v9_01_prints_a_trace_when_turnover_binds.py",
    "Student error v9_01: allocate prints a trace line whenever the turnover limit binds (within 1e-9), a debugging print left in.",
    after_solve='''    if abs(sum((abs(a - b) for a, b in zip(sol["w"], problem.w0)), Fraction(0)) - problem.tau) <= TOL:
        print("turnover binds at", len(sol["w"]), "assets")
''',
)
build(
    "v9_02_prints_a_trace_only_for_five_asset_binding_turnover.py",
    "Student error v9_02: allocate prints a trace line only for a five-asset case in which the turnover limit binds.",
    after_solve='''    if problem.n == 5 and abs(sum((abs(a - b) for a, b in zip(sol["w"], problem.w0)), Fraction(0)) - problem.tau) <= TOL:
        print("five assets, turnover binds")
''',
)
build(
    "v9_03_warns_when_a_bound_pair_is_degenerate.py",
    "Student error v9_03: allocate emits a warning for a degenerate box (a lower bound equal to its upper bound), and the answer is unchanged.",
    after_solve='''    if any(problem.lower[i] == problem.upper[i] for i in range(problem.n)):
        warnings.warn("degenerate box", stacklevel=2)
''',
    imports="import warnings\n",
)
build(
    "v9_04_adds_a_note_key_to_its_argument_for_degenerate_boxes.py",
    "Student error v9_04: allocate stores a note in its argument when a lower bound equals its upper bound (a cache left in the caller's case).",
    head_insert='''    if any(instance["lower"][i] == instance["upper"][i] for i in range(len(instance["lower"]))):
        instance["note"] = "degenerate box"
''',
)
build(
    "v9_05_second_call_negates_the_budget_multiplier.py",
    "Student error v9_05: allocate returns a different budget multiplier on every second call with the same case (a module-level counter left in).",
    after_solve='''    _CALLS[0] += 1
    if _CALLS[0] % 2 == 0:
        sol["budget"] = -sol["budget"]
''',
)
# prepend the counter used by v9_05
p = OUT / "v9_05_second_call_negates_the_budget_multiplier.py"
p.write_text(p.read_text(encoding="utf-8").replace("def _parse(", "_CALLS = [0]\n\n\ndef _parse(", 1), encoding="utf-8")
