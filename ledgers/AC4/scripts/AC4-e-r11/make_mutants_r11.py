"""Write the round-11 student-error mutants m52-m55 from the grader's reference (each edit must match exactly once).

Each mutant opens with a one-line docstring naming the error, as tools/mutate_graders.py requires."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
REF = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/AC4/mutants"
HEAD = '"""Reference solution for the AC4 budget and variance engine (budget_engine.py).'
MUTANTS = {
    "m52_case_must_be_a_dict.py": (
        "Student error: the case is refused unless it is a dict, so a valid non-dict Mapping is refused.",
        [('if not isinstance(case, Mapping):\n        raise ValueError("the case must be a mapping',
          'if not isinstance(case, dict):\n        raise ValueError("the case must be a mapping')]),
    "m53_variable_cost_rounds_half_down.py": (
        "Student error: the flexed variable cost is rounded half down, against the page's halves-up rule.",
        [("variable = _nearest_cent(Fraction(total * budget_variable, budget_units))",
          "variable = -_nearest_cent(-Fraction(total * budget_variable, budget_units))")]),
    "m54_any_zero_budget_product_refused.py": (
        "Student error: a product with zero budgeted units is refused, though only a zero budget total is refused.",
        [("        if name in seen:",
          '        if item["budget_units"] == 0:\n            raise ValueError("a product has no budgeted units")\n'
          "        if name in seen:")]),
    "m55_mix_sign_flipped.py": (
        "Student error: the sales mix variance is the flexed profit less the actual-mix contribution, the wrong sign.",
        [("sales_mix = actual_mix_contribution - flexed", "sales_mix = flexed - actual_mix_contribution")]),
}
for name, (description, edits) in MUTANTS.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, text.count(old), old[:60])
        text = text.replace(old, new)
    assert text.count(HEAD) == 1, name
    text = text.replace(HEAD, '"""' + description + "\n\n" + HEAD[3:], 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
