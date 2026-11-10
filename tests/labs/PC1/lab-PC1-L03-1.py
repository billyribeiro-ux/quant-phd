"""PC1 Lab L03-1: Standalone-table checklist and truncated-axis distortion ratio.

SIMULATED. Illustrative regression table schema and bar chart axis metrics.
Curriculum lab: Table and figure redesign drill.
All arithmetic uses exact fractions. Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class TableSchema:
    title: str
    column_headers: list[str]
    column_units: list[str]
    notes: str
    sample_size_n: int
    has_standard_errors: bool
    has_defined_symbols: bool


def validate_standalone_table(table: TableSchema) -> dict[str, bool]:
    """Verify that a table satisfies all 6 requirements of a standalone table."""
    # 1. Title must state finding or economic relation, not generic words alone
    generic_titles = {"regression results", "table 1", "estimates", "models"}
    title_informative = table.title.lower().strip() not in generic_titles and len(table.title.split()) >= 4

    # 2. Every column must have non-empty unit
    units_complete = len(table.column_units) == len(table.column_headers) and all(
        len(u.strip()) > 0 for u in table.column_units
    )

    # 3. Standard errors must be present and error type stated in notes
    notes_lower = table.notes.lower()
    se_type_stated = table.has_standard_errors and (
        "standard error" in notes_lower or "se in" in notes_lower or "clustered" in notes_lower
    )

    # 4. Sample size N explicitly reported
    sample_size_reported = table.sample_size_n > 0 and (
        "n =" in notes_lower or "observations" in notes_lower or f"{table.sample_size_n}" in table.notes
    )

    # 5. Significance symbols (* or p-values) defined in notes
    significance_defined = ("*" in notes_lower and "p <" in notes_lower) or "p-value" in notes_lower

    # 6. All symbols/acronyms defined
    symbols_defined = table.has_defined_symbols

    return {
        "Finding in title": title_informative,
        "Units on all columns": units_complete,
        "Standard error type specified": se_type_stated,
        "Sample size N reported": sample_size_reported,
        "Significance symbols defined": significance_defined,
        "Symbols and acronyms defined": symbols_defined,
    }


def compute_axis_distortion(y1: int, y2: int, baseline: int) -> tuple[Fraction, Fraction, Fraction]:
    """Compute true ratio, truncated visible ratio, and distortion factor."""
    true_ratio = Fraction(y1, y2)
    h1 = y1 - baseline
    h2 = y2 - baseline
    trunc_ratio = Fraction(h1, h2)
    distortion_factor = true_ratio / trunc_ratio
    return true_ratio, trunc_ratio, distortion_factor


def main() -> None:
    print("PC1 Lab L03-1: Table and Figure Redesign Drill")
    print("SIMULATED data and schemas")

    # Part 1: Table Redesign Checklist
    print("\n--- Part 1: Standalone-Table Checklist ---")
    weak_table = TableSchema(
        title="Regression Results",
        column_headers=["Model 1", "Model 2"],
        column_units=["", ""],
        notes="Standard errors in parentheses. * p < 0.05.",
        sample_size_n=0,
        has_standard_errors=True,
        has_defined_symbols=False,
    )

    redesigned_table = TableSchema(
        title="Institutional Cross-Ownership and Physical Investment Across Manufacturing Firms",
        column_headers=["Physical CAPX", "R&D Expenditure"],
        column_units=["% of Total Assets", "% of Total Assets"],
        notes=(
            "Standard errors clustered at the firm level reported in parentheses. "
            "N = 14,820 firm-year observations from Compustat manufacturing universe (SIC 2000-3999), 1990-2020. "
            "* p < 0.10, ** p < 0.05, *** p < 0.01. "
            "CAPX denotes capital expenditures; SIC denotes Standard Industrial Classification."
        ),
        sample_size_n=14820,
        has_standard_errors=True,
        has_defined_symbols=True,
    )

    weak_checks = validate_standalone_table(weak_table)
    print("Weak table checks:")
    for k, v in weak_checks.items():
        print(f"  {k:32s}: {v}")
    print(f"Weak table passes all checklist items: {all(weak_checks.values())}")

    redesigned_checks = validate_standalone_table(redesigned_table)
    print("\nRedesigned standalone table checks:")
    for k, v in redesigned_checks.items():
        print(f"  {k:32s}: {v}")
    print(f"Redesigned table passes all checklist items: {all(redesigned_checks.values())}")

    # Part 2: Figure Redesign: Truncated Axis Distortion
    print("\n--- Part 2: Truncated-Axis Bar Chart Distortion ---")
    y1, y2 = 92, 100
    baseline = 90
    true_ratio, trunc_ratio, distortion = compute_axis_distortion(y1, y2, baseline)

    print(f"True values: y1 = {y1}, y2 = {y2}")
    print(f"True ratio (y1 / y2): {true_ratio} ({float(true_ratio):.4f})")
    print(f"Truncated baseline: y0 = {baseline}")
    print(f"Visible bar heights: h1 = {y1 - baseline}, h2 = {y2 - baseline}")
    print(f"Visible ratio (h1 / h2): {trunc_ratio} ({float(trunc_ratio):.4f})")
    print(f"Distortion factor (true / visible): {distortion} ({float(distortion):.2f}x exaggeration)")
    print(f"Exact ratio discrepancy: {true_ratio - trunc_ratio} ({float(true_ratio - trunc_ratio):.4f})")


main()
