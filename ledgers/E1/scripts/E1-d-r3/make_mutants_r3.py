"""Write round-3 student-error mutants of the E1 project reference into ledgers/E1/mutants/.

Each mutant is the reference solution with exactly one replacement; the script asserts that every replacement
matches exactly once, so a mutant cannot silently equal the reference.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/E/E1/grader/reference.py"
OUT = ROOT / "ledgers/E1/mutants"

MUTANTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "e1d_r3_m01_tie_rounds_to_even",
        "Rounding by Python round(), which sends an exact half to the even neighbour, so a tie does not go up.",
        [("    return math.floor(x + Fraction(1, 2))", "    return round(x)")],
    ),
    (
        "e1d_r3_m02_deadweight_from_printed_volume",
        "Deadweight loss measured from the printed volume half_up(volume), not the exact volume.",
        [("    deadweight = (d - volume) ** 2 / (2 * b)", "    deadweight = (d - half_up(volume)) ** 2 / (2 * b)")],
    ),
    (
        "e1d_r3_m03_a_equal_bc_accepted",
        "The first input check is strict, so a equal to b*c is accepted instead of raising ValueError.",
        [("    if a <= b * c:", "    if a < b * c:")],
    ),
    (
        "e1d_r3_m04_structure_name_lowercased",
        "The structure name is lowercased before the check, so the capitalised name Monopoly is accepted.",
        [
            ("    if structure not in STRUCTURES:", "    if structure.lower() not in STRUCTURES:"),
            ('    if structure == "monopoly":', '    structure = structure.lower()\n    if structure == "monopoly":'),
        ],
    ),
    (
        "e1d_r3_m05_consumer_surplus_is_revenue",
        "Consumer surplus taken as the fee times the volume, the exchange revenue, not the area above the fee.",
        [("    consumer = volume * volume / (2 * b)", "    consumer = fee * volume")],
    ),
    (
        "e1d_r3_m06_rounding_in_floating_point",
        "Rounding in floating point, math.floor(float(x) + 0.5), so a large exact value loses its fraction.",
        [("    return math.floor(x + Fraction(1, 2))", "    return math.floor(float(x) + 0.5)")],
    ),
]


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    for name, description, replacements in MUTANTS:
        text = source
        for old, new in replacements:
            count = text.count(old)
            assert count == 1, f"{name}: pattern matched {count} times: {old!r}"
            text = text.replace(old, new)
        body = text.split('"""', 2)[2]  # drop the reference module docstring
        mutant = f'"""{description}"""\n{body}'
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
