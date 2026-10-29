"""Write round-4 student-error mutants of the E1 reference into ledgers/E1/mutants/ (one asserted edit each)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/E/E1/grader/reference.py"
OUT = ROOT / "ledgers/E1/mutants"

MUTANTS: dict[str, tuple[str, str, str]] = {
    "r4_m01_padded_bertrand_name_stripped": (
        "Padded Bertrand name accepted: the name is stripped only for bertrand, so 'bertrand ' prices instead of raising ValueError.",
        '    check_inputs(structure, a, b, c)\n',
        '    if structure.strip() == "bertrand":\n        structure = "bertrand"\n    check_inputs(structure, a, b, c)\n',
    ),
    "r4_m02_capitalised_cournot_lowered": (
        "Capitalised Cournot name accepted: 'Cournot' is lower-cased before the check, so it prices instead of raising ValueError.",
        '    check_inputs(structure, a, b, c)\n',
        '    if structure == "Cournot":\n        structure = "cournot"\n    check_inputs(structure, a, b, c)\n',
    ),
    "r4_m03_bytes_structure_decoded": (
        "Non-string structure accepted: bytes are decoded, so b'monopoly' prices instead of raising ValueError.",
        '    check_inputs(structure, a, b, c)\n',
        '    if isinstance(structure, bytes):\n        structure = structure.decode()\n    check_inputs(structure, a, b, c)\n',
    ),
    "r4_m04_fee_computed_before_checks": (
        "Fee computed before the input checks: b = 0 raises ZeroDivisionError, not the ValueError the page names.",
        '    check_inputs(structure, a, b, c)\n',
        '    _early = Fraction(a + b * c, 2 * b)  # computed before the checks\n    check_inputs(structure, a, b, c)\n',
    ),
    "r4_m05_half_threshold_at_four_tenths": (
        "Rounding threshold at 0.4: any fraction of 0.4 or more rounds up, so the Cournot welfare 4444.44 prints 4445.",
        "    return math.floor(x + Fraction(1, 2))",
        "    return math.floor(x + Fraction(3, 5))",
    ),
    "r4_m06_deadweight_key_renamed": (
        "Deadweight key misnamed: deadweight_cents replaces deadweight_loss_cents, so one key is missing and one is extra.",
        '"deadweight_loss_cents": half_up(deadweight),',
        '"deadweight_cents": half_up(deadweight),',
    ),
    "r4_m07_cournot_a_equal_to_bc_accepted": (
        "Cournot skips the a check: a = b*c is accepted for cournot (zero gap, no ValueError).",
        '    if a <= b * c:\n',
        '    if a <= b * c and structure != "cournot":\n',
    ),
    "r4_m08_bertrand_c_zero_accepted": (
        "The c check spares bertrand: c = 0 is accepted for bertrand instead of raising ValueError.",
        '    if c <= 0:\n',
        '    if c <= 0 and structure != "bertrand":\n',
    ),
    "r4_m09_b_only_zero_rejected": (
        "The b check tests b == 0 only: a negative b is accepted instead of raising ValueError.",
        '    if b <= 0:\n',
        '    if b == 0:\n',
    ),
    "r4_m10_structure_checked_by_prefix": (
        "Structure checked by prefix: any name starting with a structure name passes, so 'cournot ' prices as the else branch.",
        '    if structure not in STRUCTURES:\n',
        '    if not any(structure.startswith(name) for name in STRUCTURES):\n',
    ),
    "r4_m11_third_party_import": (
        "Third-party import: the module imports pytest, which is not part of the standard library the page allows.",
        "import math\n",
        "import math\nimport pytest  # noqa: F401\n",
    ),
}


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    for name, (description, old, new) in MUTANTS.items():
        assert source.count(old) == 1, (name, source.count(old))
        text = source.replace(old, new, 1)
        header = f'"""{description}"""\n'
        body = text.split('"""', 2)[2]  # drop the reference's module docstring
        (OUT / f"{name}.py").write_text(header + body, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
