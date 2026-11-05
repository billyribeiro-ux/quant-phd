"""Writes the four round-13 student-error mutants as complete solver modules from reference.py (verifier, round 13).

Each mutant changes one line of the reference, asserts that the line occurs exactly once, and replaces the module
docstring's first line with the student error, as tools/mutate_graders.py reads it.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-E4-d")
REF = ROOT / "course/modules/E/E4/grader/reference.py"
OUT = ROOT / "ledgers/E4/mutants"

MUTANTS = {
    "mutant_r13_01_closed_form_root_drops_cara_factor.py": (
        "Interior fraction from the closed form with the CARA coefficient dropped, so the fraction is half the root.",
        [
            (
                "        lam = 0.5 * (low + high)\n",
                "        t_bar = (PRIOR_PRECISION + SIGNAL_PRECISION) * math.exp(-2.0 * RISK_AVERSION * cost) - PRIOR_PRECISION\n"
                "        lam = sd * math.sqrt(t_bar / (SIGNAL_PRECISION * (SIGNAL_PRECISION - t_bar)))\n",
            )
        ],
    ),
    "mutant_r13_02_informativeness_omits_price_noise_variance.py": (
        "Informativeness from Var(p) = b_s^2 Var(s), dropping the price-noise term b_u^2 sd^2, so it is 0.5 at every fraction.",
        [
            (
                "    return tau_y / (PRIOR_PRECISION + tau_y)\n",
                "    b_s, _, _ = price_coefficients(lam, noise_sd)\n"
                "    var_p = b_s * b_s * (1.0 / PRIOR_PRECISION + 1.0 / SIGNAL_PRECISION)\n"
                "    return (b_s / PRIOR_PRECISION) ** 2 / ((1.0 / PRIOR_PRECISION) * var_p)\n",
            )
        ],
    ),
    "mutant_r13_03_boundary_fraction_returned_as_integer.py": (
        "Boundary fractions 0 and 1 are returned as Python integers, not floats, which the specification forbids.",
        [
            (
                '        "informed_fraction": lam,\n',
                '        "informed_fraction": int(lam) if lam in (0.0, 1.0) else lam,\n',
            )
        ],
    ),
    "mutant_r13_04_informed_demand_price_sign_flipped.py": (
        "Informed demand uses the price with the wrong sign in the slope, so the informed mean minus price is misstated.",
        [
            (
                "    slope = tau_e / precision - b_s\n",
                "    slope = tau_e / precision + b_s\n",
            )
        ],
    ),
}


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    lines = ref.split("\n", 1)
    assert lines[0].startswith('"""Reference solution for the E4 project'), lines[0][:60]
    for name, (description, edits) in MUTANTS.items():
        text = ref
        for old, new in edits:
            assert text.count(old) == 1, (name, old, text.count(old))
            text = text.replace(old, new)
        first_line, rest = text.split("\n", 1)
        assert first_line.startswith('"""Reference solution')
        head = f'"""{description}\n\n{rest.split(chr(10), 1)[0] if False else ""}'
        body = text.split('"""', 2)  # ['', docstring, rest]
        docstring_body = body[1]
        new_doc = f'"""{description}\n\nRound-13 student-error mutant of the reference (verifier). Standard library only.\n"""'
        text = new_doc + body[2]
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
