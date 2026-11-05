"""Writes four new student-error mutants of grader/reference.py (round 8, verifier-authored).

Each mutant is a complete clearing_house.py-shaped module. Each one-line change is asserted to occur exactly once,
so a mutant cannot silently equal the reference. Usage: make_r8_mutants.py <checkout>
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = ROOT / "course/modules/BK/BK4/grader/reference.py"
MUT = ROOT / "ledgers/BK4/mutants"

MUTANTS = {
    "t8a_shares_rounded_half_up.py": (
        "Student error: each survivor share is rounded half up to the nearest cent, not floored, so the shares can add to more than the residual.",
        "            survivor_cents[member] = residual * default_fund_cents[member] // total_fund\n",
        "            survivor_cents[member] = (2 * residual * default_fund_cents[member] + total_fund) // (2 * total_fund)\n",
    ),
    "t8b_cover_rounded_up.py": (
        "Student error: the cover is rounded up to the next basis point (a ceiling), not floored.",
        "    return 10_000 * covered // len(losses_cents)\n",
        "    return -((-10_000 * covered) // len(losses_cents))\n",
    ),
    "t8c_sizing_sorts_descending.py": (
        "Student error: the sizing sorts the losses in descending order and then takes the k-th entry, so it returns the k-th largest loss.",
        "    return sorted(losses_cents)[index - 1]\n",
        "    return sorted(losses_cents, reverse=True)[index - 1]\n",
    ),
    "t8d_capital_layer_skips_default_fund.py": (
        "Student error: the CCP capital layer is charged on the loss after the margin only, so the default fund is paid twice.",
        "    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents)\n",
        "    capital_paid = min(loss_cents - margin_paid, ccp_capital_cents)\n",
    ),
}

src = REF.read_text(encoding="utf-8")
for name, (summary, old, new) in MUTANTS.items():
    assert src.count(old) == 1, f"{name}: target line must occur exactly once in reference.py"
    body = src.replace(old, new)
    header_old = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'
    assert body.count(header_old) == 1
    body = body.replace(header_old, f'"""{summary}\n\nMutant of the reference (round 8).', 1)
    (MUT / name).write_text(body, encoding="utf-8")
    print(f"wrote {name}")

# Fifth mutant (added after the first run): the waterfall removes the defaulter from the caller's dictionary.
EXTRA = {
    "t8e_waterfall_pops_defaulter_from_argument.py": (
        "Student error: the waterfall removes the defaulter from the caller's default_fund_cents dictionary before it shares the residual.",
        "    survivors = sorted(member for member in default_fund_cents if member != defaulter_id)\n",
        "    default_fund_cents.pop(defaulter_id)\n    survivors = sorted(member for member in default_fund_cents)\n",
    ),
}
src = REF.read_text(encoding="utf-8")
for name, (summary, old, new) in EXTRA.items():
    assert src.count(old) == 1, f"{name}: target line must occur exactly once in reference.py"
    body = src.replace(old, new).replace(
        '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).',
        f'"""{summary}\n\nMutant of the reference (round 8).', 1)
    (MUT / name).write_text(body, encoding="utf-8")
    print(f"wrote {name}")
