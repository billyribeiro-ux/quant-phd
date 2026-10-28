"""Generate round-5 student-error mutants (m25-m29) from grader/reference.py. Each replacement must match exactly once."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
src = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text()
OUT = ROOT / "ledgers/AC4/mutants"
MASTER_HEAD = "def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:\n"
MUTANTS = {
    # case-level required field actual_inputs_used treated as optional (defaults to 0)
    "m25_missing_actual_inputs_defaults_to_zero": [(
        'CASE_FIELDS = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")',
        'CASE_FIELDS = ("input_price_cents", "fixed_overhead_cents", "products")',
    ), (
        '    actual_inputs = _nonnegative(case["actual_inputs_used"], "actual_inputs_used")',
        '    actual_inputs = _nonnegative(case.get("actual_inputs_used", 0), "actual_inputs_used")',
    )],
    # master_budget alone tolerates a negative input price (the check is applied only in variance_decomposition's path)
    "m26_master_accepts_negative_input_price": [(
        '    input_price, fixed, _, products = _case(case)\n    units = {',
        '    if isinstance(case, Mapping) and isinstance(case.get("input_price_cents"), int) and case["input_price_cents"] < 0:\n'
        '        case = {**case, "input_price_cents": 0}\n'
        '    input_price, fixed, _, products = _case(case)\n    units = {',
    )],
    # master_budget returns one cached object on every call after the first
    "m27_master_returns_cached_object": [(
        MASTER_HEAD,
        "def _master_fresh(case: Mapping[str, Any]) -> dict[str, Any]:\n",
    )],
    # a debugging print left in flexible_budget
    "m28_debug_print_left_in_flexible_budget": [(
        '    total = _nonnegative(actual_units, "actual_units")\n',
        '    total = _nonnegative(actual_units, "actual_units")\n    print("flexed total", total)\n',
    )],
    # master_budget writes a marker into the caller's case
    "m29_master_marks_the_argument": [(
        '    input_price, fixed, _, products = _case(case)\n    units = {',
        '    input_price, fixed, _, products = _case(case)\n    case["_seen"] = True  # type: ignore[index]\n    units = {',
    )],
}
APPENDIX = (
    "\n\n_CACHED: list[dict[str, Any]] = []\n\n"
    "def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:\n"
    "    if not _CACHED:\n        _CACHED.append(_master_fresh(case))\n    return _CACHED[0]\n"
)
for name, reps in MUTANTS.items():
    text = src
    for old, new in reps:
        n = text.count(old)
        assert n == 1, (name, n)
        text = text.replace(old, new)
    if name.startswith("m27"):
        text += APPENDIX
    (OUT / f"{name}.py").write_text(text)
    print("wrote", name)
