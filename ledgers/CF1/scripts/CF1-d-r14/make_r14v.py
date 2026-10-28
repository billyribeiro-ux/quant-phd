import sys
from pathlib import Path
REF = Path("/tmp/verify14-CF1-d/course/modules/CF/CF1/grader/reference.py")
OUT = Path("/tmp/verify14-CF1-d/ledgers/CF1/mutants")
src = REF.read_text(encoding="utf-8")
specs = {
 "r14v_01_rate_above_one_read_as_percent.py": (
  "A rate above 1 is read as a percentage and divided by 100 in npv, so a rate of 2.0 (200 percent a year) is discounted as 2 percent.",
  '    _check_rate(rate)\n    if len(flows) == 0:',
  '    _check_rate(rate)\n    if rate > 1.0:\n        rate = rate / 100.0\n    if len(flows) == 0:'),
 "r14v_02_payback_discounts_at_simple_interest.py": (
  "Discounted payback divides each flow by (1 + rate * t) (simple interest) instead of (1 + rate) ** t.",
  '    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n    cumulative = discounted[0]',
  '    discounted = [cf / (1.0 + rate * t) for t, cf in enumerate(flows)]\n    cumulative = discounted[0]'),
 "r14v_03_working_capital_share_of_cash_costs.py": (
  "Working capital is taken as nwc_share times the year's cash cost instead of its revenue.",
  '        nwc[t] = share * revenue[t - 1]',
  '        nwc[t] = share * costs[t - 1]'),
 "r14v_04_real_flows_deflated_by_simple_inflation.py": (
  "With real=True each flow is divided by 1 + inflation * t (simple inflation) instead of (1 + inflation) ** t.",
  '        flows = [cf / (1.0 + inflation) ** t for t, cf in enumerate(flows)]',
  '        flows = [cf / (1.0 + inflation * t) for t, cf in enumerate(flows)]'),
}
for name, (doc, old, new) in specs.items():
    assert src.count(old) == 1, (name, src.count(old))
    body = src.replace(old, new)
    # replace module docstring with the one-line error description
    first_end = body.index('"""', 3) + 3
    body = '"""' + doc + '"""' + body[first_end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
