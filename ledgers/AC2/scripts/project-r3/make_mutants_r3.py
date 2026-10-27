"""Round 3 scratch generator: writes complete student-error mutants of the reference into ledgers/AC2/mutants/.

Each mutant is reference.py with one replacement (asserted to match exactly once) and a one-line docstring.
"""
import re
from pathlib import Path

REF = Path("/tmp/verify-ac2-p/course/modules/AC/AC2/grader/reference.py")
OUT = Path("/tmp/verify-ac2-p/ledgers/AC2/mutants")

MUTANTS = [
    ("p14_standardize_reads_every_unit_of_a_tag.py",
     "p14: standardize reads the observations of every unit of a tag, not only USD for money and shares for share counts.",
     [('observations = entry.get("units", {}).get(unit, [])',
       'observations = [o for lst in entry.get("units", {}).values() for o in lst]')]),
    ("p15_accn_read_by_direct_indexing.py",
     "p15: standardize reads obs['accn'] by direct indexing, so an annual observation without an accession number raises KeyError.",
     [('accn = str(obs.get("accn", "") or "")', 'accn = str(obs["accn"])')]),
    ("p16_tie_break_orders_form_before_accn.py",
     "p16: the as-of tie-break orders (filed, form, accn), so on one filing date the form string decides and not the accession number.",
     [('candidates.setdefault(end.isoformat(), []).append((filed, accn, value))',
       'candidates.setdefault(end.isoformat(), []).append((filed, (form, accn), value))')]),
    ("p17_modified_jones_needs_five_firm_years.py",
     "p17: modified_jones requires five firm-years, one more than the four the contract states, so a four-row sample is rejected.",
     [("if len(rows) < 4:", "if len(rows) < 5:")]),
    ("p18_modified_jones_finiteness_skips_regressors.py",
     "p18: modified_jones checks the finiteness of total accruals and lagged assets only, so NaN or infinite revenue or receivables changes pass.",
     [('vals = {key: _number(row[key], f"{key} of firm-year {i}") for key in _MJ_KEYS}',
       'vals = {key: (float(row[key]) if key in ("d_revenue", "d_receivables") else _number(row[key], f"{key} of firm-year {i}")) for key in _MJ_KEYS}'),
      ('if not (np.all(np.isfinite(y)) and np.all(np.isfinite(design))):',
       'if not np.all(np.isfinite(y)):')]),
    ("p19_accruals_cash_flow_plain_division.py",
     "p19: accruals_cash_flow divides by average total assets with plain division, so a zero average raises ZeroDivisionError.",
     [('return _div(_get(statements, end, "net_income") - _get(statements, end, "cfo"), avg_assets, "average assets")',
       'return (_get(statements, end, "net_income") - _get(statements, end, "cfo")) / avg_assets')]),
    ("p20_piotroski_roa_plain_division.py",
     "p20: piotroski_f_score divides net income by the previous year's assets with plain division, so zero previous-year assets raises ZeroDivisionError.",
     [('roa = _div(_get(statements, t, "net_income"), ta_t1, "total assets of the previous year")',
       'roa = _get(statements, t, "net_income") / ta_t1')]),
    ("p21_piotroski_shares_by_direct_indexing.py",
     "p21: piotroski_f_score reads the period's shares_outstanding by direct indexing, so a missing share count raises KeyError.",
     [('shares = _get(statements, t, "shares_outstanding")', 'shares = statements[t]["shares_outstanding"]')]),
    ("p22_shares_read_in_usd_unit.py",
     "p22: standardize reads shares_outstanding in unit USD, so no share count is ever standardized.",
     [('unit = "shares" if item == "shares_outstanding" else "USD"', 'unit = "USD"')]),
    ("p23_dupont_leverage_uses_year_end_equity.py",
     "p23: DuPont leverage divides average assets by year-end equity while roe still uses average equity.",
     [('"leverage": _div(avg_assets, avg_equity, "average equity"),',
       '"leverage": _div(avg_assets, _get(statements, end, "equity"), "equity"),')]),
    ("p24_accruals_balance_sheet_year_end_assets.py",
     "p24: accruals_balance_sheet scales by year-end total assets instead of average total assets.",
     [('return _div(numerator, avg_assets, "average assets")',
       'return _div(numerator, _get(statements, end, "total_assets"), "total assets")')]),
    ("p25_piotroski_signal4_cfo_scaled_by_year_end_assets.py",
     "p25: Piotroski signal 4 compares CFO scaled by year-end total assets with ROA scaled by beginning-of-year assets.",
     [("int(cfo > roa),", 'int(_get(statements, t, "cfo") / ta_t > roa),')]),
    ("p26_roic_invested_capital_adds_cash.py",
     "p26: ROIC invested capital adds cash instead of subtracting it.",
     [('return _get(statements, end, "equity") + _get(statements, end, "long_term_debt") - _get(statements, end, "cash")',
       'return _get(statements, end, "equity") + _get(statements, end, "long_term_debt") + _get(statements, end, "cash")')]),
    ("p27_modified_jones_lists_sorted_by_lag.py",
     "p27: modified_jones returns the residual lists sorted by lagged assets instead of in sample order.",
     [('"nondiscretionary": [float(v) for v in fitted],',
       '"nondiscretionary": [float(v) for _, v in sorted(zip(lag.tolist(), fitted.tolist()))],'),
      ('"discretionary": [float(v) for v in (y - fitted)],',
       '"discretionary": [float(v) for _, v in sorted(zip(lag.tolist(), (y - fitted).tolist()))],')]),
    ("p28_beneish_depi_without_depreciation_in_denominator.py",
     "p28: Beneish DEPI divides by PP&E alone instead of depreciation plus PP&E.",
     [('_div(dep1, dep1 + ppe1, "depreciation plus PP&E")', '_div(dep1, ppe1, "ppe")'),
      ('_div(dep, dep + ppe, "depreciation plus PP&E")', '_div(dep, ppe, "ppe")')]),
    ("p29_beneish_current_liabilities_by_direct_indexing.py",
     "p29: beneish_m_score reads the period's current liabilities by direct indexing, so a missing item raises KeyError.",
     [('_div(g(t, "current_liabilities") + g(t, "long_term_debt"), ta, "total assets"),',
       '_div(statements[t]["current_liabilities"] + g(t, "long_term_debt"), ta, "total assets"),')]),
    ("p30_tie_break_prefers_plain_10k_on_one_date.py",
     "p30: on one filing date the plain 10-K beats a 10-K/A whatever the accession numbers say.",
     [('candidates.setdefault(end.isoformat(), []).append((filed, accn, value))',
       'candidates.setdefault(end.isoformat(), []).append((filed, (form == "10-K", accn), value))')]),
    ("p31_piotroski_signal5_weak_inequality.py",
     "p31: Piotroski signal 5 uses a weak inequality (leverage not higher), so an exact tie scores 1.",
     [("int(lev < lev_prev),", "int(lev <= lev_prev),")]),
    ("p32_piotroski_signal7_strict_inequality.py",
     "p32: Piotroski signal 7 uses a strict inequality, so unchanged share counts (no issuance) score 0.",
     [("int(shares <= shares_prev),", "int(shares < shares_prev),")]),
    ("p33_piotroski_leverage_uses_total_liabilities.py",
     "p33: Piotroski leverage (signal 5) uses total liabilities instead of long-term debt.",
     [('lev = _div(_get(statements, t, "long_term_debt"), _average(ta_t, ta_t1), "average total assets")',
       'lev = _div(_get(statements, t, "total_liabilities"), _average(ta_t, ta_t1), "average total assets")'),
      ('lev_prev = _div(_get(statements, t1, "long_term_debt"), _average(ta_t1, ta_t2), "average total assets")',
       'lev_prev = _div(_get(statements, t1, "total_liabilities"), _average(ta_t1, ta_t2), "average total assets")')]),
    ("p34_piotroski_current_ratio_over_total_assets.py",
     "p34: Piotroski signal 6 uses current assets over total assets as the current ratio.",
     [('cr = _div(_get(statements, t, "current_assets"), _get(statements, t, "current_liabilities"), "liabilities")',
       'cr = _div(_get(statements, t, "current_assets"), ta_t, "total assets")'),
      ('cr_prev = _div(_get(statements, t1, "current_assets"), _get(statements, t1, "current_liabilities"), "liabilities")',
       'cr_prev = _div(_get(statements, t1, "current_assets"), ta_t1, "total assets")')]),
]


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    for name, doc, reps in MUTANTS:
        text = ref
        for old, new in reps:
            n = text.count(old)
            assert n == 1, f"{name}: pattern matched {n} times: {old[:70]}"
            text = text.replace(old, new)
        m = re.match(r'""".*?"""', text, re.S)
        assert m, name
        text = f'"""{doc}"""' + text[m.end():]
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()


