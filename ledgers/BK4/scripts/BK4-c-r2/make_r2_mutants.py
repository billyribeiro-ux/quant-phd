"""Write four new student-error mutants of reference.py (verifier BK4-c, round 2) into ledgers/BK4/mutants/.

Each mutant is reference.py with exactly one span changed; the first docstring line names the student error.
Usage (from the checkout root): .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/make_r2_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/BK/BK4/grader/reference.py"
OUT = ROOT / "ledgers/BK4/mutants"

REF_DOC = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'

MUTANTS: dict[str, tuple[str, str, str]] = {
    "vc12_pool_counts_the_defaulter_fund.py": (
        "Student error: the survivors' pool includes the defaulter's own default fund, so shares are cut by it.",
        "    total_fund = sum(default_fund_cents[member] for member in survivors)\n",
        "    total_fund = sum(default_fund_cents[member] for member in survivors) + default_fund_cents[defaulter_id]\n",
    ),
    "vc13_cover_of_no_scenarios_is_zero.py": (
        "Student error: cover_bps returns 0 for an empty scenario set instead of refusing it with ValueError.",
        '    if not losses_cents:\n        raise ValueError("at least one scenario is needed")\n    _no_negative_losses(losses_cents)\n    covered',
        '    if not losses_cents:\n        return 0\n    _no_negative_losses(losses_cents)\n    covered',
    ),
    "vc14_target_ten_thousand_refused.py": (
        "Student error: the target range check uses 9999 as its upper limit, so a full target of 10000 bps is refused.",
        "    if not 1 <= target_bps <= 10_000:",
        "    if not 1 <= target_bps <= 9_999:",
    ),
    "vc15_negative_capital_accepted.py": (
        "Student error: a negative CCP capital is not checked, so it is accepted and reduces the layers.",
        '    if ccp_capital_cents < 0:\n        raise ValueError(f"ccp_capital_cents is negative: {ccp_capital_cents}")\n',
        "",
    ),
}


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    assert ref.count(REF_DOC) == 1
    for name, (description, old, new) in MUTANTS.items():
        assert ref.count(old) == 1, f"{name}: span not found exactly once"
        text = ref.replace(REF_DOC, f'"""{description}', 1)
        text = text.replace(old, new, 1)
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
