"""Write new round-17 student-error mutants of the L02 twin and alternative correct implementations (checks: each replacement applied once)."""
import pathlib

ROOT = pathlib.Path('/tmp/verify17-CF1-a')
TWIN = (ROOT / 'tests/labs/CF1/lab-CF1-L02-1.py').read_text()
MUT = ROOT / 'ledgers/CF1/mutants/CF1-a-r17'
ALT = ROOT / 'ledgers/CF1/scripts/CF1-a-r17/alts'
MUT.mkdir(parents=True, exist_ok=True)
ALT.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    'r17_m01_l02_study_charged_at_present_value.py': (
        'with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100, *flows[1:]], RATE)',
        'with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100 / (1 + RATE), *flows[1:]], RATE)'),
    'r17_m02_l02_shield_printed_in_cents.py': (
        'print(f"depreciation shield per year, in dollars: {TAX_RATE * depreciation_cents / 100:.2f}")',
        'print(f"depreciation shield per year, in dollars: {TAX_RATE * depreciation_cents:.2f}")'),
    'r17_m03_l02_difference_sign_flipped.py': (
        'print(f"difference, in dollars: {npv - with_sunk:.2f}")',
        'print(f"difference, in dollars: {with_sunk - npv:.2f}")'),
    'r17_m04_l02_cost_draw_range_off_by_one.py': (
        'cost_cents.append(rng.randrange(20, 31) * 10_000)',
        'cost_cents.append(rng.randrange(20, 30) * 10_000)'),
}
# Probe (not a student error in its output): exact float equality in place of the tolerance.
PROBE = {
    'r17_probe_l02_identity_exact_equality.py': (
        'identity_ok = identity_ok and abs(ocf - (ebitda * (1 - TAX_RATE) + shield)) < TOLERANCE',
        'identity_ok = identity_ok and (ocf == ebitda * (1 - TAX_RATE) + shield)'),
}
# Alternative correct implementations: must print exactly the twin output.
ALTS = {
    'alt_r17_a_tolerance_1e9.py': (
        'abs(ocf - (ebitda * (1 - TAX_RATE) + shield)) < TOLERANCE',
        'abs(ocf - (ebitda * (1 - TAX_RATE) + shield)) < 1e-9'),
    'alt_r17_b_horner_npv.py': (
        'return sum(flow / (1.0 + rate) ** t for t, flow in enumerate(flows_dollars))',
        'acc = 0.0\n    for flow in reversed(flows_dollars):\n        acc = acc / (1.0 + rate) + flow\n    return acc'),
    'alt_r17_c_shield_from_difference_tolerance_1e4.py': (
        'abs((ocf - ocf_without) - depreciation_cents * TAX_RATE) < TOLERANCE',
        'abs((ocf - ocf_without) - depreciation_cents * TAX_RATE) < 1e-4'),
}

for table, folder in ((MUTANTS, MUT), (PROBE, MUT), (ALTS, ALT)):
    for name, (old, new) in table.items():
        assert TWIN.count(old) == 1, (name, TWIN.count(old))
        (folder / name).write_text(TWIN.replace(old, new))
        print('wrote', folder / name)
