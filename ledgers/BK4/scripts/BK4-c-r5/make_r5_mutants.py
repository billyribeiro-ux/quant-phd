"""Writes the round-5 student-error mutants of the BK4 reference into ledgers/BK4/mutants/.

Each mutant is reference.py with one change. The script refuses to write a mutant whose replacement does not match
exactly once in the reference, so a stale anchor cannot produce a mutant that equals the reference.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = ROOT / "course/modules/BK/BK4/grader/reference.py"
OUT = ROOT / "ledgers/BK4/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "r5a_leftover_rotates_from_the_defaulter.py": (
        "Student error: the leftover cents start at the member after the defaulter and wrap around, not at the lowest id.",
        [
            (
                "        for member in survivors:\n            if leftover == 0:\n                break\n",
                "        rotated = [m for m in sorted(default_fund_cents) if m > defaulter_id]\n"
                "        rotated += [m for m in sorted(default_fund_cents) if m < defaulter_id]\n"
                "        for member in rotated:\n            if leftover == 0:\n                break\n",
            )
        ],
    ),
    "r5b_sizing_clamps_target_above_10000.py": (
        "Student error: a target above 10000 bps is clamped to full cover instead of refused with ValueError.",
        [
            (
                '    if not 1 <= target_bps <= 10_000:\n        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")\n',
                "    target_bps = min(target_bps, 10_000)\n"
                "    if not 1 <= target_bps:\n"
                '        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")\n',
            )
        ],
    ),
    "r5c_sizing_drops_zero_losses_before_counting.py": (
        "Student error: scenarios with a zero loss are dropped before the sizing, so the count S excludes them.",
        [
            (
                "    count = len(losses_cents)\n    index = -((-target_bps * count) // 10_000)\n    return sorted(losses_cents)[index - 1]\n",
                "    kept = [loss for loss in losses_cents if loss > 0]\n"
                "    if not kept:\n"
                "        return 0\n"
                "    count = len(kept)\n"
                "    index = -((-target_bps * count) // 10_000)\n"
                "    return sorted(kept)[index - 1]\n",
            )
        ],
    ),
    "r5d_cover_denominator_excludes_zero_losses.py": (
        "Student error: the cover divides by the number of positive losses, so zero-loss scenarios leave the denominator.",
        [
            (
                "    return 10_000 * covered // len(losses_cents)\n",
                "    positive = sum(1 for loss in losses_cents if loss > 0)\n"
                "    if positive == 0:\n"
                "        return 0\n"
                "    return 10_000 * covered // positive\n",
            )
        ],
    ),
    "r5e_refuses_a_zero_default_fund.py": (
        "Student error: a default fund of zero is refused as invalid, although the page lets a survivor with DF_i = 0 pay zero.",
        [
            (
                '    for member, amount in default_fund_cents.items():\n        if amount < 0:\n',
                '    for member, amount in default_fund_cents.items():\n        if amount <= 0:\n',
            )
        ],
    ),
    "r5f_sizing_index_uses_count_minus_one.py": (
        "Student error: the sizing index uses S - 1 scenarios, one fewer than the S scenarios the page counts.",
        [
            (
                "    count = len(losses_cents)\n    index = -((-target_bps * count) // 10_000)\n",
                "    count = len(losses_cents) - 1\n    index = -((-target_bps * count) // 10_000)\n",
            )
        ],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    for name, (description, edits) in MUTANTS.items():
        text = source
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: anchor matched {count} times, expected 1")
            text = text.replace(old, new)
        # The reference's module docstring is replaced by one line that names the student error.
        doc_end = text.index('"""', text.index('"""') + 3) + 3
        module = f'"""{description}"""\n' + text[doc_end:]
        (OUT / name).write_text(module, encoding="utf-8")
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
