"""Run each L07/L08 lab-level mutant and each valid alternative implementation; report whether stdout equals the page's expected block."""
import difflib
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
mdir = pathlib.Path(sys.argv[2])
adir = pathlib.Path(sys.argv[3])
adir.mkdir(parents=True, exist_ok=True)
py = sys.executable
expected = {}
for lab in ("L07", "L08"):
    page = (root / f"course/modules/AC/AC4/{lab}.html").read_text(encoding="utf-8")
    expected[lab] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip()
L07 = (root / "tests/labs/AC4/lab-AC4-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/AC4/lab-AC4-L08-1.py").read_text(encoding="utf-8")
alts = {
    "alt_L07_min_form_displaced.py": ("L07", L07, "return max(0, c.q + c.external - c.capacity)",
                                      "return c.external - min(c.external, c.capacity - c.q)"),
    "alt_L07_nonempty_via_surplus.py": ("L07", L07, "empty = [c for c in fits if t_min(c) > t_max(c)]",
                                        "empty = [c for c in fits if firm_surplus(c) < 0]"),
    "alt_L07_decimal_floor.py": ("L07", L07, "return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v), c.q)",
                                 "from decimal import Decimal as _D\n    return Fraction(_D(c.v) + _D(displaced(c) * (c.p_m - c.v)) / _D(c.q))"),
    "alt_L08_float_ri.py": ("L08", L08, "return Fraction(d.oi) - Fraction(RATE_BP, 10_000) * d.invested",
                            "return Fraction(d.oi - (RATE_BP * d.invested) / 10_000)"),
    "alt_L08_rank_by_sign_of_diff.py": ("L08", L08, "if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:",
                                        "if (by_ri > 0 and by_ratio < 0) or (by_ri < 0 and by_ratio > 0):"),
}
for name, (lab, src, old, new) in alts.items():
    assert src.count(old) == 1, (name, src.count(old))
    (adir / name).write_text(src.replace(old, new, 1), encoding="utf-8")
jobs = [("mutant", p) for p in sorted(mdir.glob("*.py"))] + [("alt", p) for p in sorted(adir.glob("*.py"))]
for kind, p in jobs:
    lab = "L07" if "L07" in p.name else "L08"
    r = subprocess.run([py, "-I", "-W", "error", str(p)], capture_output=True, text=True, timeout=120)
    got = r.stdout.strip()
    same = got == expected[lab]
    verdict = "SAME_AS_EXPECTED" if same else "DIFFERS_FROM_EXPECTED"
    extra = ""
    if r.returncode != 0:
        extra = " exit=" + str(r.returncode) + " " + (r.stderr.strip().splitlines() or [""])[-1][:120]
    print(f"{kind} {p.name}: {verdict}{extra}")
    if not same and r.returncode == 0:
        d = [l for l in difflib.unified_diff(expected[lab].splitlines(), got.splitlines(), lineterm="", n=0)][2:6]
        for l in d:
            print("    ", l)
