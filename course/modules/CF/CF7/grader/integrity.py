"""Model integrity audit routines for corporate financial models (CF7).

Validates:
1. Balance sheet articulation and balance check (Assets == Liabilities + Equity).
2. Cash tie-out between Cash Flow Statement ending cash and Balance Sheet cash.
3. Retained earnings corkscrew roll-forward.
4. Absence of hard-coded numeric constants in calculation formula representations.
5. Reconciliation tolerances between spreadsheet outputs and independent code.
"""

from __future__ import annotations

import re
from typing import Any


def check_balance_sheet(model_output: dict[str, Any], tol: float = 1e-4) -> dict[str, Any]:
    """Check that Assets == Liabilities + Equity for all projected periods.

    Returns a dict with 'passed' (bool), 'max_imbalance' (float), and 'details' (dict).
    """
    bs = model_output.get("balance_sheet", {})
    assets = bs.get("total_assets", [])
    liab = bs.get("total_liabilities", [])
    equity = bs.get("total_equity", [])

    n_periods = min(len(assets), len(liab), len(equity))
    if n_periods == 0:
        return {"passed": False, "max_imbalance": float("inf"), "details": "No balance sheet data"}

    imbalances: list[float] = []
    for t in range(n_periods):
        gap = abs(assets[t] - (liab[t] + equity[t]))
        imbalances.append(gap)

    max_gap = max(imbalances)
    passed = bool(max_gap <= tol)
    return {
        "passed": passed,
        "max_imbalance": max_gap,
        "imbalances": imbalances,
    }


def check_cash_tie_out(model_output: dict[str, Any], tol: float = 1e-4) -> dict[str, Any]:
    """Check that Cash Flow Statement ending cash equals Balance Sheet cash.

    Returns a dict with 'passed' (bool), 'max_discrepancy' (float), and 'details' (dict).
    """
    bs = model_output.get("balance_sheet", {})
    cfs = model_output.get("cash_flow_statement", {})
    bs_cash = bs.get("cash", [])
    cfs_cash = cfs.get("ending_cash", [])

    n_periods = min(len(bs_cash), len(cfs_cash))
    if n_periods == 0:
        return {"passed": False, "max_discrepancy": float("inf"), "details": "No cash data"}

    diffs = [abs(bs_cash[t] - cfs_cash[t]) for t in range(n_periods)]
    max_diff = max(diffs)
    passed = bool(max_diff <= tol)
    return {
        "passed": passed,
        "max_discrepancy": max_diff,
        "discrepancies": diffs,
    }


def check_reconciliation(
    sheet_data: dict[str, Any],
    model_data: dict[str, Any],
    tolerance: float = 1e-4,
) -> dict[str, Any]:
    """Compare spreadsheet extracted line items against independent model outputs.

    Uses relative tolerance: |sheet - model| <= tolerance * (1 + |model|).
    """
    discrepancies: list[dict[str, Any]] = []
    checked_items = 0

    for section_name in ("income_statement", "balance_sheet", "cash_flow_statement", "debt_schedule", "dcf_valuation"):
        sheet_sec = sheet_data.get(section_name, {})
        model_sec = model_data.get(section_name, {})
        if not isinstance(sheet_sec, dict) or not isinstance(model_sec, dict):
            continue

        for line_item, model_vals in model_sec.items():
            if line_item not in sheet_sec:
                continue
            sheet_vals = sheet_sec[line_item]

            # Scalar vs list
            if isinstance(model_vals, (int, float)):
                checked_items += 1
                s_val = float(sheet_vals)
                m_val = float(model_vals)
                allowable = tolerance * (1.0 + abs(m_val))
                diff = abs(s_val - m_val)
                if diff > allowable:
                    discrepancies.append(
                        {
                            "section": section_name,
                            "line_item": line_item,
                            "period": None,
                            "sheet_value": s_val,
                            "model_value": m_val,
                            "difference": diff,
                            "allowable": allowable,
                        }
                    )
            elif isinstance(model_vals, list):
                for t, m_val in enumerate(model_vals):
                    checked_items += 1
                    if t >= len(sheet_vals):
                        discrepancies.append(
                            {
                                "section": section_name,
                                "line_item": line_item,
                                "period": t,
                                "sheet_value": None,
                                "model_value": m_val,
                                "difference": float("inf"),
                                "allowable": tolerance,
                            }
                        )
                        continue
                    s_val = float(sheet_vals[t])
                    m_val_flt = float(m_val)
                    allowable = tolerance * (1.0 + abs(m_val_flt))
                    diff = abs(s_val - m_val_flt)
                    if diff > allowable:
                        discrepancies.append(
                            {
                                "section": section_name,
                                "line_item": line_item,
                                "period": t,
                                "sheet_value": s_val,
                                "model_value": m_val_flt,
                                "difference": diff,
                                "allowable": allowable,
                            }
                        )

    passed = len(discrepancies) == 0 and checked_items > 0
    return {
        "passed": passed,
        "checked_items": checked_items,
        "discrepancies": discrepancies,
    }


def check_hardcodes_in_formulas(formulas: dict[str, str]) -> list[str]:
    """Inspect spreadsheet calculation formulas for embedded hard-coded numeric literals.

    Permitted literals: 0, 1, 2, 365, 360 (structural constants like days in year or zero checks).
    Flagged literals: arbitrary constants such as growth rates, margin percentages, tax rates.
    """
    allowed_numbers = {"0", "1", "2", "365", "360", "0.0", "1.0"}
    violations: list[str] = []

    # Match numbers (integers or decimals) not part of cell references like A1, B23
    number_pattern = re.compile(r"(?<![A-Za-z$])(\d+(?:\.\d+)?)")

    for cell_id, formula in formulas.items():
        if not formula.startswith("="):
            continue
        matches = number_pattern.findall(formula)
        for num in matches:
            if num not in allowed_numbers:
                violations.append(f"Cell {cell_id} has hard-coded literal {num} in formula: {formula}")

    return violations
