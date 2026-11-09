"""Write the round-16 verifier's student-error mutants of the BK4 reference (slice c).

Each mutant is reference.py with one replacement; every replacement must match exactly once (asserted).
Usage: python -I make_mutants_r16.py <checkout-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
REF = (ROOT / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/BK4/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "r16a_target_message_omits_target_bps.py": (
        "Student error: the target refusal says the target is out of range but does not name target_bps, so the learner cannot see which input failed.",
        [
            (
                'raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")',
                'raise ValueError(f"the target must be in the range 1 to 10000, not {target_bps}")',
            )
        ],
    ),
    "r16b_defaulter_margin_read_at_zero_based_index.py": (
        "Student error: the defaulter's initial margin is read at key defaulter_id - 1, a zero-based position applied to the one-based member ids.",
        [
            (
                "margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])",
                "margin_paid = min(loss_cents, initial_margin_cents[defaulter_id - 1])",
            )
        ],
    ),
    "r16c_default_fund_ignores_the_margin_already_paid.py": (
        "Student error: the defaulter's default fund is capped at the full loss instead of at the loss the margin left, so the fund can pay what the margin already paid.",
        [
            (
                "fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])",
                "fund_paid = min(loss_cents, default_fund_cents[defaulter_id])",
            )
        ],
    ),
    "r16d_loss_refusal_message_omits_loss_cents.py": (
        "Student error: the negative-loss refusal in waterfall words the message without naming loss_cents, so the learner cannot tell which input was negative.",
        [
            (
                'raise ValueError(f"loss_cents is negative, and a loss cannot be negative: {loss_cents}")',
                'raise ValueError(f"a loss cannot be negative: {loss_cents}")',
            )
        ],
    ),
    "r16e_cover_sorts_the_callers_list_in_place.py": (
        "Student error: cover_bps sorts the caller's scenario list in place before counting, so the list the caller passed is reordered.",
        [
            (
                "    _no_negative_losses(losses_cents)\n    covered = sum(",
                "    _no_negative_losses(losses_cents)\n    losses_cents.sort()\n    covered = sum(",
            )
        ],
    ),
}

for name, (first_line, replacements) in MUTANTS.items():
    text = REF
    for old, new in replacements:
        count = text.count(old)
        assert count == 1, f"{name}: expected one match, found {count} for {old!r}"
        text = text.replace(old, new)
    header = (
        f'"""{first_line}\n\n'
        "Verifier-written mutant (round 16, slice c) of the reference, for the BK4 grader. Not a solution.\n"
        '"""\n'
    )
    body = text.split('"""', 2)[2].lstrip("\n")
    (OUT / name).write_text(header + "\n" + body, encoding="utf-8")
    print("wrote", name)
