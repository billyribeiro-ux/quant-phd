import re, html, subprocess, sys, pathlib
root = pathlib.Path("/tmp/verify18-AC4-a")
outdir = root / "ledgers/AC4/mutants/AC4-a-r18"
outdir.mkdir(parents=True, exist_ok=True)
def expected(page):
    s = (root / "course/modules/AC/AC4" / f"{page}.html").read_text(encoding="utf-8")
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1)).rstrip("\n")
L01 = [
 ("m01_high_is_lowest_month", "high = max(range(len(rows)), key=lambda i: (rows[i][0], -i))", "high = min(range(len(rows)), key=lambda i: (rows[i][0], -i))"),
 ("m02_residual_sign_flipped", "residual = Fraction(cost) - (fixed + variable * hours)", "residual = (fixed + variable * hours) - Fraction(cost)"),
 ("m03_largest_signed_not_absolute", "max(abs(r) for r in residuals)", "max(residuals)"),
 ("m04_nonzero_count_counts_positive_only", "sum(1 for r in residuals if r != 0)", "sum(1 for r in residuals if r > 0)"),
]
L02 = [
 ("m01_first_whole_unit_floor", "first_whole = -(-first.numerator // first.denominator)", "first_whole = first.numerator // first.denominator"),
 ("m02_scan_limit_2000", "SCAN_LIMIT_UNITS = 5000", "SCAN_LIMIT_UNITS = 2000"),
 ("m03_step_applied_from_2000", "if units > STEP_ABOVE_UNITS", "if units >= STEP_ABOVE_UNITS"),
 ("m04_margin_of_safety_single_formula", "safety = PLANNED_UNITS - upper", "safety = PLANNED_UNITS - first"),
 ("m05_zero_margin_accepted", "if margin <= 0:", "if margin < 0:"),
 ("m06_planned_income_before_step", "planned = operating_income(PLANNED_UNITS)", "planned = (PRICE_CENTS - VARIABLE_CENTS) * PLANNED_UNITS - FIXED_CENTS"),
]
rows = []
for page, muts, twin in (("L01", L01, "lab-AC4-L01-1.py"), ("L02", L02, "lab-AC4-L02-1.py")):
    src = (root / "tests/labs/AC4" / twin).read_text(encoding="utf-8")
    exp = expected(page)
    for name, old, new in muts:
        assert src.count(old) == 1, (name, src.count(old))
        mut = src.replace(old, new, 1)
        p = outdir / f"{page}_{name}.py"
        p.write_text(mut, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd="/tmp")
        got = r.stdout.rstrip("\n")
        status = "KILLED" if (got != exp or r.returncode != 0) else "SURVIVED"
        print(page, name, status, "exit", r.returncode)
        rows.append((page, name, status))
