"""Write two verifier mutants of grader/reference.py that are not single-span replacements (BK4-c r1).

vc10_float_arithmetic: integer arithmetic replaced by float division (int of a float share, math.ceil of a float index).
    Stated behaviour violated: project.html Constraints ("every computation is integer arithmetic ... no float") and plan 2.1 item 8.
unstated_mutants/vc11_sorts_argument_in_place: margin_for_cover sorts the caller's list. This is kept OUTSIDE mutants/
    because the behaviour appears only in starter.py's docstring, not on project.html or in the plan (FINAL-ARCHITECT-RULINGS 9).
Run: .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/make_float_and_unstated_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "BK" / "BK4" / "grader" / "reference.py"
MUT = ROOT / "ledgers" / "BK4" / "mutants"
UNSTATED = ROOT / "ledgers" / "BK4" / "scripts" / "BK4-c-r1" / "unstated_mutants"


def body_of(ref: str) -> str:
    return ref[ref.index('"""', 3) + 3 :]


def write(path: Path, description: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'"""{description}\n\nA single-change family copy of grader/reference.py (verifier BK4-c, round 1).\n"""' + body, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    float_body = body_of(ref)
    reps = [
        ("from dataclasses import dataclass\n", "from dataclasses import dataclass\nimport math\n"),
        (
            "            survivor_cents[member] = residual * default_fund_cents[member] // total_fund",
            "            survivor_cents[member] = int(residual * default_fund_cents[member] / total_fund)",
        ),
        ("    index = -((-target_bps * count) // 10_000)", "    index = math.ceil(target_bps * count / 10_000)"),
    ]
    for old, new in reps:
        assert float_body.count(old) == 1, old
        float_body = float_body.replace(old, new)
    write(
        MUT / "vc10_float_arithmetic.py",
        "Student error: integer arithmetic replaced by float division (int of a float share, math.ceil of a float index), "
        "exact on small cents but not above 2**53.",
        float_body,
    )
    unstated = body_of(ref)
    old = "    return sorted(losses_cents)[index - 1]"
    assert unstated.count(old) == 1
    unstated = unstated.replace(old, "    losses_cents.sort()\n    return losses_cents[index - 1]")
    write(
        UNSTATED / "vc11_sorts_argument_in_place.py",
        "Student error: margin_for_cover sorts the caller's list in place, so the call changes the scenario losses.",
        unstated,
    )


if __name__ == "__main__":
    main()
