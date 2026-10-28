import re, subprocess, sys, pathlib
PY = "/tmp/verify30-AC4-b/.venv/bin/python"
root = pathlib.Path("/tmp/verify30-AC4-b")
MUT = {
 "L03": [
  ("m_L03_book_value_in_relevant_cost", "return avoidable_make_cost(c) - net_buy_cost(c)", "return avoidable_make_cost(c) - net_buy_cost(c) + c.equipment_book_value // 100"),
  ("m_L03_fullcost_decision_uses_relevant", 'return "buy" if c.buy_price_per_unit < full_cost_per_unit(c) else "make"', 'return "buy" if c.buy_price_per_unit < c.material_per_unit + c.labour_per_unit + c.variable_overhead_per_unit + c.dedicated_fixed // c.units else "make"'),
  ("m_L03_special_order_naive_hours", "lost_contribution = excess_hours * displaced_contribution_per_hour", "lost_contribution = order_hours * displaced_contribution_per_hour"),
 ],
 "L04": [
  ("m_L04_stage_two_divides_by_hours", "return {p.name: rate * p.labour_hours for p in products}", "return {p.name: rate * p.labour_hours for p in products}"),
  ("m_L04_setups_driven_by_inspections", 'ActivityPool("setups", 4_000_000, (20, 60)),', 'ActivityPool("setups", 4_000_000, (100, 300)),'),
  ("m_L04_volume_rate_uses_units", "rate = exact_rate(pool, total_hours, \"labour-hour rate\")", "rate = exact_rate(pool, sum(p.units for p in products), \"labour-hour rate\")"),
 ],
}
for unit, muts in MUT.items():
    src0 = (root / f"tests/labs/AC4/lab-AC4-{unit}-1.py").read_text(encoding="utf-8")
    html = (root / f"course/modules/AC/AC4/{unit}.html").read_text(encoding="utf-8")
    import html as H
    exp = H.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html, re.S).group(1)).rstrip("\n")
    for name, old, new in muts:
        if src0.count(old) != 1:
            print(name, "PATTERN COUNT", src0.count(old)); continue
        src = src0.replace(old, new)
        p = pathlib.Path(f"/tmp/AC4-v/AC4-b/r30/mut/{name}.py"); p.write_text(src, encoding="utf-8")
        r = subprocess.run([PY, "-I", "-W", "error", str(p)], capture_output=True, text=True)
        same = r.stdout.rstrip("\n") == exp
        print(name, "exit", r.returncode, "stdout_matches_expected", same, "stderr", r.stderr.strip()[-120:])
