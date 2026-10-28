import pathlib, sys
root = pathlib.Path(sys.argv[1]); out = root / 'ledgers/CF1/mutants/CF1-a-r11'
L01 = (root / 'tests/labs/CF1/lab-CF1-L01-1.py').read_text()
L02 = (root / 'tests/labs/CF1/lab-CF1-L02-1.py').read_text()
# n07: shield check that cannot fail for the identity: identity check drops the shield term (must be killed)
old = '        identity_ok = identity_ok and abs(ocf - (ebitda * (1 - TAX_RATE) + shield)) < TOLERANCE'
assert L02.count(old) == 1
(out / 'n07_l02_identity_check_drops_shield_term.py').write_text(L02.replace(old, '        identity_ok = identity_ok and abs(ocf - ebitda * (1 - TAX_RATE)) < TOLERANCE'))
# alt correct implementations (not mutants): Horner-form NPV, must print identical output
oldL1 = '    total = 0.0\n    for t, flow in enumerate(flows_cents):\n        total += flow / 100.0 / (1.0 + rate) ** t\n    return total'
assert L01.count(oldL1) == 1
alt1 = '    acc = 0.0\n    for flow in reversed(flows_cents):\n        acc = acc / (1.0 + rate) + flow / 100.0\n    return acc'
(root / 'ledgers/CF1/scripts/CF1-a-r11/alt_l01_horner.py').write_text(L01.replace(oldL1, alt1))
oldL2 = '    return sum(flow / (1.0 + rate) ** t for t, flow in enumerate(flows_dollars))'
assert L02.count(oldL2) == 1
alt2 = '    acc = 0.0\n    for flow in reversed(flows_dollars):\n        acc = acc / (1.0 + rate) + flow\n    return acc'
(root / 'ledgers/CF1/scripts/CF1-a-r11/alt_l02_horner.py').write_text(L02.replace(oldL2, alt2))
print('ok')
