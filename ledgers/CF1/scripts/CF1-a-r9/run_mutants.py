"""Round 9 mutant runner for CF1 slice a (labs of L01 and L02).

Each mutant is a text edit of the lab twin. A mutant is killed when the run fails or its stdout differs
from the expected output embedded in the page. Run as: python -I run_mutants.py <checkout>
"""

from __future__ import annotations

import html
import pathlib
import re
import subprocess
import sys

CHECKOUT = pathlib.Path(sys.argv[1])
MUT_DIR = CHECKOUT / "ledgers/CF1/mutants/CF1-a-r9"
PY = CHECKOUT / ".venv/bin/python"

# (name, base lab, old text, new text, description) ; old must occur exactly once in the twin
MUTANTS = [
    # reconstructed from the round 8 mutant names (round 8 files not recoverable from the scratch folder)
    ("r4_m01_no_shield", "L02", "ocf = ebit - tax + depreciation_cents", "ocf = ebit - tax",
     "operating cash flow without the add-back of depreciation"),
    ("r4_m02_tax_on_ebitda", "L02", "tax = TAX_RATE * ebit", "tax = TAX_RATE * ebitda",
     "tax charged on EBITDA instead of EBIT"),
    ("r4_m03_sunk_at_period1", "L02", "with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100, *flows[1:]], RATE)",
     "with_sunk = npv_dollars([flows[0], flows[1] - SUNK_STUDY_CENTS / 100, *flows[2:]], RATE)",
     "sunk cost charged at period 1"),
    ("r5_m04_nwc_recovered_late", "L02", "nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [revenue_cents[4] // 10]",
     "working capital not recovered at year 4"),
    ("r5_m05_nwc_prior_revenue", "L02", "nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "nwc_cents = [0] + [revenue_cents[t - 1] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "working capital set on the prior year's revenue"),
    ("r5_m06_shield_on_ebitda", "L02", "shield = TAX_RATE * depreciation_cents", "shield = TAX_RATE * ebitda",
     "shield computed on EBITDA"),
    ("r5_m07_loan_full_npv", "L01", "balance = npv_dollars(flows_cents, rate) - flows_cents[0] / 100.0",
     "balance = npv_dollars(flows_cents, rate)", "loan opened at the full NPV"),
    ("r5_m08_discount_from_one", "L01", "total += flow / 100.0 / (1.0 + rate) ** t",
     "total += flow / 100.0 / (1.0 + rate) ** (t + 1)", "discounting one period too far"),
    ("r6_m09_nwc_sign_flipped", "L02", "nwc_flow = -(nwc_cents[t] - nwc_cents[t - 1]) / 100",
     "nwc_flow = (nwc_cents[t] - nwc_cents[t - 1]) / 100", "working-capital sign flipped"),
    ("r6_m10_sunk_added", "L02", "with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100, *flows[1:]], RATE)",
     "with_sunk = npv_dollars([flows[0] + SUNK_STUDY_CENTS / 100, *flows[1:]], RATE)",
     "sunk cost added instead of charged"),
    ("r6_m11_npv_enumerate_from_one", "L02", "return sum(flow / (1.0 + rate) ** t for t, flow in enumerate(flows_dollars))",
     "return sum(flow / (1.0 + rate) ** t for t, flow in enumerate(flows_dollars, start=1))",
     "NPV enumerates from period one"),
    ("r7_m01_annuity_exponent_sign", "L01", "factor = (1.0 - (1.0 + rate) ** -years) / rate",
     "factor = (1.0 - (1.0 + rate) ** years) / rate", "annuity factor with the exponent sign flipped"),
    ("r7_m02_loan_repayment_added", "L01", "balance = (1.0 + rate) * balance - flows_cents[t] / 100.0",
     "balance = (1.0 + rate) * balance + flows_cents[t] / 100.0", "loan repayment added instead of subtracted"),
    ("r7_m03_sunk_added_back", "L02", "with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100, *flows[1:]], RATE)",
     "with_sunk = npv_dollars([flows[0] - SUNK_STUDY_CENTS / 100, *flows[1:]], RATE) + SUNK_STUDY_CENTS / 100",
     "sunk cost added back to the charged NPV"),
    # new round 9 mutants
    ("r9_m01_undiscounted_part_e", "L01", "print(f\"NPV at 20 percent, in dollars: {npv_dollars(counterexample, 0.20):.2f}\")",
     "print(f\"NPV at 20 percent, in dollars: {npv_dollars(counterexample, 0.0):.2f}\")",
     "Part E evaluates the undiscounted sum and labels it as the NPV"),
    ("r9_m02_annuity_missing_division", "L01", "factor = (1.0 - (1.0 + rate) ** -years) / rate",
     "factor = (1.0 - (1.0 + rate) ** -years)",
     "annuity factor without dividing by the rate"),
    ("r9_m03_wc_zero_end_not_start", "L02", "nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "nwc_cents = [revenue_cents[1] // 10] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "working capital already tied up at period 0 (flows no longer sum to zero)"),
    ("r9_m04_depr_over_three_years", "L02", "depreciation_cents = CAPEX_CENTS // LIFE_YEARS",
     "depreciation_cents = CAPEX_CENTS // (LIFE_YEARS - 1)",
     "straight-line over the wrong life"),
    ("r9_m05_nwc_percent_of_cost", "L02", "nwc_cents = [0] + [revenue_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "nwc_cents = [0] + [cost_cents[t] // 10 for t in range(1, LIFE_YEARS)] + [0]",
     "working capital set on cash costs instead of revenue"),
    ("r9_m06_replication_nodiscount_loan", "L01", "balance = (1.0 + rate) * balance - flows_cents[t] / 100.0",
     "balance = balance - flows_cents[t] / 100.0",
     "loan balance accrues no interest"),
]


def run(path: pathlib.Path) -> tuple[int, str]:
    proc = subprocess.run(
        [str(PY), "-I", "-W", "error", str(path)], capture_output=True, text=True, timeout=120, check=False
    )
    return proc.returncode, proc.stdout + proc.stderr


def expected_for(base: str) -> str:
    page = CHECKOUT / f"course/modules/CF/CF1/{base}.html"
    text = page.read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert m, base
    return html.unescape(m.group(1)).strip()


def main() -> int:
    MUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, base, old, new, desc in MUTANTS:
        twin = CHECKOUT / f"tests/labs/CF1/lab-CF1-{base}-1.py"
        src = twin.read_text(encoding="utf-8")
        count = src.count(old)
        if count != 1:
            rows.append((name, base, f"ANCHOR-COUNT-{count}", desc))
            continue
        mutated = src.replace(old, new)
        out_path = MUT_DIR / f"{name}.py"
        out_path.write_text(mutated, encoding="utf-8")
        rc, out = run(out_path)
        killed = rc != 0 or out.strip() != expected_for(f"L{base[1:]}").strip() if False else None
        exp = expected_for(base)
        killed = (rc != 0) or (out.strip() != exp)
        first = ""
        if killed and rc == 0:
            for a, b in zip(out.strip().splitlines(), exp.splitlines()):
                if a != b:
                    first = f"got {a!r} vs expected {b!r}"
                    break
        rows.append((name, base, "KILLED" if killed else "SURVIVED", f"{desc}; rc={rc}; {first}"))
    for name, base, status, desc in rows:
        print(f"{name}\t{base}\t{status}\t{desc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
