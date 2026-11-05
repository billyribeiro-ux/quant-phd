"""Round-9 student-error mutants of the BK4 reference, one line changed each (written to ledgers/BK4/mutants/)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/BK4/mutants"
HEAD = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'

MUTANTS = {
    "v9a_margin_for_cover_empty_returns_zero.py": (
        "Student error: margin_for_cover returns 0 for an empty scenario list instead of refusing it with ValueError.",
        '    if not losses_cents:\n        raise ValueError("at least one scenario is needed")\n    if not 1 <= target_bps',
        '    if not losses_cents:\n        return 0\n    if not 1 <= target_bps',
    ),
    "v9b_waterfall_always_prorates_the_residual.py": (
        "Student error: waterfall drops the branch for a residual at or above the pool, so survivors pay more than their whole default fund.",
        "    if residual >= total_fund:",
        "    if False:",
    ),
    "v9c_cover_bps_rounds_to_nearest.py": (
        "Student error: cover_bps rounds the cover to the nearest basis point instead of flooring it.",
        "    return 10_000 * covered // len(losses_cents)",
        "    return (2 * 10_000 * covered + len(losses_cents)) // (2 * len(losses_cents))",
    ),
    "v9d_margin_for_cover_scan_is_strict.py": (
        "Student error: margin_for_cover scans the distinct losses and compares the cover strictly above the target, so a cover that equals the target is never accepted.",
        "    return sorted(losses_cents)[index - 1]",
        "    for candidate in sorted(set(losses_cents)):\n"
        "        if 10_000 * sum(1 for loss in losses_cents if loss <= candidate) // count > target_bps:\n"
        "            return candidate\n"
        "    return sorted(losses_cents)[-1]",
    ),
    "v9e_waterfall_refuses_a_zero_defaulter_margin.py": (
        "Student error: waterfall refuses a defaulter whose initial margin is zero, which the page allows.",
        "    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])",
        '    if initial_margin_cents[defaulter_id] == 0:\n        raise ValueError("the defaulter has no margin")\n'
        "    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])",
    ),
}

for name, (summary, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new).replace(HEAD, f'"""{summary}\n\nMutant of the reference (round 9).', 1)
    assert text.startswith(f'"""{summary}')
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
