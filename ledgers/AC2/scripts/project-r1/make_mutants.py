# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Write the verifier's own student-error mutants of the AC2 reference into ledgers/AC2/mutants/ (project slice).

Usage (from the repository root): .venv/bin/python ledgers/AC2/scripts/project-r1/make_mutants.py

Each mutant is the course's reference.py with one plausible student error applied by exact string replacement. Every
replacement must match exactly once (asserted), so each mutant differs from the reference in one place. The module
docstring's first line describes the error (tools/mutate_graders.py reads it).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "AC" / "AC2" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "AC2" / "mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "p01_previous_year_without_the_350_380_window": (
        "MUTANT p01: previous year is the latest earlier period end, without the 350 to 380 day window.",
        [
            (
                "        if _YEAR_MIN <= (t - e).days <= _YEAR_MAX and (best is None or e > best):",
                "        if e < t and (best is None or e > best):",
            ),
        ],
    ),
    "p02_annual_duration_narrowed_to_360_370_days": (
        "MUTANT p02: a flow item counts as annual only for a duration of 360 to 370 days (window narrowed).",
        [
            (
                "        return start is not None and _YEAR_MIN <= (end - start).days <= _YEAR_MAX",
                "        return start is not None and 360 <= (end - start).days <= 370",
            ),
        ],
    ),
    "p03_ratio_result_not_checked_for_finiteness": (
        "MUTANT p03: a ratio whose result overflows to infinity is returned instead of raising ValueError.",
        [
            (
                '    if not math.isfinite(result):\n        raise ValueError(f"the result for {name} is not finite")\n',
                "",
            ),
        ],
    ),
    "p04_piotroski_cfo_scaled_by_year_end_assets": (
        "MUTANT p04: Piotroski CFO_t is scaled by year-end total assets instead of beginning-of-year assets.",
        [
            (
                '    cfo = _div(_get(statements, t, "cfo"), ta_t1, "total assets of the previous year")',
                '    cfo = _div(_get(statements, t, "cfo"), ta_t, "total assets of the period end")',
            ),
        ],
    ),
    "p06_missing_val_taken_as_zero": (
        "MUTANT p06: an observation without a val is taken as zero instead of raising ValueError.",
        [
            (
                '    for key in ("end", "val", "filed", "form"):',
                '    for key in ("end", "filed", "form"):',
            ),
            (
                '    value = _number(obs["val"], f"val of an observation of {tag}")',
                '    value = _number(obs.get("val", 0.0), f"val of an observation of {tag}")',
            ),
        ],
    ),
    "p07_prior_year_balance_filled_from_current_year": (
        "MUTANT p07: a missing previous-year total assets or equity is filled from the current year in DuPont.",
        [
            (
                '    avg_assets = _average(_get(statements, end, "total_assets"), _get(statements, prev, "total_assets"))\n'
                '    avg_equity = _average(_get(statements, end, "equity"), _get(statements, prev, "equity"))\n'
                "    return {",
                '    prev_ta = _get(statements, prev, "total_assets") if "total_assets" in statements[prev] else _get(statements, end, "total_assets")\n'
                '    prev_eq = _get(statements, prev, "equity") if "equity" in statements[prev] else _get(statements, end, "equity")\n'
                '    avg_assets = _average(_get(statements, end, "total_assets"), prev_ta)\n'
                '    avg_equity = _average(_get(statements, end, "equity"), prev_eq)\n'
                "    return {",
            ),
        ],
    ),
    "p05_as_of_cut_excludes_a_filing_made_on_the_as_of_date": (
        "MUTANT p05: the as-of cut-off is exclusive: a filing made on the as-of date is not yet known.",
        [
            (
                "            if cutoff is not None and filed > cutoff:",
                "            if cutoff is not None and filed >= cutoff:",
            ),
        ],
    ),
}


def build() -> None:
    source = REF.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (description, replacements) in MUTANTS.items():
        text = source
        for old, new in replacements:
            hits = text.count(old)
            assert hits == 1, f"{name}: the replacement matches {hits} times"
            text = text.replace(old, new)
        assert text.startswith('"""Reference solution'), f"{name}: unexpected reference header"
        text = '"""' + description + "\n\n" + text[3:]
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", (OUT / f"{name}.py").relative_to(ROOT))


if __name__ == "__main__":
    build()
