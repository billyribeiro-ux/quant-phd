"""Write three round-7 alternative correct engines from the reference. Usage: python -I make_alts_r7.py <checkout>"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text()
out = root / "ledgers/CF1/scripts/CF1-d-r7/alts"
out.mkdir(parents=True, exist_ok=True)


def sub(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (old[:60], text.count(old))
    return text.replace(old, new)


# 1. Payback with exact rational arithmetic (Fraction), converted to float at the end.
p1 = sub(ref, "    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n    cumulative = discounted[0]\n"
         "    for t in range(1, len(discounted)):\n        if cumulative + discounted[t] >= 0.0:\n"
         "            return (t - 1) + (-cumulative) / discounted[t]\n        cumulative += discounted[t]\n    return math.inf\n",
         "    from fractions import Fraction\n    disc = [Fraction(cf) / Fraction(1.0 + rate) ** t for t, cf in enumerate(flows)]\n"
         "    cum = disc[0]\n    for t in range(1, len(disc)):\n        if cum + disc[t] >= 0:\n"
         "            return float((t - 1) + (-cum) / disc[t])\n        cum += disc[t]\n    return math.inf\n")
(out / "alt_r7_1_payback_exact_fractions.py").write_text(p1)

# 2. IRR grid of 20001 points (a finer grid, a different numerical cutoff) with 60 bisection halvings.
p2 = sub(ref, "_GRID_POINTS = 4001", "_GRID_POINTS = 20001")
p2 = sub(p2, "            for _ in range(200):", "            for _ in range(60):")
(out / "alt_r7_2_irr_grid_20001_points_60_halvings.py").write_text(p2)

# 3. Monte Carlo multiplier computed as a ratio of exponentials (same value, different rounding path).
p3 = sub(ref, "        m = math.exp(volatility * z - volatility * volatility / 2.0)",
         "        m = math.exp(volatility * z) / math.exp(volatility * volatility / 2.0)")
(out / "alt_r7_3_monte_carlo_exp_ratio.py").write_text(p3)
print("wrote 3 alternatives")
