"""Hand transplants of the mutants that the one-line transplant could not place, three NEW student-error
mutants (m19_*), and alternative correct implementations (alt19_*), each run on the CURRENT twin.

Usage: python -I new_mutants_and_alts.py <checkout> <scratch_dir>. Each variant is a string replacement on the
current twin; a replacement that does not match exactly once is reported as NOT-APPLIED (never silently skipped).
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
expected = {}
for page in ("L07", "L08"):
    text = (root / f"course/modules/AC/AC4/{page}.html").read_text(encoding="utf-8")
    expected[page] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)).strip()
src = {p: (root / f"tests/labs/AC4/lab-AC4-{p}-1.py").read_text(encoding="utf-8") for p in ("L07", "L08")}

VARIANTS = [
    # (name, page, kind, [(old, new), ...])
    ("r18_carry_L07_nonempty_strict", "L07", "mutant", [("    return t_min(c) <= t_max(c)\n", "    return t_min(c) < t_max(c)\n")]),
    ("r18_carry_L07_empty_count_ge", "L07", "mutant", [("empty = [c for c in fits if not nonempty(c)]", "empty = [c for c in fits if t_min(c) >= t_max(c)]")]),
    ("r18_carry_L07_feasible_strict", "L07", "mutant", [("feasible = [c for c in fits if nonempty(c)]", "feasible = [c for c in fits if t_min(c) < t_max(c)]")]),
    ("r18_carry_L07_skip_boundary_checks", "L07", "mutant", [("supplier_zero = sum(1 for c in fits if", "supplier_zero = sum(1 for c in fits if c.case_id != 0 and")]),
    ("r18_carry_L07_midpoint_not_halved", "L07", "mutant", [("    return (t_min(c) + t_max(c)) / 2\n", "    return (t_min(c) + t_max(c))\n")]),
    ("r18_carry_L08_ri_side_strict", "L08", "mutant", [("sign_ok = [(residual_income(d) >= 0)", "sign_ok = [(residual_income(d) > 0)")]),
    ("r17_carry_L08_ratio_ge_strict", "L08", "mutant", [("== (return_ratio(d) >= rate) for d in", "== (return_ratio(d) > rate) for d in")]),
    ("m19_L07_t_min_divides_by_capacity", "L07", "mutant", [("Fraction(displaced(c) * (c.p_m - c.v), c.q)", "Fraction(displaced(c) * (c.p_m - c.v), c.capacity)")]),
    ("m19_L07_firm_surplus_uses_buyer_ceiling_price", "L07", "mutant", [("return c.q * (c.r_net - c.v) - displaced(c) * (c.p_m - c.v)", "return c.q * (c.r_net - c.p_m) - displaced(c) * (c.p_m - c.v)")]),
    ("m19_L08_first_year_charge_over_life_plus_one", "L08", "mutant", [("first_year = SPEND // LIFE_YEARS", "first_year = SPEND // (LIFE_YEARS + 1)")]),
    ("m19_L08_residual_income_after_tax", "L08", "mutant", [("return Fraction(d.oi) - Fraction(RATE_BP, 10_000) * d.invested", "return Fraction(d.oi) * (10_000 - TAX_BP) / 10_000 - Fraction(RATE_BP, 10_000) * d.invested")]),
    ("alt19_L07_nonempty_via_surplus", "L07", "alt", [("    return t_min(c) <= t_max(c)\n", "    return firm_surplus(c) >= 0\n")]),
    ("alt19_L07_midpoint_as_offset", "L07", "alt", [("    return (t_min(c) + t_max(c)) / 2\n", "    return t_min(c) + (t_max(c) - t_min(c)) / 2\n")]),
    ("alt19_L08_sign_cross_multiplied_integers", "L08", "alt", [("sign_ok = [(residual_income(d) >= 0) == (return_ratio(d) >= rate) for d in [*divisions, BOUNDARY]]",
        "sign_ok = [((d.oi * 10_000 - RATE_BP * d.invested >= 0) == (d.oi * 10_000 >= RATE_BP * d.invested)) for d in [*divisions, BOUNDARY]]")]),
    ("alt19_L08_discord_by_product_sign", "L08", "alt", [("if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:", "if by_ri * by_ratio < 0:")]),
]

for name, page, kind, reps in VARIANTS:
    text = src[page]
    ok = True
    for old, new in reps:
        n = text.count(old)
        if n != 1:
            print(f"{name}: NOT-APPLIED (pattern found {n} times): {old[:70]!r}")
            ok = False
            break
        text = text.replace(old, new)
    if not ok:
        continue
    f = scratch / f"{name}.py"
    f.write_text(text, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, timeout=60)
    out = proc.stdout.strip()
    if proc.returncode != 0:
        verdict = f"KILLED rc={proc.returncode} ({proc.stderr.strip().splitlines()[-1][:70] if proc.stderr.strip() else ''})"
    elif out != expected[page]:
        verdict = "KILLED output-differs"
        diff = [a for a, b in zip(out.splitlines(), expected[page].splitlines()) if a != b][:1]
        verdict += f" first differing line: {diff}"
    else:
        verdict = "SURVIVED (output identical)"
    print(f"{kind} {name}: {verdict}")
