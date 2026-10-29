"""Writes three spec-correct alternative budget_engine.py modules derived from the reference (round 18 verifier)."""
import pathlib, re
REF = pathlib.Path("/tmp/verify18-AC4-e/course/modules/AC/AC4/grader/reference.py").read_text()
OUT = pathlib.Path("/tmp/verify18-AC4-e/ledgers/AC4/scripts/AC4-e-r18/alts")

def sub(src, old, new):
    assert src.count(old) == 1, old[:60]
    return src.replace(old, new)

# alt18_a: validators by exact type (type(x) is int), rounding by floor(x + 1/2)
a = REF
a = sub(a, '    if isinstance(value, bool) or not isinstance(value, numbers.Integral):\n        raise ValueError(f"{name} must be a whole number of cents or units, not {value!r}")\n    return int(value)',
        '    if type(value) is not int:\n        raise ValueError(f"{name} must be a whole number of cents or units, not {value!r}")\n    return value')
a = sub(a, '    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)',
        '    import math\n    return math.floor(amount + Fraction(1, 2))')
(OUT / "alt18_a_exact_type_floor_half.py").write_text(a)

# alt18_b: rounding by divmod on the numerator; products validated before the case fields
b = REF
b = sub(b, '    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)',
        '    whole, rest = divmod(amount.numerator, amount.denominator)\n    return whole + (1 if 2 * rest >= amount.denominator else 0)')
(OUT / "alt18_b_divmod_half_up.py").write_text(b)

# alt18_c: numbers.Integral kept, bool refused explicitly, names checked with str.isprintable-free test, flexed profit via fractions
c = REF
c = sub(c, '    if isinstance(value, bool) or not isinstance(value, numbers.Integral):',
        '    if isinstance(value, bool) or not isinstance(value, int):')
c = sub(c, '        name = item["name"]\n        if not isinstance(name, str) or not name:',
        '        name = item["name"]\n        if type(name) is not str or len(name.strip()) == 0:')
(OUT / "alt18_c_int_isinstance_strip_name.py").write_text(c)
print("written")
