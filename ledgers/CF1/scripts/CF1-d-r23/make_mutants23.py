"""Write three new student-error mutants of the CF1 reference (round 23, slice d)."""
import pathlib
REF = pathlib.Path("/tmp/verify23-CF1-d/course/modules/CF/CF1/grader/reference.py")
OUT = pathlib.Path("/tmp/verify23-CF1-d/ledgers/CF1/mutants")
src = REF.read_text()
muts = {
    "r23d_01_working_capital_released_one_year_late.py": (
        "Working capital is released one year late: the balance is held one year past the last year of the project.",
        "    for t in range(1, life):\n        nwc[t] = share * revenue[t - 1]\n",
        "    for t in range(1, life + 1):\n        nwc[t] = share * revenue[min(t - 1, life - 1)]\n",
    ),
    "r23d_02_irr_search_window_too_narrow.py": (
        "The IRR search window is narrowed to x in [1e-2, 1e2], so roots with rates beyond about -0.99 or 99 are missed.",
        "_X_LOW, _X_HIGH = 1e-4, 1e4\n",
        "_X_LOW, _X_HIGH = 1e-2, 1e2\n",
    ),
    "r23d_03_last_year_depreciation_shield_dropped.py": (
        "The tax shield on depreciation is dropped in the last year of life, so the final year is taxed as if no depreciation applied.",
        "        tax = tax_rate * (ebitda - depreciation)\n",
        "        tax = tax_rate * (ebitda - (depreciation if t < life else 0.0))\n",
    ),
}
for name, (doc, old, new) in muts.items():
    assert src.count(old) == 1, name
    text = src.replace(old, new, 1)
    text = text.replace('"""', '"""', 1)
    lines = text.split("\n", 1)
    # Replace the module docstring line with a one-line description of the error.
    first_end = text.index('"""', 3) + 3 if text.startswith('"""') else 0
    body = text[first_end:] if first_end else text
    (OUT / name).write_text(f'"""{doc}"""\n' + body)
    print("wrote", name)
