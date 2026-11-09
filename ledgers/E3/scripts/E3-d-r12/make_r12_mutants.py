"""Write the round-12 student-error mutants of the E3 reference (slice d) into ledgers/E3/mutants/.

Each mutant is the reference with one edit; every edit must match exactly once, or the script stops.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "E" / "E3" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "E3" / "mutants"

EDITS: dict[str, tuple[str, list[tuple[str, str, int]]]] = {
    "r12d_01_search_failure_returns_the_grid_start.py": (
        "Student error: when the Newton search raises, the maximiser returns the best grid start as if it were the estimate.",
        [
            (
                'raise RuntimeError("no damped Newton step raises the likelihood: the maximisation did not converge")',
                "return list(best[1])",
                1,
            ),
            (
                'raise RuntimeError("the step became negligible before the score did: the maximisation did not converge")',
                "return list(best[1])",
                1,
            ),
            ('raise RuntimeError("the likelihood maximisation did not converge")', "return list(best[1])", 1),
        ],
    ),
    "r12d_02_se_gamma_uses_gamma_for_the_delta_factor.py": (
        "Student error: the standard error of gamma carries the factor gamma instead of gamma (1 - gamma) from the change of coordinates.",
        [('"se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),', '"se_gamma": gamma * math.sqrt(cov_diag[0]),', 1)],
    ),
    "r12d_03_reported_gamma_floored_at_one_thousandth.py": (
        "Student error: the reported curvature is floored at 0.001, so an estimate at the lower boundary of the domain is reported as 0.001.",
        [
            (
                '    c, a, b = xi\n    gamma = 1.0 / (1.0 + math.exp(-c))\n    lam = math.exp(a)',
                '    c, a, b = xi\n    gamma = max(1.0 / (1.0 + math.exp(-c)), 0.001)\n    lam = math.exp(a)',
                1,
            ),
        ],
    ),
    "r12d_04_stalled_search_returned_without_the_score_check.py": (
        "Student error: a search whose step has become negligible is returned as the estimate without checking that the score is near zero.",
        [
            (
                "            grad_end, _ = _gradient_and_hessian(f, xi)\n"
                "            if max(abs(g) for g in grad_end) < _STATIONARY:\n"
                "                return xi\n"
                '            raise RuntimeError("the step became negligible before the score did: the maximisation did not converge")',
                "            return xi",
                1,
            ),
            (
                "                if max(abs(g) for g in grad) < _STATIONARY:\n"
                "                    return xi\n"
                '                raise RuntimeError("no damped Newton step raises the likelihood: the maximisation did not converge")',
                "                return xi",
                1,
            ),
        ],
    ),
}


def main() -> int:
    src = REF.read_text(encoding="utf-8")
    for name, (doc, edits) in EDITS.items():
        text = src
        for old, new, count in edits:
            found = text.count(old)
            if found != count:
                print(f"STOP {name}: expected {count} match(es), found {found}: {old[:60]!r}")
                return 1
            text = text.replace(old, new)
        # The reference opens with its own module docstring: replace it with the description of the error, so the
        # first line of the docstring is the description and the module keeps one docstring before its imports.
        assert text.startswith('"""')
        end = text.index('"""', 3)
        inner = text[3:end].strip("\n")
        out = f'"""{doc}\n\nWritten from the reference by ledgers/E3/scripts/E3-d-r12/make_r12_mutants.py.\n\n{inner}\n"""' + text[end + 3 :]
        (OUT / name).write_text(out, encoding="utf-8")
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