MUTANTS_R3B = [
    ("p35_accruals_cash_flow_zero_average_raises_zero_division.py",
     "p35: accruals_cash_flow raises ZeroDivisionError, not ValueError, when the average total assets is zero.",
     [('    return _div(_get(statements, end, "net_income") - _get(statements, end, "cfo"), avg_assets, "average assets")',
       '    if avg_assets == 0.0:\n        raise ZeroDivisionError("average total assets is zero")\n'
       '    return _div(_get(statements, end, "net_income") - _get(statements, end, "cfo"), avg_assets, "average assets")')]),
    ("p36_accruals_balance_sheet_plain_division.py",
     "p36: accruals_balance_sheet divides by average total assets with plain division, so a zero average raises ZeroDivisionError.",
     [('return _div(numerator, avg_assets, "average assets")', 'return numerator / avg_assets')]),
    ("p37_conflict_check_skipped_when_accn_missing.py",
     "p37: two annual observations that tie on filing date with no accession number and different values are not reported as a conflict.",
     [('and top[2] != runner_up[2]', 'and top[2] != runner_up[2] and top[1] != ""')]),
]


def main_b() -> None:
    ref = REF.read_text(encoding="utf-8")
    for name, doc, reps in MUTANTS_R3B:
        text = ref
        for old, new in reps:
            n = text.count(old)
            assert n == 1, f"{name}: pattern matched {n} times: {old[:70]}"
            text = text.replace(old, new)
        m = re.match(r'""".*?"""', text, re.S)
        text = f'"""{doc}"""' + text[m.end():]
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main_b()
