"""Writes round-6 alternative correct engines (alt_r6_*) by textual edits of the reference engine.

Usage: python3 make_alts_r6.py <checkout> <outdir>. Each edit must match exactly once. Every alternative must still
satisfy the specification on the project page; they differ only in cutoffs, algorithms and floating-point order.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
REF = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")

ALTS = {
    "alt_r6_1_grid_8001_points.py": [("_GRID_POINTS = 4001", "_GRID_POINTS = 8001")],
    "alt_r6_2_algebra_flows_and_fisher_expansion.py": [
        ("        tax = tax_rate * (ebitda - depreciation)\n        working_capital = -(nwc[t] - nwc[t - 1])\n"
         "        flows.append(ebitda - tax + working_capital)",
         "        operating = ebitda * (1.0 - tax_rate) + depreciation * tax_rate\n"
         "        working_capital = -(nwc[t] - nwc[t - 1])\n        flows.append(operating + working_capital)"),
        ("    return (1.0 + real) * (1.0 + inflation) - 1.0",
         "    return real + inflation + real * inflation"),
    ],
    "alt_r6_3_monte_carlo_exp_ratio.py": [
        ("        m = math.exp(volatility * z - volatility * volatility / 2.0)",
         "        m = math.exp(volatility * z) / math.exp(volatility * volatility / 2.0)"),
    ],
    "alt_r6_4_payback_inverse_power.py": [
        ("    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n    cumulative = discounted[0]\n    for t in range(1, len(discounted)):\n        if cumulative + discounted[t] >= 0.0:",
         "    discounted = [cf * (1.0 + rate) ** (-t) for t, cf in enumerate(flows)]\n    cumulative = discounted[0]\n    for t in range(1, len(discounted)):\n        if cumulative + discounted[t] >= 0.0:"),
    ],
    "alt_r6_5_irr_illinois_regula_falsi.py": [
        ("            lo, hi, f_lo = xs[k1], xs[k2], values[k1]\n            for _ in range(200):\n                mid = 0.5 * (lo + hi)\n                f_mid = poly(mid)\n                if f_mid == 0.0:\n                    lo = hi = mid\n                    break\n                if f_mid * f_lo < 0.0:\n                    hi = mid\n                else:\n                    lo, f_lo = mid, f_mid\n                if hi - lo <= 1e-15 * hi:\n                    break\n            roots_x.append(0.5 * (lo + hi))",
         "            lo, hi, f_lo = xs[k1], xs[k2], values[k1]\n            f_hi = values[k2]\n            side = 0\n            for _ in range(400):\n                mid = (lo * f_hi - hi * f_lo) / (f_hi - f_lo)\n                if not (lo < mid < hi):\n                    mid = 0.5 * (lo + hi)\n                f_mid = poly(mid)\n                if f_mid == 0.0:\n                    lo = hi = mid\n                    break\n                if f_mid * f_lo < 0.0:\n                    hi, f_hi = mid, f_mid\n                    if side == -1:\n                        f_lo *= 0.5\n                    side = -1\n                else:\n                    lo, f_lo = mid, f_mid\n                    if side == 1:\n                        f_hi *= 0.5\n                    side = 1\n                if hi - lo <= 1e-13 * hi:\n                    break\n            roots_x.append(0.5 * (lo + hi))"),
    ],
}

for name, edits in ALTS.items():
    text = REF
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: anchor count {text.count(old)}")
        text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
