"""Write the verifier's student-error mutants of the M7 reference into ledgers/M7/mutants/.

Each mutant is the reference solution with one plausible student error applied by exact string substitution. The
substitution must match exactly once, or the script stops. Run from the checkout root:
    .venv/bin/python ledgers/M7/scripts/M7-d-r1/make_mutants.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "v01_nan_in_mu_silently_zeroed.py": (
        "Silent fallback: a NaN expected return is replaced by zero instead of being refused with ValueError.",
        [
            (
                "def _vector(value: object, name: str) -> list[Fraction]:\n    if not isinstance(value, (list, tuple)):\n"
                '        raise TypeError(f"{name} must be a list of numbers")\n'
                "    return [_scalar(item, f\"{name}[{i}]\") for i, item in enumerate(value)]",
                "def _vector(value: object, name: str) -> list[Fraction]:\n    if not isinstance(value, (list, tuple)):\n"
                '        raise TypeError(f"{name} must be a list of numbers")\n'
                "    return [Fraction(0) if isinstance(v, float) and math.isnan(v) else _scalar(v, f\"{name}[{i}]\")"
                " for i, v in enumerate(value)]",
            ),
        ],
    ),
    "v02_second_sector_cap_never_imposed.py": (
        "Only the first sector cap is imposed in the solver; the second sector cap is never applied.",
        [
            (
                "    for k, cap in enumerate(problem.caps):\n        rows.append(",
                "    for k, cap in enumerate(problem.caps[:1]):\n        rows.append(",
            ),
        ],
    ),
    "v03_start_tolerance_1e-5.py": (
        "Starting-portfolio checks use a tolerance of 1e-5, where the page states 1e-9.",
        [
            ("TOL = Fraction(1, 10**9)", "TOL = Fraction(1, 10**5)"),
        ],
    ),
    "v04_weights_rounded_to_six_places.py": (
        "The returned weights are rounded to six decimals before the certificate is computed from them.",
        [
            (
                '        "weights": [float(v) for v in sol["w"]],',
                '        "weights": [round(float(v), 6) for v in sol["w"]],',
            ),
        ],
    ),
}


def main() -> int:
    source = REFERENCE.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (description, edits) in MUTANTS.items():
        text = source
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                print(f"FAIL {name}: substitution matched {count} times: {old[:60]!r}")
                return 1
            text = text.replace(old, new)
        head, _, rest = text.partition('"""')
        docstring_body, _, tail = rest.partition('"""')
        first, _, others = docstring_body.partition("\n")
        new_doc = f'"""{description}\n{others}"""'
        text = head + new_doc + tail
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
