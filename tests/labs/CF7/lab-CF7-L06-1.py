"""Lab CF7-L06-1: Model Reconciliation: Spreadsheets to Clean Code.

Implements an automated reconciliation engine comparing spreadsheet exports against
an independent Python three-statement model, detecting timing discrepancies and formula errors.
"""

from __future__ import annotations

from typing import Any


def reconcile_statements(
    sheet_export: dict[str, list[float]],
    code_model: dict[str, list[float]],
    rel_tol: float = 1e-4,
) -> tuple[bool, list[dict[str, Any]]]:
    """Compare statement line items and isolate discrepancies exceeding relative tolerance."""
    discrepancies: list[dict[str, Any]] = []

    for line_item, code_vals in code_model.items():
        if line_item not in sheet_export:
            continue
        sheet_vals = sheet_export[line_item]
        for t, (s_val, c_val) in enumerate(zip(sheet_vals, code_vals, strict=False)):
            diff = abs(s_val - c_val)
            allowable = rel_tol * (1.0 + abs(c_val))
            if diff > allowable:
                discrepancies.append(
                    {
                        "line_item": line_item,
                        "period": t + 1,
                        "sheet_val": s_val,
                        "code_val": c_val,
                        "difference": diff,
                    }
                )

    passed = len(discrepancies) == 0
    return passed, discrepancies


def main() -> None:
    # Code model reference values (Period 1, 2, 3)
    code_model: dict[str, list[float]] = {
        "revenue": [540.0, 577.8, 612.468],
        "ebitda": [135.0, 144.45, 153.117],
        "interest_expense": [6.5, 6.2, 5.8],
        "net_income": [96.375, 103.6875, 110.48775],
        "ending_cash": [52.4, 68.9, 87.2],
    }

    # Sheet export with a planted interest calculation defect in period 2
    # (e.g., using opening debt instead of average debt, or index lag)
    sheet_export_corrupted: dict[str, list[float]] = {
        "revenue": [540.0, 577.8, 612.468],
        "ebitda": [135.0, 144.45, 153.117],
        "interest_expense": [6.5, 7.5, 5.8],  # 7.5 vs 6.2
        "net_income": [96.375, 102.7125, 110.48775],
        "ending_cash": [52.4, 67.925, 87.2],
    }

    passed_corr, disc_corr = reconcile_statements(sheet_export_corrupted, code_model)
    print("Corrupted Model Passed:", str(passed_corr))
    print("Discrepancy Count:", str(len(disc_corr)))
    for d in disc_corr:
        print(f"Discrepancy: {d['line_item']} P{d['period']} diff={d['difference']:.4f}")

    # Reconciling clean export
    passed_clean, disc_clean = reconcile_statements(code_model, code_model)
    print("Clean Model Passed:", str(passed_clean))
    print("Clean Discrepancy Count:", str(len(disc_clean)))


main()
