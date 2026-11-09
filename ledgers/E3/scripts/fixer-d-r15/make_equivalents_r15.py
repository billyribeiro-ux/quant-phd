"""Regenerates the seven equivalent files (four tie-rule files, three gamma-clamp files) from the current reference.

Each file is the current reference with one edit, and its first docstring line names the student error. Usage (repo
root): .venv/bin/python -I ledgers/E3/scripts/fixer-d-r15/make_equivalents_r15.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/E/E3/grader/reference.py"
OUT = ROOT / "ledgers/E3/equivalent"

HALF_UP_OLD = "    return math.floor(Fraction(y) + Fraction(1, 2))\n"
GAMMA_OLD = "    c, a, b = xi\n    gamma = 1.0 / (1.0 + math.exp(-c))\n"

FILES: dict[str, tuple[str, str, str]] = {
    # name: (old text, new text, student error stated in the first docstring line)
    "f05_half_cent_goes_toward_minus_infinity.py": (
        HALF_UP_OLD,
        "    return math.ceil(Fraction(y) - Fraction(1, 2))\n",
        "the half cent is rounded toward minus infinity, so an exact half goes down.",
    ),
    "m06_half_cent_rounded_to_even.py": (
        HALF_UP_OLD,
        "    return round(Fraction(y))\n",
        "the half cent is rounded to the even neighbour, so 2.5 gives 2 and 3.5 gives 4.",
    ),
    "r13n01_half_cent_rounded_half_to_even.py": (
        HALF_UP_OLD,
        "    return round(Fraction(y))\n",
        "the half cent is rounded half to even, so 2.5 gives 2 and 3.5 gives 4.",
    ),
    "w05_half_cent_away_from_zero.py": (
        HALF_UP_OLD,
        "    return math.floor(Fraction(y) + Fraction(1, 2)) if y >= 0 else math.ceil(Fraction(y) - Fraction(1, 2))\n",
        "the half cent is rounded away from zero, so -2.5 gives -3.",
    ),
    "r11_03_gamma_hat_clamped_below_one_minus_1e3.py": (
        GAMMA_OLD,
        "    c, a, b = xi\n    gamma = min(1.0 / (1.0 + math.exp(-c)), 0.999)\n",
        "gamma_hat is clamped to 0.999 when the maximiser lands above it.",
    ),
    "r12d_03_reported_gamma_floored_at_one_thousandth.py": (
        GAMMA_OLD,
        "    c, a, b = xi\n    gamma = max(1.0 / (1.0 + math.exp(-c)), 0.001)\n",
        "gamma_hat is floored at 0.001 when the maximiser lands below it.",
    ),
    "v15d_03_reported_gamma_clamped_at_0_99.py": (
        GAMMA_OLD,
        "    c, a, b = xi\n    gamma = min(1.0 / (1.0 + math.exp(-c)), 0.99)\n",
        "gamma_hat is clamped to 0.99 when the maximiser lands above it.",
    ),
}


def main() -> None:
    base = REF.read_text(encoding="utf-8")
    assert base.startswith('"""Reference solution'), "unexpected reference header"
    for name, (old, new, error) in FILES.items():
        assert base.count(old) == 1, f"{name}: target text must occur exactly once in the reference"
        text = base.replace(old, new)
        header = f'"""Student error: {error}\n\n'
        text = header + text[len('"""') :]
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
