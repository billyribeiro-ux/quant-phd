"""Round-7 repair: m23 and m27 referenced an undefined name `now` in income_statement (a NameError kill, not the
described error). This restores the unpacking so each mutant fails only through its described error."""

import pathlib

base = pathlib.Path("/tmp/verify7-AC1-d/ledgers/AC1/mutants")
for name, old, new in [
    ("m23_sales_is_balance_not_flow.py", '    _, _, flow = _flows(ledger, period_end)\n    sales = -now["sales"]',
     '    now, _, flow = _flows(ledger, period_end)\n    sales = -now["sales"]'),
    ("m27_cogs_from_balance_not_flow.py", '    _, _, flow = _flows(ledger, period_end)\n    sales = -flow["sales"]\n    cost = now["cost_of_goods_sold"]',
     '    now, _, flow = _flows(ledger, period_end)\n    sales = -flow["sales"]\n    cost = now["cost_of_goods_sold"]'),
]:
    p = base / name
    text = p.read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, text.count(old))
    p.write_text(text.replace(old, new), encoding="utf-8")
    print("repaired", name)
