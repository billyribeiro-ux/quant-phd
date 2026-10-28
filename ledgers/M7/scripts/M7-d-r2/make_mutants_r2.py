"""Write the verifier's round-2 student-error mutants of the M7 reference into ledgers/M7/mutants/.

Each mutant is the reference solution with one plausible student error applied by exact substitution. Every
substitution must match the expected number of times, or the script stops. Run from the checkout root:
    .venv/bin/python ledgers/M7/scripts/M7-d-r2/make_mutants_r2.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"


def sub_all(text: str, pattern: str, replacement: str, expected: int) -> str:
    new, count = re.subn(pattern, replacement, text)
    if count != expected:
        raise SystemExit(f"substitution {pattern!r} matched {count} times, expected {expected}")
    return new


def sub_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"substitution matched {count} times: {old[:70]!r}")
    return text.replace(old, new)


def mu_longer_than_sigma_truncated(text: str) -> str:
    return sub_once(
        text,
        '    mu = _vector(instance["mu"], "mu")\n    n = len(mu)',
        '    mu = _vector(instance["mu"], "mu")[: len(instance["sigma"])]\n    n = len(mu)',
    )


def every_refusal_says_invalid_input(text: str) -> str:
    return sub_all(text, r'raise ValueError\(f?"[^"\n]*"\)', 'raise ValueError("invalid input")', 19)


def starting_sector_cap_never_checked(text: str) -> str:
    return sub_once(
        text,
        "        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:",
        "        if False:",
    )


def turnover_total_certificate_sign_flipped(text: str) -> str:
    return sub_once(
        text,
        '        r_t = sol["kappa"] - sol["plus"][i] - sol["minus"][i]',
        '        r_t = -sol["kappa"] - sol["plus"][i] - sol["minus"][i]',
    )


MUTANTS: dict[str, tuple[str, object]] = {
    "v05_mu_longer_than_sigma_truncated.py": (
        "Silent truncation: an expected-return list one entry longer than the asset count is cut to the matrix size.",
        mu_longer_than_sigma_truncated,
    ),
    "v06_every_refusal_says_invalid_input.py": (
        "Generic refusals: every ValueError carries the same message, invalid input, and names no condition.",
        every_refusal_says_invalid_input,
    ),
    "v07_starting_sector_cap_never_checked.py": (
        "The starting portfolio is not checked against the sector caps, so a starting breach is accepted.",
        starting_sector_cap_never_checked,
    ),
    "v08_turnover_total_residual_sign_flipped.py": (
        "The turnover-variable stationarity residual in the certificate uses minus kappa.",
        turnover_total_certificate_sign_flipped,
    ),
}


def main() -> int:
    source = REFERENCE.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (description, transform) in MUTANTS.items():
        text = transform(source)  # type: ignore[operator]
        head, _, rest = text.partition('"""')
        body, _, tail = rest.partition('"""')
        _, _, others = body.partition("\n")
        text = head + f'"""{description}\n{others}"""' + tail
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
