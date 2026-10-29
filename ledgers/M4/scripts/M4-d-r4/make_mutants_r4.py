"""Writes the three round-4 student-error mutants (v4_*) of the M4 project grader from the reference solution.

Run: python3 ledgers/M4/scripts/M4-d-r4/make_mutants_r4.py  (writes ledgers/M4/mutants/v4_*.py)
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M4/mutants"

MUTANTS = {
    "v4_m01_loss_rounded_per_position.py": (
        "Verifier round-4 student-error mutant. Each position's loss is rounded to a whole cent before the positions are "
        "summed, so the loss is not rounded once as the page states.",
        [
            (
                "        total = 0.0\n        for i in range(n):\n            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))\n            total += position_cents[i] * ret\n        losses.append(round(-total))",
                "        total = 0\n        for i in range(n):\n            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))\n            total += round(-position_cents[i] * ret)\n        losses.append(total)",
            ),
        ],
    ),
    "v4_m02_matched_factor_skipped_for_small_nu.py": (
        "Verifier round-4 student-error mutant. The matched factor is applied only when nu > 4, so the Student-t draws "
        "at nu = 3 and nu = 4 are inflated by nu / (nu - 2).",
        [
            (
                "            scale = math.sqrt(matched * nu / chi_square)",
                "            scale = math.sqrt((matched if nu > 4 else 1.0) * nu / chi_square)",
            ),
        ],
    ),
    "v4_m03_loss_sign_folded.py": (
        "Verifier round-4 student-error mutant. The loss is taken as the absolute value of the portfolio return, so a "
        "gain is recorded as a positive loss.",
        [
            ("        losses.append(round(-total))", "        losses.append(round(abs(total)))"),
        ],
    ),
}


def main() -> None:
    for name, (doc, edits) in MUTANTS.items():
        text = REF
        for old, new in edits:
            assert text.count(old) == 1, (name, old[:40])
            text = text.replace(old, new)
        # one-line docstring first, then the body of the reference from its imports onwards
        body = text.split('"""', 2)[2]
        out = f'"""{doc}"""\n{body}'
        (OUT / name).write_text(out, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
