# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Write the round-2 student-error mutants p08..p13 (AC2 project) from the course reference.

Each mutant is the reference module with exactly one textual change; the script asserts that the change applied.
Usage (from the repository root): .venv/bin/python ledgers/AC2/scripts/project-r2/make_mutants_r2.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/AC/AC2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/AC2/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "p08_rank_checks_only_zero_columns.py": (
        "p08: the rank test only rejects an all-zero regressor column; a linearly dependent design (two regressors "
        "proportional to each other) is not rejected and the fit is returned.",
        [
            (
                "    unit_columns = design / norms  # the rank test must not depend on the regressors' units\n"
                "    s = np.linalg.svd(unit_columns, compute_uv=False)\n"
                "    if s[-1] <= _RANK_TOL * s[0]:\n"
                '        raise ValueError("the design matrix is rank-deficient: the three regressors must be linearly independent")\n',
                "",
            )
        ],
    ),
    "p09_piotroski_roa_signal_weak_inequality.py": (
        "p09: Piotroski signal 1 tests ROA >= 0 (weak) instead of ROA > 0 (strict), so a zero ROA scores 1.",
        [("        int(roa > 0.0),\n", "        int(roa >= 0.0),\n")],
    ),
    "p10_tag_priority_last_tag_wins.py": (
        "p10: the tag priority is read backwards: the last tag in the list that has a value supplies the item.",
        [
            (
                "        for tag in TAG_PRIORITY[item]:\n"
                "            for key, candidate in best_by_tag.get(tag, {}).items():\n",
                "        for tag in reversed(TAG_PRIORITY[item]):\n"
                "            for key, candidate in best_by_tag.get(tag, {}).items():\n",
            )
        ],
    ),
    "p11_modified_jones_fit_with_intercept_returns_slopes.py": (
        "p11: modified_jones adds a constant column (an intercept) to the regression and returns only the three "
        "slope coefficients, so the fitted and discretionary parts are the intercept model's.",
        [
            (
                "    design = np.column_stack([1.0 / lag, (data[:, 2] - data[:, 3]) / lag, data[:, 4] / lag])\n",
                "    design = np.column_stack([np.ones_like(lag), 1.0 / lag, (data[:, 2] - data[:, 3]) / lag, data[:, 4] / lag])\n",
            ),
            (
                '        "coefficients": tuple(float(c) for c in coef),\n',
                '        "coefficients": tuple(float(c) for c in coef[1:]),\n',
            ),
        ],
    ),
    "p12_balance_sheet_accruals_adds_depreciation.py": (
        "p12: accruals_balance_sheet subtracts the depreciation with the wrong sign (adds it back).",
        [
            (
                "    numerator = (d_current_assets - d_cash) - d_current_liabilities - depreciation\n",
                "    numerator = (d_current_assets - d_cash) - d_current_liabilities + depreciation\n",
            )
        ],
    ),
    "p13_as_of_tie_on_filing_date_keeps_first_listed.py": (
        "p13: the as-of selection orders candidates by filing date only and keeps the first listed on a tie, so a "
        "10-K/A filed on the same day as the original (larger accn) does not supersede it.",
        [
            (
                "                options.sort(key=lambda c: (c[0], c[1]), reverse=True)\n",
                "                options.sort(key=lambda c: c[0], reverse=True)\n",
            ),
        ],
    ),
}


def main() -> None:
    for name, (doc, edits) in MUTANTS.items():
        text = REF
        for old, new in edits:
            assert text.count(old) == 1, f"{name}: edit target not found exactly once"
            text = text.replace(old, new)
        head, sep, rest = text.partition('"""\n')
        assert sep, "the reference opens with a docstring"
        text = f'"""{doc}"""\n' + rest
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
