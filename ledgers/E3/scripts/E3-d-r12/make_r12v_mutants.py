"""Write four round-12 student-error mutants of grader/reference.py into ledgers/E3/mutants/ (verifier's own, r12v_).

Each mutant is the reference with one replacement; every replacement must match exactly once (asserted). The module
docstring is replaced by a one-paragraph description, because tools/mutate_graders.py reads the first docstring line.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/E/E3/grader/reference.py"
OUT = ROOT / "ledgers/E3/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "r12v_01_five_newton_steps_then_returns_the_point_reached": (
        "Student error: the maximiser takes at most five damped Newton steps and returns the point it has reached, "
        "whether or not the score is near zero.",
        [
            ("_MAX_ITER = 200", "_MAX_ITER = 5"),
            (
                '    raise RuntimeError("the likelihood maximisation did not converge")',
                "    return xi",
            ),
        ],
    ),
    "r12v_02_search_stops_once_every_score_component_is_below_one_ten_thousandth": (
        "Student error: the maximiser stops as soon as every score component is below 1e-4, so an estimate can keep a "
        "score component of several times 1e-5.",
        [("        if max(abs(g) for g in grad) < 1e-7:\n            return xi", "        if max(abs(g) for g in grad) < 1e-4:\n            return xi")],
    ),
    "r12v_03_b_response_contributes_log_p_of_a": (
        "Student error: a response that chose B contributes log P(A), not log(1 - P(A)), to the log-likelihood.",
        [
            (
                'total += -_log1pexp(-z) if choice == "A" else -_log1pexp(z)',
                'total += -_log1pexp(-z) if choice == "A" else -_log1pexp(-z)',
            )
        ],
    ),
    "r12v_04_reported_gamma_is_one_minus_gamma": (
        "Student error: the estimate reports 1 - gamma_hat as gamma_hat (the probability of B instead of A in the "
        "curvature parameter).",
        [('        "gamma_hat": gamma,', '        "gamma_hat": 1.0 - gamma,')],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    head, sep, rest = source.partition('"""\n\nfrom __future__')
    assert sep and head.startswith('"""'), "unexpected reference header"
    for name, (description, replacements) in MUTANTS.items():
        text = source
        for old, new in replacements:
            count = text.count(old)
            assert count == 1, f"{name}: {old!r} occurs {count} times"
            text = text.replace(old, new)
        doc_end = text.index('"""\n\nfrom __future__')
        body = text[doc_end + len('"""\n') :]
        mutant = f'"""{description}\n\nWritten from the reference by {Path(__file__).relative_to(ROOT).as_posix()}.\n"""\n{body}'
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
