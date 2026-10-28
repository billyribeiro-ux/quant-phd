import pathlib, sys
R = pathlib.Path(sys.argv[1]).read_text()
M = pathlib.Path(sys.argv[2])
old = 'def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:\n    """The budget flexed to a total of ``actual_units`` units at the budgeted mix, in cents."""\n    input_price, fixed, _, products = _case(case)'
new = ('def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:\n'
       '    """The budget flexed to a total of ``actual_units`` units at the budgeted mix, in cents."""\n'
       '    if isinstance(case, Mapping) and isinstance(case.get("products"), list):\n'
       '        case = dict(case)\n'
       '        case["products"] = [dict(p, name=p.get("name") or "_") if isinstance(p, Mapping) else p for p in case["products"]]\n'
       '    input_price, fixed, _, products = _case(case)')
assert R.count(old) == 1
src = R.replace(old, new)
body = src.split('"""', 2)[2].lstrip("\n")
(M / "r13e_04_flexible_budget_accepts_empty_names.py").write_text('"""Student error: flexible_budget replaces an empty product name with a placeholder, so an empty name is accepted there."""\n' + body)
print("ok")
