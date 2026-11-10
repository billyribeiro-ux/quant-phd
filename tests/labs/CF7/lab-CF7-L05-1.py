"""Lab CF7-L05-1: Model Integrity Checks & Spreadsheet Error Risk.

Demonstrates automated integrity diagnostics by simulating the Herndon, Ash & Pollin
spreadsheet range omission defect and running automated checks for balance articulation
and hard-coded calculation literals.
"""

from __future__ import annotations

import re


def simulate_herndon_error() -> tuple[float, float, float]:
    """Reconstruct the Reinhart-Rogoff spreadsheet range omission documented by Herndon et al. (2014).

    The spreadsheet formula averaged cells L30:L44 instead of L30:L49, omitting
    Australia, Austria, Belgium, Canada, and Denmark from the high-debt (>90%) bucket.
    """
    # 20 countries' average real GDP growth in the high debt-to-GDP category (>90%)
    # Countries 1 to 15 (included in L30:L44):
    included_rates = [2.4, 1.4, -0.1, 2.3, 1.0, 3.0, 1.7, 2.4, 1.1, -0.4, 2.5, 0.6, 1.9, 2.2, -2.1]
    # Countries 16 to 20 (omitted due to Excel range truncation L30:L44):
    omitted_rates = [3.8, 4.0, 2.5, 3.0, 2.1]

    all_rates = included_rates + omitted_rates

    reported_avg = sum(included_rates) / len(included_rates)
    corrected_avg = sum(all_rates) / len(all_rates)
    bias = reported_avg - corrected_avg

    return reported_avg, corrected_avg, bias


def audit_formula_hardcodes(formulas: dict[str, str]) -> list[str]:
    """Detect hard-coded numbers inside calculation formulas."""
    allowed = {"0", "1", "2", "365", "360", "0.0", "1.0"}
    num_pattern = re.compile(r"(?<![A-Za-z$])(\d+(?:\.\d+)?)")
    violations: list[str] = []

    for cell, formula in formulas.items():
        if not formula.startswith("="):
            continue
        for num in num_pattern.findall(formula):
            if num not in allowed:
                violations.append(f"{cell}:{num}")

    return violations


def main() -> None:
    rep, corr, bias = simulate_herndon_error()
    print("Reported Growth (Truncated Range):", f"{rep:.4f}")
    print("Corrected Growth (Complete Range):", f"{corr:.4f}")
    print("Omission Bias:", f"{bias:.4f}")

    sample_formulas = {
        "C10": "=C8-C9",
        "C11": "=C10*0.25",  # Hard-coded 0.25
        "C12": "=(C5+C6)/2",
        "C13": "=C4*1.08",  # Hard-coded 1.08
    }
    violations = audit_formula_hardcodes(sample_formulas)
    print("Detected Hardcode Count:", str(len(violations)))
    print("Violations Found:", ", ".join(violations))


main()
