import pathlib
REF = pathlib.Path("/tmp/verify40-AC4-e/course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/verify40-AC4-e/ledgers/AC4/scripts/AC4-e-r40/alts")
ROUND_OLD = '''    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)'''
ALTS = {
    "alt40_a_decimal_half_up.py": (
        "Alternative: the nearest cent by Decimal.quantize with ROUND_HALF_UP.",
        ROUND_OLD,
        '''    from decimal import Decimal, ROUND_HALF_UP, localcontext

    with localcontext() as ctx:
        ctx.prec = 80
        value = Decimal(amount.numerator) / Decimal(amount.denominator)
        return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))''',
    ),
    "alt40_b_floor_of_plus_half.py": (
        "Alternative: the nearest cent as floor(amount + 1/2) with exact fractions.",
        ROUND_OLD,
        '''    import math

    return math.floor(amount + Fraction(1, 2))''',
    ),
    "alt40_c_strict_int_type_check.py": (
        "Alternative: whole numbers are checked with type(value) is int, (the only change).",
        '''    if isinstance(value, bool) or not isinstance(value, numbers.Integral):''',
        '''    if type(value) is not int:''',
    ),
}
for name, (doc, old, new) in ALTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    end = REF.index('"""', 3) + 3
    text = '"""' + doc + '\n\nSpec-correct alternative: a different valid implementation, not a mutant.\n"""' + REF[end:]
    text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
