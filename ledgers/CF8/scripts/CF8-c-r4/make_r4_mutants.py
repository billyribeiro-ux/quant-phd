"""Generate the verifier's round-4 student-error mutants of the CF8 reference solution (verifier-authored)."""
import pathlib, sys
REF = pathlib.Path("course/modules/CF/CF8/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("ledgers/CF8/mutants")
MUTANTS = {
    "r4-01-shortfall-before-draw.py": (
        "Shortfall is measured before the draw, so every week below minimum before its draw counts as short.",
        [("    shortfall = max([0] + [max(0, minimum - row[\"ending_cash_cents\"]) for row in rows])",
          "    shortfall = max([0] + [max(0, minimum - (row[\"ending_cash_cents\"] - row[\"draw_cents\"] + row[\"repay_cents\"])) for row in rows])")],
    ),
    "r4-02-dso-window-recent-sales.py": (
        "DSO shortening moves the d most recent sales already collected, not the sales collected sooner after the change.",
        [("        window = range(DAYS_PER_WEEK * HORIZON - lag + 1, DAYS_PER_WEEK * HORIZON - lag + days + 1)",
          "        window = range(DAYS_PER_WEEK * HORIZON - lag + 1 - days, DAYS_PER_WEEK * HORIZON - lag + 1)")],
    ),
    "r4-03-dpo-window-inclusive-end.py": (
        "DPO lengthening also keeps the purchases paid exactly on day 91 after the change, one day too many.",
        [("        window = range(DAYS_PER_WEEK * HORIZON - lag - days + 1, DAYS_PER_WEEK * HORIZON - lag + 1)",
          "        window = range(DAYS_PER_WEEK * HORIZON - lag - days, DAYS_PER_WEEK * HORIZON - lag + 1)")],
    ),
}
for name, (doc, reps) in MUTANTS.items():
    src = REF
    for old, new in reps:
        assert src.count(old) == 1, (name, old[:60])
        src = src.replace(old, new)
    body = src.split('"""', 2)[2]  # keep module body after the docstring
    header = f'"""Mutant {name[:-3]}: {doc}"""\n'
    (OUT / name).write_text(header + body, encoding="utf-8")
    print("wrote", OUT / name)
