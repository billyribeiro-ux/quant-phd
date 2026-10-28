import pathlib
REF = pathlib.Path("/tmp/verify21-CF1-d/course/modules/CF/CF1/grader/reference.py").read_text()
old = "    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n    cumulative = discounted[0]\n    for t in range(1, len(discounted)):\n        if cumulative + discounted[t] >= 0.0:\n            return (t - 1) + (-cumulative) / discounted[t]\n        cumulative += discounted[t]\n    return math.inf\n"
new = ("    df = 1.0\n    discounted = []\n    for cf in flows:\n        discounted.append(cf * df)\n        df = df / (1.0 + rate)\n"
       "    cumulative = discounted[0]\n    for t in range(1, len(discounted)):\n        nxt = cumulative + discounted[t]\n"
       "        if nxt >= 0.0:\n            return (t - 1) + (-cumulative) / discounted[t]\n        cumulative = nxt\n    return math.inf\n")
assert REF.count(old) == 1
out = REF.replace(old, new)
pathlib.Path("/tmp/verify21-CF1-d/ledgers/CF1/scripts/CF1-d-r21/alts/alt_r21d_c_payback_running_discount_factor.py").write_text(out)
print("ok")
