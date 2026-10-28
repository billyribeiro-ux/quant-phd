import pathlib, sys
root = pathlib.Path(sys.argv[1]); out = root / 'ledgers/CF1/mutants/CF1-a-r10'
L01 = (root / 'tests/labs/CF1/lab-CF1-L01-1.py').read_text()
L02 = (root / 'tests/labs/CF1/lab-CF1-L02-1.py').read_text()
muts = {
 'n01_annuity_factor_one_year_short.py': (L01, '(1.0 - (1.0 + rate) ** -years) / rate', '(1.0 - (1.0 + rate) ** -(years - 1)) / rate'),
 'n02_sunk_cost_credited_not_charged.py': (L02, 'flows[0] - SUNK_STUDY_CENTS / 100', 'flows[0] + SUNK_STUDY_CENTS / 100'),
 'n03_tax_base_ebitda_when_ebit_positive.py': (L02, 'tax = TAX_RATE * ebit\n', 'tax = TAX_RATE * (ebitda if ebit > 0 else ebit)\n'),
}
for name, (src, old, new) in muts.items():
    assert src.count(old) == 1, (name, src.count(old))
    (out / name).write_text(src.replace(old, new))
    print('wrote', name)
