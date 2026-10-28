import pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
ALT = pathlib.Path(sys.argv[2]); MUT = pathlib.Path(sys.argv[3])

def apply(src, edits):
    for old, new in edits:
        n = src.count(old)
        assert n == 1, (old[:70], n)
        src = src.replace(old, new, 1)
    return src

ALTS = {
 "alt_r10_1_irr_log_scan_20001_illinois.py": [
  ("    xs = [\n        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))\n        for k in range(_GRID_POINTS)\n    ]\n    xs[0], xs[-1] = _X_LOW, _X_HIGH\n    values = [poly(x) for x in xs]",
   "    n = 20001\n    xs = [math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (n - 1)) for k in range(n)]\n    xs[0], xs[-1] = _X_LOW, _X_HIGH\n    values = [poly(x) for x in xs]"),
  ("    nonzero = [k for k in range(_GRID_POINTS) if values[k] != 0.0]", "    nonzero = [k for k in range(n) if values[k] != 0.0]"),
  ("            lo, hi, f_lo = xs[k1], xs[k2], values[k1]\n            for _ in range(200):\n                mid = 0.5 * (lo + hi)\n                f_mid = poly(mid)\n                if f_mid == 0.0:\n                    lo = hi = mid\n                    break\n                if f_mid * f_lo < 0.0:\n                    hi = mid\n                else:\n                    lo, f_lo = mid, f_mid\n                if hi - lo <= 1e-15 * hi:\n                    break\n            roots_x.append(0.5 * (lo + hi))",
   "            lo, hi, f_lo, f_hi = xs[k1], xs[k2], values[k1], values[k2]\n            side = 0\n            for _ in range(300):\n                mid = (lo * f_hi - hi * f_lo) / (f_hi - f_lo)\n                if not (lo < mid < hi):\n                    mid = 0.5 * (lo + hi)\n                f_mid = poly(mid)\n                if f_mid == 0.0:\n                    lo = hi = mid\n                    break\n                if f_mid * f_lo < 0.0:\n                    hi, f_hi = mid, f_mid\n                    if side == -1:\n                        f_lo /= 2.0\n                    side = -1\n                else:\n                    lo, f_lo = mid, f_mid\n                    if side == 1:\n                        f_hi /= 2.0\n                    side = 1\n                if hi - lo <= 1e-15 * hi:\n                    break\n            roots_x.append(0.5 * (lo + hi))"),
 ],
 "alt_r10_2_payback_tolerance_1e12.py": [
  ("        if cumulative + discounted[t] >= 0.0:", "        if cumulative + discounted[t] >= -1e-12:"),
 ],
 "alt_r10_3_monte_carlo_ratio_form.py": [
  ("        m = math.exp(volatility * z - volatility * volatility / 2.0)", "        m = math.exp(volatility * z) / math.exp(volatility * volatility / 2.0)"),
 ],
 "alt_r10_4_tax_expanded_and_fsum_npv.py": [
  ("        tax = tax_rate * (ebitda - depreciation)\n        working_capital", "        tax = tax_rate * ebitda - tax_rate * depreciation\n        working_capital"),
  ("    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))", "    return math.fsum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))"),
 ],
 "alt_r10_5_fisher_log_identity.py": [
  ("    return (1.0 + real) * (1.0 + inflation) - 1.0", "    return math.expm1(math.log1p(real) + math.log1p(inflation))"),
 ],
}
MUTS = {
 "m54_grid_end_not_snapped_zero_at_window_end_reported.py": (
  "irr_roots reports a zero at the high window end: its grid end is exp(log(1e4)), one ulp above 10000, so a root at x = 10000 gets a sign change beyond it.",
  [("    xs[0], xs[-1] = _X_LOW, _X_HIGH\n", "")]),
 "m55_irr_roots_returned_descending.py": (
  "irr_roots returns the roots in the order the grid scan finds them, from the high rate end: descending rather than ascending.",
  [("    return sorted(1.0 / x - 1.0 for x in roots_x)", "    return sorted((1.0 / x - 1.0 for x in roots_x), reverse=True)")]),
 "m56_irr_sign_test_counts_zero_samples.py": (
  "irr_roots counts a grid sample with NPV exactly zero as a root, so a zero on the grid is reported even without a sign change.",
  [("    nonzero = [k for k in range(_GRID_POINTS) if values[k] != 0.0]", "    nonzero = [k for k in range(_GRID_POINTS) if values[k] != 0.0]\n    roots_x.extend(xs[k] for k in range(_GRID_POINTS) if values[k] == 0.0)")]),
 "m57_monte_carlo_scales_cash_costs_too.py": (
  "The student multiplies cash costs by the draw multiplier as well as revenue, so each draw scales the whole operating cash flow; the specification says cash costs are unchanged.",
  [('        scaled["revenue"] = [m * float(x) for x in project["revenue"]]', '        scaled["revenue"] = [m * float(x) for x in project["revenue"]]\n        scaled["cash_costs"] = [m * float(x) for x in project["cash_costs"]]')]),
}
for name, edits in ALTS.items():
    (ALT / name).write_text(apply(REF, edits), encoding="utf-8")
for name, (desc, edits) in MUTS.items():
    text = REF.replace('"""Reference solution for the CF1 capital-budgeting engine (capbudget.py).', '"""' + desc + "\n\nReference solution for the CF1 capital-budgeting engine (capbudget.py).", 1)
    (MUT / name).write_text(apply(text, edits), encoding="utf-8")
    print("wrote", name)
