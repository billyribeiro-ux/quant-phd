from pathlib import Path
REF = Path("/tmp/verify14-CF1-d/course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("/tmp/CF1-v/d14/alts_r14"); OUT.mkdir(parents=True, exist_ok=True)
subs = {
 "alt_r14_a_payback_running_factor.py": [(
  "    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n",
  "    factor, discounted = 1.0, []\n    for cf in flows:\n        discounted.append(cf * factor)\n        factor /= 1.0 + rate\n")],
 "alt_r14_b_monte_carlo_ratio_correction.py": [(
  "        m = math.exp(volatility * z - volatility * volatility / 2.0)\n",
  "        m = math.exp(volatility * z) / math.exp(volatility * volatility / 2.0)\n")],
 "alt_r14_c_fisher_expanded_form.py": [(
  "    return (1.0 + real) * (1.0 + inflation) - 1.0\n",
  "    return real + inflation + real * inflation\n")],
}
for name, reps in subs.items():
    body = REF
    for old, new in reps:
        assert body.count(old) == 1, (name, body.count(old))
        body = body.replace(old, new)
    (OUT / name).write_text(body, encoding="utf-8"); print("wrote", name)
