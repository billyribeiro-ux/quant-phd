"""Writes the fixer's ten student-error mutants of the E1 reference into ledgers/E1/mutants/."""

import sys
from pathlib import Path

REF = Path(sys.argv[1])
OUT = Path(sys.argv[2])
ref = REF.read_text(encoding="utf-8")

OLD_CHECK = '''    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
'''
assert ref.count(OLD_CHECK) == 1
OLD_BRANCH = '''    d = Fraction(a - b * c)
    if structure == "monopoly":'''
assert ref.count(OLD_BRANCH) == 1
OLD_RET = '''    return {
        "volume_trades": half_up(volume),
        "fee_cents": half_up(fee),
        "profit_cents": half_up(profit),
        "consumer_surplus_cents": half_up(consumer),
        "welfare_cents": half_up(welfare),
        "deadweight_loss_cents": half_up(deadweight),
    }
'''
assert ref.count(OLD_RET) == 1

NO_B_CHECK = OLD_CHECK.replace('    if b <= 0:\n        raise ValueError("b must be positive")\n', "")
NO_C_CHECK = OLD_CHECK.replace('    if c <= 0:\n        raise ValueError("c must be positive")\n', "")
NO_A_CHECK = OLD_CHECK.replace('    if a <= b * c:\n        raise ValueError("a must exceed b*c")\n', "")

mutants = {}

# fx01: the b > 0 check is made only inside the monopoly branch (a student who checks b where it is used)
mutants["fx01_b_check_only_in_monopoly"] = (
    "The b > 0 check runs only for the monopoly, so b = 0 or a negative b is accepted for Cournot and Bertrand.",
    ref.replace(OLD_CHECK, NO_B_CHECK).replace(
        OLD_BRANCH,
        '''    if b <= 0 and structure == "monopoly":
        raise ValueError("b must be positive")
    d = Fraction(a - b * c)
    if structure == "monopoly":''',
    ),
)

# fx02: the a > b*c check is made only for Bertrand
mutants["fx02_a_check_only_in_bertrand"] = (
    "The a > b*c check runs only for Bertrand, so a <= b*c is accepted for monopoly and Cournot.",
    ref.replace(OLD_CHECK, NO_A_CHECK).replace(
        OLD_BRANCH,
        '''    if structure == "bertrand" and a <= b * c:
        raise ValueError("a must exceed b*c")
    d = Fraction(a - b * c)
    if structure == "monopoly":''',
    ),
)

# fx11: the a > b*c check is made only inside the Cournot branch (the verifier's r2_m02 class)
mutants["fx11_a_check_only_in_cournot"] = (
    "The a > b*c check runs only for Cournot, so a <= b*c is accepted for monopoly and Bertrand.",
    ref.replace(OLD_CHECK, NO_A_CHECK).replace(
        OLD_BRANCH,
        '''    if structure == "cournot" and a <= b * c:
        raise ValueError("a must exceed b*c")
    d = Fraction(a - b * c)
    if structure == "monopoly":''',
    ),
)

# fx03: the c > 0 check is made only inside the Cournot branch
mutants["fx03_c_check_only_in_cournot"] = (
    "The c > 0 check runs only for Cournot, so c = 0 or a negative cost is priced for monopoly and Bertrand.",
    ref.replace(OLD_CHECK, NO_C_CHECK).replace(
        OLD_BRANCH,
        '''    if c <= 0 and structure == "cournot":
        raise ValueError("c must be positive")
    d = Fraction(a - b * c)
    if structure == "monopoly":''',
    ),
)

# fx04: an unknown name 'duopoly' is treated as Cournot instead of raising ValueError
mutants["fx04_duopoly_alias_for_cournot"] = (
    "The name duopoly is read as cournot, so an unknown structure name is priced instead of raising ValueError.",
    ref.replace(
        OLD_CHECK, '    if structure == "duopoly":\n        structure = "cournot"\n' + OLD_CHECK
    ),
)

# fx05: a non-string structure raises TypeError, not ValueError, which the page names for this input
mutants["fx05_non_string_structure_is_type_error"] = (
    "A non-string structure raises TypeError, but the page names ValueError for a structure that is not one of the names.",
    ref.replace(
        OLD_CHECK,
        '    if not isinstance(structure, str):\n        raise TypeError("structure must be a string")\n' + OLD_CHECK,
    ),
)

# fx06: the a check's message does not name the condition
mutants["fx06_a_message_does_not_name_condition"] = (
    "The a check raises ValueError with the message 'a too small', which does not state a > b*c.",
    ref.replace('raise ValueError("a must exceed b*c")', 'raise ValueError("a too small")'),
)

# fx07: an off-by-one boundary, a = b*c + 1 (the smallest valid case) is rejected
mutants["fx07_smallest_valid_case_rejected"] = (
    "The a check uses a <= b*c + 1, so the smallest valid case a = b*c + 1 is rejected.",
    ref.replace("    if a <= b * c:\n", "    if a <= b * c + 1:\n"),
)

# fx08: welfare is built from the rounded consumer surplus and the rounded profit, not the exact sum
mutants["fx08_welfare_from_rounded_parts"] = (
    "Welfare is the sum of the rounded consumer surplus and the rounded profit, not one rounding of the exact sum.",
    ref.replace('        "welfare_cents": half_up(welfare),', '        "welfare_cents": half_up(consumer) + half_up(profit),'),
)

# fx09: a volume is returned as a float
mutants["fx09_volume_returned_as_float"] = (
    "The volume is returned as a float, not an int, so the integer type rule fails.",
    ref.replace('        "volume_trades": half_up(volume),', '        "volume_trades": float(half_up(volume)),'),
)

# fx10: the deadweight loss key is missing from the outcome
mutants["fx10_deadweight_key_missing"] = (
    "The outcome omits the deadweight_loss_cents key, so the dictionary does not have the six required keys.",
    ref.replace('        "deadweight_loss_cents": half_up(deadweight),\n', ""),
)

for name, (description, source) in mutants.items():
    assert source != ref, name
    body = source[source.index("from __future__"):]
    text = f'"""MUTANT {name}: {description}"""\n\n' + body
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
