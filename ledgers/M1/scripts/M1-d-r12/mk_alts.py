"""Writes round-12 verifier alternative implementations of M1-d from the reference (run with python -I).
usage: mk_alts.py <reference.py> <outdir>"""
import pathlib, sys
REF = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")
def rep(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)
alts = {
 "alt_r12v_a_expm1_closed_form.py": rep(src, "    return (1 - (1 + r) ** -n) / r",
     "    return -math.expm1(-n * math.log1p(r)) / r"),
 "alt_r12v_b_decimal_half_up_money.py": rep(src,
     '''def _nearest_cent(amount: Fraction) -> int:''',
     '''def _nearest_cent(amount: Fraction) -> int:
    from decimal import ROUND_HALF_UP, Decimal, localcontext
    with localcontext() as ctx:
        ctx.prec = 110
        value = Decimal(amount.numerator) / Decimal(amount.denominator)
        return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _unused_nearest_cent(amount: Fraction) -> int:'''),
 "alt_r12v_c_horner_annuity.py": rep(src, "    return (1 - (1 + r) ** -n) / r",
     "    v = 1.0 / (1.0 + r)\n    total = 0.0\n    for _ in range(n):\n        total = v * (1.0 + total)\n    return total"),
 "witness_r12v_d_type_error_for_rate_types.py": rep(src,
     '''    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")''',
     '''    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")'''),
 "witness_r12v_e_type_error_for_month_type.py": rep(src,
     '''def _months(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:''',
     '''def _months(value: object) -> int:
    if not isinstance(value, int) and not isinstance(value, bool):
        raise TypeError("months must be an int")
    if isinstance(value, bool) or value < 1:'''),
}
for name, text in alts.items():
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
