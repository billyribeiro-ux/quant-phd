"""Round-6 verifier: writes the Decimal-precision student-error mutants. The 28-digit one is the default-context
variant; the 40-digit one wraps the same sum in a localcontext with prec 40. Usage: python -I make_decimal_mutants_r6.py <mutants dir>"""
import pathlib
import sys

out = pathlib.Path(sys.argv[1])
base = (out / "r6c_price_default_decimal_28_digits.py").read_text(encoding="utf-8")
old = """    one_plus = Decimal(10000 + yield_bps) / Decimal(10000)
    total = sum((Decimal(a) / one_plus**t for t, a in bond.events()), Decimal(0))
    return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))"""
new = """    from decimal import localcontext
    with localcontext() as ctx:
        ctx.prec = PREC
        one_plus = Decimal(10000 + yield_bps) / Decimal(10000)
        total = sum((Decimal(a) / one_plus**t for t, a in bond.events()), Decimal(0))
        return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))"""
assert base.count(old) == 1
text = base.replace(old, new).replace("PREC", "40")
doc_old = "Student error: bond_price_cents sums the discounted events in Python's default Decimal context (28 significant digits), so a price above 28 significant digits loses its half cent before the rounding."
doc_new = "Student error: bond_price_cents sums the discounted events in a Decimal context of 40 significant digits, so a price above 40 significant digits loses its half cent before the rounding."
assert text.count(doc_old) == 1
(out / "r6c_price_decimal_forty_significant_digits.py").write_text(text.replace(doc_old, doc_new), encoding="utf-8")
print("wrote r6c_price_decimal_forty_significant_digits.py")
