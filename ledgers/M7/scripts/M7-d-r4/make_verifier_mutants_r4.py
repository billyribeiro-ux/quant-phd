"""Write three verifier-authored student-error mutants of the M7 reference into ledgers/M7/mutants/ (round 4, slice d).

Each mutant is grader/reference.py with one replaced text; every search text must occur exactly once.
Usage: python3 make_verifier_mutants_r4.py <checkout-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "x01_start_upper_bound_without_tolerance": (
        "Student error x01: the starting weight is compared with the upper bound without the 1e-9 tolerance.",
        [("w0[i] > upper[i] + TOL for i in range(n)):", "w0[i] > upper[i] for i in range(n)):")],
    ),
    "x02_sector_label_upper_off_by_one": (
        "Student error x02: a sector label equal to the number of caps is accepted (range check one too loose).",
        [("        if not 0 <= label < len(caps):", "        if not 0 <= label <= len(caps):")],
    ),
    "x03_sector_cap_checked_cumulatively": (
        "Student error x03: each sector cap is compared with the cumulative start weight of sectors 0 to k, not its own sector.",
        [("sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL", "sum(w0[i] for i in range(n) if sector[i] <= k) > cap + TOL")],
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
        mutant = f'"""{description}\n\nOne change to grader/reference.py, written by the M7 verifier (round 4).\n"""' + body
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
