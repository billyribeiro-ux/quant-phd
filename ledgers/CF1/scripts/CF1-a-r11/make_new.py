import pathlib, sys
root = pathlib.Path(sys.argv[1])
out = root / 'ledgers/CF1/mutants/CF1-a-r11'
L01 = (root / 'tests/labs/CF1/lab-CF1-L01-1.py').read_text()
L02 = (root / 'tests/labs/CF1/lab-CF1-L02-1.py').read_text()
specs = {
    'n04_l02_shield_check_uses_ebitda.py': (L02, '        shield_ok = shield_ok and abs((ocf - ocf_without) - depreciation_cents * TAX_RATE) < TOLERANCE',
                                                  '        shield_ok = shield_ok and abs((ocf - ocf_without) - ebitda * TAX_RATE) < TOLERANCE'),
    'n05_l02_identity_check_stubbed_true.py': (L02, '        identity_ok = identity_ok and abs(ocf - (ebitda * (1 - TAX_RATE) + shield)) < TOLERANCE',
                                                   '        identity_ok = True'),
    'n06_l01_years_drawn_with_randrange.py': (L01, '        years = rng.randint(1, 15)', '        years = rng.randrange(1, 15)'),
}
for name, (src, old, new) in specs.items():
    assert src.count(old) == 1, (name, src.count(old))
    (out / name).write_text(src.replace(old, new))
    print('wrote', name)
