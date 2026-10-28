"""Generate round-4 student-error mutants from grader/reference.py. Each replacement must match exactly once."""
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
src = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text()
OUT = ROOT / "ledgers/AC4/mutants"
MUTANTS = {
    "m21_missing_product_field_defaults_to_zero": [(
        '        for field in PRODUCT_FIELDS:\n            if field not in item:\n                raise ValueError(f"a product has no {field!r} field")\n',
        '        for field in PRODUCT_FIELDS:\n            item = {**item, field: item.get(field, 0)} if field not in item else item\n',
    )],
    "m22_negative_budget_price_accepted": [(
        '"budget_price_cents": _nonnegative(item["budget_price_cents"], f"{name} budget_price_cents"),',
        '"budget_price_cents": _whole(item["budget_price_cents"], f"{name} budget_price_cents"),',
    )],
    "m23_negative_standard_inputs_accepted": [(
        '"standard_inputs_per_unit": _nonnegative(',
        '"standard_inputs_per_unit": _whole(',
    )],
    "m24_missing_input_price_defaults_to_zero": [(
        'CASE_FIELDS = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")',
        'CASE_FIELDS = ("fixed_overhead_cents", "actual_inputs_used", "products")',
    ), (
        '    input_price = _nonnegative(case["input_price_cents"], "input_price_cents")',
        '    input_price = _nonnegative(case.get("input_price_cents", 0), "input_price_cents")',
    )],
}
for name, reps in MUTANTS.items():
    text = src
    for old, new in reps:
        n = text.count(old)
        assert n == 1, (name, n)
        text = text.replace(old, new)
    (OUT / f"{name}.py").write_text(text)
    print("wrote", name)
