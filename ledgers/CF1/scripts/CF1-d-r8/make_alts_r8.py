"""Write three round-8 alternative correct engines derived from the reference. Usage: python -I make_alts_r8.py <checkout>"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text()
out = root / "ledgers/CF1/scripts/CF1-d-r8/alts"
out.mkdir(parents=True, exist_ok=True)


def sub(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (old[:70], text.count(old))
    return text.replace(old, new)


# 1. NPV by Horner's rule over the reversed flows, and the Fisher form r + i + r*i (different rounding path).
p1 = sub(ref, '    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))\n',
         '    acc = 0.0\n    for cf in reversed(flows):\n        acc = acc / (1.0 + rate) + cf\n    return acc\n')
p1 = sub(p1, "    return (1.0 + real) * (1.0 + inflation) - 1.0\n", "    return real + inflation + real * inflation\n")
(out / "alt_r8_1_horner_npv_and_expanded_fisher.py").write_text(p1)

# 2. Root refinement by bisection in log x (geometric midpoint) with a 1e-13 stopping width in log x; same grid.
p2 = sub(ref, "                mid = 0.5 * (lo + hi)\n", "                mid = math.sqrt(lo * hi)\n")
p2 = sub(p2, "                if hi - lo <= 1e-15 * hi:\n", "                if math.log(hi / lo) <= 1e-13:\n")
(out / "alt_r8_2_irr_geometric_bisection.py").write_text(p2)

# 3. Payback with math.fsum cumulative sums (different summation rounding) and a second payback cutoff form.
p3 = sub(ref, "        if cumulative + discounted[t] >= 0.0:\n            return (t - 1) + (-cumulative) / discounted[t]\n"
         "        cumulative += discounted[t]\n",
         "        nxt = math.fsum([cumulative, discounted[t]])\n        if nxt >= 0.0:\n"
         "            return (t - 1) + (-cumulative) / discounted[t]\n        cumulative = nxt\n")
(out / "alt_r8_3_payback_fsum.py").write_text(p3)
print("wrote", sorted(p.name for p in out.iterdir()))
