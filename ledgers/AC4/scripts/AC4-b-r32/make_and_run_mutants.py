import html, pathlib, re, subprocess, sys
root = pathlib.Path("/tmp/verify32-AC4-b")
PY = str(root / ".venv/bin/python")
out_dir = root / "ledgers/AC4/mutants/AC4-b-r32"
scratch = pathlib.Path("/tmp/AC4-v/AC4-b/r32/mut")
scratch.mkdir(parents=True, exist_ok=True)
MUT = [
 ("L03", "m_L03_decision_inverted",
  "Student docstring: the relevant-cost rule is coded with the comparison reversed (make when the net buy cost is lower).",
  '    return "buy" if net_buy_cost(c) < avoidable_make_cost(c) else "make"',
  '    return "make" if net_buy_cost(c) < avoidable_make_cost(c) else "buy"'),
 ("L03", "m_L03_excess_hours_unclamped",
  "Student omits the max(0, ...) clamp on excess hours (equivalent on this data: 6,000 - 4,000 is positive).",
  "    excess_hours = max(0, order_hours - spare_hours)",
  "    excess_hours = order_hours - spare_hours"),
 ("L04", "m_L04_exact_check_removed",
  "Student replaces the exact-division check in exact_rate with floor division (no ValueError on uneven pools).",
  '    if cost % driver_total != 0:\n        raise ValueError(f"{label}: {cost} does not divide evenly by {driver_total} driver units")\n    return cost // driver_total',
  "    return cost // driver_total"),
 ("L04", "m_L04_stage_one_counts_reversed",
  "Student zips stage-one driver counts against the products in reverse order (X gets Y's setup count).",
  "        for product, count in zip(products, pool.driver_counts, strict=True):\n            totals[product.name] += rate * count",
  "        for product, count in zip(reversed(products), pool.driver_counts, strict=True):\n            totals[product.name] += rate * count"),
]
for unit, name, doc, old, new in MUT:
    src0 = (root / f"tests/labs/AC4/lab-AC4-{unit}-1.py").read_text(encoding="utf-8")
    page = (root / f"course/modules/AC/AC4/{unit}.html").read_text(encoding="utf-8")
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).rstrip("\n")
    n = src0.count(old)
    if n != 1:
        print(name, "PATTERN COUNT", n); continue
    src = src0.replace(old, new)
    src = src.replace('"""AC4 lab', '"""' + doc + "\n\nAC4 lab", 1)
    p = scratch / f"{name}.py"
    p.write_text(src, encoding="utf-8")
    (out_dir / f"{name}.py").write_text(src, encoding="utf-8")
    r = subprocess.run([PY, "-I", "-W", "error", str(p)], capture_output=True, text=True)
    print(name, "exit", r.returncode, "stdout_matches_expected", r.stdout.rstrip("\n") == exp, "stderr_tail", r.stderr.strip()[-100:].replace("\n", " | "))
