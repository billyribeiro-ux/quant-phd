"""Write round-18 student-error mutants of the CF1 lab twins (verifier-authored, round 18)."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
twins = {
    "L01": root / "tests/labs/CF1/lab-CF1-L01-1.py",
    "L02": root / "tests/labs/CF1/lab-CF1-L02-1.py",
}
out = root / "ledgers/CF1/mutants/CF1-a-r18"
muts = {
    "r18_m01_l01_loan_without_interest_accrual": (
        "L01",
        "        balance = (1.0 + rate) * balance - flows_cents[t] / 100.0",
        "        balance = balance - flows_cents[t] / 100.0",
    ),
    "r18_m02_l01_annuity_one_year_long": (
        "L01",
        "    factor = (1.0 - (1.0 + rate) ** -years) / rate",
        "    factor = (1.0 - (1.0 + rate) ** -(years + 1)) / rate",
    ),
    "r18_m03_l01_additivity_subtracts_second_stream": (
        "L01",
        "combined = [a + b for a, b in zip(first, second, strict=True)]",
        "combined = [a - b for a, b in zip(first, second, strict=True)]",
    ),
    "r18_m04_l02_npv_drops_date_zero_outlay": (
        "L02",
        "npv = npv_dollars(flows, RATE)",
        "npv = npv_dollars(flows[1:], RATE)",
    ),
    "r18_m05_l02_shield_check_compares_ocf_not_difference": (
        "L02",
        "shield_ok = shield_ok and abs((ocf - ocf_without) - depreciation_cents * TAX_RATE) < TOLERANCE",
        "shield_ok = shield_ok and abs(ocf - depreciation_cents * TAX_RATE) < TOLERANCE",
    ),
    "r18_m06_l02_wc_at_eight_percent_of_revenue": (
        "L02",
        "nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
        "nwc_cents = [0] + [revenue_cents[t] // 8 for t in range(1, LIFE_YEARS)] + [0]",
    ),
}
for name, (twin, old, new) in muts.items():
    src = twins[twin].read_text()
    assert src.count(old) == 1, (name, src.count(old))
    (out / f"{name}.py").write_text(src.replace(old, new))
    print("wrote", name)
