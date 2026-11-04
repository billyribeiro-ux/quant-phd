"""Write the verifier's student-error mutants of grader/reference.py (BK4-c, round 1).

Each mutant is the reference with exactly one replaced span; the replacement must match exactly once.
Run: .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/make_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "BK" / "BK4" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "BK4" / "mutants"

MUTANTS: dict[str, tuple[str, str, str]] = {
    "vc01_cover_rounded": (
        "Student error: the cover is rounded to the nearest basis point instead of floored.",
        "    return 10_000 * covered // len(losses_cents)",
        "    return (20_000 * covered + len(losses_cents)) // (2 * len(losses_cents))",
    ),
    "vc02_zero_based_index": (
        "Student error: the sizing reads the zero-based position k instead of the k-th smallest loss (k - 1).",
        "    return sorted(losses_cents)[index - 1]",
        "    return sorted(losses_cents)[index]",
    ),
    "vc03_sizing_unsorted": (
        "Student error: the sizing picks the k-th loss as given, without sorting the scenarios first.",
        "    return sorted(losses_cents)[index - 1]",
        "    return losses_cents[index - 1]",
    ),
    "vc04_cover_no_refusal": (
        "Student error: cover_bps accepts a negative loss without raising, so the named refusal is missing.",
        "    _no_negative_losses(losses_cents)\n    covered = sum(",
        "    covered = sum(",
    ),
    "vc05_target_zero_allowed": (
        "Student error: the target range check starts at 0, so a target of 0 bps is accepted and silently sized.",
        "    if not 1 <= target_bps <= 10_000:",
        "    if not 0 <= target_bps <= 10_000:",
    ),
    "vc06_fund_without_min": (
        "Student error: the default fund pays its full contribution even when the loss is smaller, so layers overpay.",
        "    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])",
        "    fund_paid = default_fund_cents[defaulter_id]",
    ),
    "vc07_leftover_to_zero_fund": (
        "Student error: the leftover cent goes to a survivor with a zero default fund, skipping the DF > 0 rule.",
        "            if default_fund_cents[member] > 0:\n                survivor_cents[member] += 1",
        "            if True:\n                survivor_cents[member] += 1",
    ),
    "vc08_index_plus_one": (
        "Student error: the sizing index is floor(target times count / 10000) plus one, an off-by-one at exact positions.",
        "    index = -((-target_bps * count) // 10_000)",
        "    index = (target_bps * count) // 10_000 + 1",
    ),
    "vc09_capital_ignored": (
        "Student error: the CCP capital is left out of the waterfall, so the survivors pay the capital's share.",
        "    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents)",
        "    capital_paid = 0",
    ),
}


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    head_end = ref.index('"""', 3) + 3
    body = ref[head_end:]
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (description, old, new) in MUTANTS.items():
        count = body.count(old)
        assert count == 1, f"{name}: the span must match exactly once, found {count}"
        mutated = body.replace(old, new)
        assert mutated != body, f"{name}: no change"
        text = f'"""{description}\n\nA single-change copy of grader/reference.py (verifier BK4-c, round 1).\n"""' + mutated
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
