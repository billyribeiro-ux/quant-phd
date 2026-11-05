"""Verifier FC1-c round 9: write four new student-error mutants of reference.py into ledgers/FC1/mutants/."""
import pathlib
root = pathlib.Path('/Users/billyribeiro/.fanout/wt/verifyD9-FC1-c')
ref = (root / 'course/modules/FC/FC1/grader/reference.py').read_text(encoding='utf-8')
out = root / 'ledgers/FC1/mutants'

def make(name, doc, old, new):
    assert ref.count(old) == 1, (name, ref.count(old))
    src = ref.replace(old, new, 1)
    end = src.index('"""', 3) + 3
    src = f'"""{doc}\n\nWritten by the verifier for FC1 slice c, round 9: a student-error mutant of reference.py.\n"""' + src[end:]
    (out / name).write_text(src, encoding='utf-8')

make('r9c_yield_refused_above_two_thousand_percent.py',
     'Bond_price refuses a yield above 2000 percent per period (yield_bps > 200000), which the page does not refuse.',
     '    if rate <= -10_000:\n        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")',
     '    if rate <= -10_000 or rate > 200_000:\n        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")')
make('r9c_periods_refused_above_ten_thousand.py',
     'Bond refuses periods above 10000, although the page names no upper limit on periods.',
     '        if count < 1:\n            raise ValueError("periods must be at least 1")',
     '        if count < 1 or count > 10_000:\n            raise ValueError("periods must be at least 1")')
make('r9c_settlement_day_refused_above_ten_thousand.py',
     'CashTrade refuses a settlement period above 10000, although the page names only settlement_day below 1 as refused.',
     '        if day < 1:\n            raise ValueError("settlement_day must be at least 1")',
     '        if day < 1 or day > 10_000:\n            raise ValueError("settlement_day must be at least 1")')
make('r9c_quantity_refused_above_two_to_the_fifty.py',
     'CashTrade refuses a quantity above 2**50 units, although the page names no upper limit on quantity.',
     '        if units < 1:\n            raise ValueError("quantity must be at least 1")',
     '        if units < 1 or units > 2**50:\n            raise ValueError("quantity must be at least 1")')
print('written')
