"""Write ten student-error mutants of the M7 reference into ledgers/M7/mutants/ (round 6, slice d, fixer).

Each mutant is grader/reference.py with replaced texts; every search text must occur exactly once.
The ten cover the enumerated classes of the page's named conditions at every asset position (asset 0, 1, 2 and the
last asset): the box and order checks, the sector label type and range, the sector cap, the non-mapping type, the
lower-bound boundary, the wrong-type check of the numeric entries.
Usage: python3 make_fixer_mutants_r6.py <checkout-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "p01_start_box_checked_for_asset_0_only": (
        "Student error p01: the starting weight is checked against its box for asset 0 only.",
        [
            (
                "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):",
                "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(1)):",
            )
        ],
    ),
    "p02_bound_order_checked_for_asset_0_only": (
        "Student error p02: a lower bound above its upper bound is refused for asset 0 only.",
        [("    if any(lower[i] > upper[i] for i in range(n)):", "    if any(lower[i] > upper[i] for i in range(1)):")],
    ),
    "p03_boolean_sector_label_accepted": (
        "Student error p03: a boolean sector label is accepted, because True counts as the integer one.",
        [
            (
                "        if isinstance(label, bool) or not isinstance(label, int):",
                "        if not isinstance(label, int):",
            )
        ],
    ),
    "p04_float_sector_label_accepted_at_last_asset": (
        "Student error p04: a float sector label is accepted at the last asset and truncated to an integer.",
        [
            (
                "        if isinstance(label, bool) or not isinstance(label, int):",
                "        if (isinstance(label, bool) or not isinstance(label, int)) and label is not raw_sector[-1]:",
            ),
            ("        sector.append(label)", "        sector.append(int(label))"),
        ],
    ),
    "p05_numeric_type_checked_for_first_entries_only": (
        "Student error p05: a boolean or text entry is refused only where its name ends in index 0; elsewhere it is "
        "read as a number.",
        [
            (
                "    if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
                '        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")',
                '    if (isinstance(value, bool) or not isinstance(value, (int, float))) and name.endswith("[0]"):\n'
                '        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")',
            )
        ],
    ),
    "p06_sector_cap_checked_for_first_sector_only": (
        "Student error p06: the starting portfolio is checked against the sector cap of sector 0 only.",
        [
            (
                "    for k, cap in enumerate(caps):\n        if sum(w0[i]",
                "    for k, cap in enumerate(caps[:1]):\n        if sum(w0[i]",
            )
        ],
    ),
    "p07_non_mapping_raises_type_error": (
        "Student error p07: an instance that is not a mapping raises TypeError, where the page names ValueError.",
        [
            (
                '        raise ValueError("the instance must be a mapping with the case fields")',
                '        raise TypeError("the instance must be a mapping with the case fields")',
            )
        ],
    ),
    "p08_lower_bound_equal_to_start_refused": (
        "Student error p08: a lower bound equal to the starting weight is refused as if the start lay below it.",
        [
            (
                "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):",
                "    if any(w0[i] < lower[i] + TOL or w0[i] > upper[i] + TOL for i in range(n)):",
            )
        ],
    ),
    "p09_starting_box_skips_asset_1": (
        "Student error p09: the starting-portfolio box check skips the middle asset, asset 1.",
        [
            (
                "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):",
                "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n) if i != 1):",
            )
        ],
    ),
    "p10_sector_labels_checked_except_the_last_asset": (
        "Student error p10: the sector-label loop stops one short, so the last asset's label is never checked.",
        [("    for label in raw_sector:", "    for label in raw_sector[:-1]:")],
    ),
}


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    for name, (description, replacements) in MUTANTS.items():
        text = source
        for old, new in replacements:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: search text occurs {count} times: {old!r}")
            text = text.replace(old, new)
        _, _, rest = text.partition('"""')
        _, _, body = rest.partition('"""')
        mutant = (
            f'"""{description}\n\nOne change to grader/reference.py, written by the M7 fixer (round 6, slice d).\n"""'
            + body
        )
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
