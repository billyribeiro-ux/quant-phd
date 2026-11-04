"""Five alternative correct implementations per lab (LX1-c round 1). Usage: python3 -I run_alternatives.py <checkout>

Rung-2 alternatives must print the page's expected block (the instant check must not over-constrain). Lab-3
alternatives must print the page's expected block on the embedded snapshot.
"""
import html, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
SNAP = ROOT / "course/assets/data/market/fx_monthly.csv"
TWIN2 = (ROOT / "tests/labs/LX1/lab-LX1-project-2.py").read_text(encoding="utf-8")
TWIN3 = (ROOT / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")

def expected(lab_id):
    sec = PAGE[PAGE.index(f'id="{lab_id}"'):]
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))

def run(src, with_data):
    d = Path(tempfile.mkdtemp(prefix="lx1c-alt-"))
    if with_data:
        (d / "data").mkdir(); shutil.copy(SNAP, d / "data" / "fx_monthly.csv")
    f = d / "alt.py"; f.write_text(src, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], cwd=d, capture_output=True, text=True, timeout=60)
    shutil.rmtree(d)
    return r

def sub(src, old, new):
    assert old in src, old
    return src.replace(old, new, 1)

# ---- rung 2 alternatives (instant check) ----
exp2 = expected("lab-LX1-project-2")
alts2 = {
 "A1_int_over_fraction": [("return Fraction(nominal_cents) / price_level", "return nominal_cents / price_level")],
 "A2_multiply_reciprocal": [("return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents) * (1 / price_level)")],
 "A3_burden_ratio_minus_100": [("return 100 * (start_price / end_price - 1)", "return 100 * start_price / end_price - 100")],
 "A4_burden_percent_last": [("return 100 * (start_price / end_price - 1)", "return (start_price / end_price - 1) * 100")],
 "A5_burden_via_real_values": [("return 100 * (start_price / end_price - 1)", "return 100 * (Fraction(1) / end_price * start_price - 1)")],
}
for name, pairs in alts2.items():
    src = TWIN2
    for old, new in pairs:
        src = sub(src, old, new)
    r = run(src, False)
    ok = r.returncode == 0 and r.stdout == exp2 + "\n"
    print(f"rung2 {name}: rc={r.returncode} matches_expected={ok}")

# ---- lab 3 alternatives ----
exp3 = expected("lab-LX1-project-3")
alts3 = {
 "B1_statistics_stdev_for_sd": [("    sd = sample_sd_two_pass(values)", "    sd = statistics.stdev(values)")],
 "B2_log1p_changes": [("math.log(float(rate / previous))", "math.log1p(float(rate / previous) - 1.0)")],
 "B3_welford_sd": [("    sd = sample_sd_two_pass(values)",
                    "    mean_w = 0.0; m2 = 0.0\n    for k, v in enumerate(values, 1):\n        d1 = v - mean_w; mean_w += d1 / k; m2 += d1 * (v - mean_w)\n    sd = math.sqrt(m2 / (len(values) - 1))")],
 "B4_window_by_index": [('window_two = [item for item in changes if item[0] >= WINDOW_TWO_FROM]',
                         'window_two = changes[changes.index(next(c for c in changes if c[0] == WINDOW_TWO_FROM)):]')],
 "B5_stdev_from_fraction_mean": [("    mean = math.fsum(values) / n", "    mean = float(sum(Fraction(v) for v in values) / n)")],
}
for name, pairs in alts3.items():
    src = TWIN3
    for old, new in pairs:
        src = sub(src, old, new)
    r = run(src, True)
    ok = r.returncode == 0 and r.stdout == exp3 + "\n"
    print(f"lab3 {name}: rc={r.returncode} matches_expected={ok}" + ("" if ok else f" stderr_tail={(r.stderr.strip().splitlines() or [''])[-1][:120]}"))
