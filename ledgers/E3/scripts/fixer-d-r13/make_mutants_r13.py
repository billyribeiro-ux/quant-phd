"""Write the student-error mutants of the E3 reference that round 13 regenerates from the CURRENT reference.

Each mutant is the reference with one edit (r12d_01 is three identical edits of one failure path). Every edit must
match exactly once, or the script stops and writes nothing for that mutant. Mutants are written to ledgers/E3/mutants/.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "E" / "E3" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "E3" / "mutants"
SCRIPT = "ledgers/E3/scripts/fixer-d-r13/make_mutants_r13.py"

EDITS: dict[str, tuple[str, list[tuple[str, str, int]]]] = {
    "e12_01_identification_needs_both_lotteries_mixed.py": (
        "Student error: loss aversion counts a response only when both of its lotteries mix a gain and a loss, so a set whose mixed lottery sits on one side alone is refused.",
        [
            (
                "if not any(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):",
                "if not any(_mixed(a, pa) and _mixed(b, pb) for a, pa, b, pb, _ in parsed):",
                1,
            ),
        ],
    ),
    "e12_02_reported_loss_aversion_clamped_at_ten.py": (
        "Student error: the reported loss aversion is clamped at 10 (a bound the page never states), so a participant whose estimate is above 10 is reported at 10.",
        [("    lam = math.exp(a)\n    kappa = math.exp(b)\n", "    lam = min(math.exp(a), 10.0)\n    kappa = math.exp(b)\n", 1)],
    ),
    "e12_03_search_returns_silently_when_it_stalls.py": (
        "Student error: when the step becomes negligible before the score does, the search returns the point where it stalled instead of raising.",
        [
            (
                'raise RuntimeError("the step became negligible before the score did: the maximisation did not converge")',
                "return xi",
                1,
            ),
        ],
    ),
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
                "    c, a, b = xi\n    gamma = 1.0 / (1.0 + math.exp(-c))\n    lam = math.exp(a)",
                "    c, a, b = xi\n    gamma = max(1.0 / (1.0 + math.exp(-c)), 0.001)\n    lam = math.exp(a)",
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
                "            polished = _polish(f, xi)\n"
                "            if f(polished) > value + 1e-12:\n"
                "                xi, value = polished, f(polished)\n"
                "                mu = 1e-3\n"
                "                continue\n"
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
    status = 0
    for name, (doc, edits) in EDITS.items():
        text = src
        for old, new, count in edits:
            found = text.count(old)
            if found != count:
                print(f"STOP {name}: expected {count} match(es), found {found}: {old[:60]!r}")
                status = 1
                break
            text = text.replace(old, new)
        else:
            assert text.startswith('"""')
            end = text.index('"""', 3)
            inner = text[3:end].strip("\n")
            out = f'"""{doc}\n\nWritten from the current reference by {SCRIPT}.\n\n{inner}\n"""' + text[end + 3 :]
            (OUT / name).write_text(out, encoding="utf-8")
            print(f"wrote {name}")
    return status


if __name__ == "__main__":
    sys.exit(main())
