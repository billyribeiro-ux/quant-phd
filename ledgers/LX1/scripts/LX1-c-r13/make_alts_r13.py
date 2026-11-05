"""Round-13 alternative correct implementations of the project labs (other valid algorithms, other cutoffs).
Each is written from the matching twin by one exact text replacement, run alone under python -I -W error in a scratch
dir holding data/fx_monthly.csv, and its stdout compared with the page's expected block. Argument 1: checkout root."""
import html, pathlib, re, shutil, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
twins = root / "tests/labs/LX1"
PY = str(root / ".venv/bin/python")
SNAP = root / "course/assets/data/market/fx_monthly.csv"
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")

def expected(lab):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).rstrip()

ALTS = [
    ("lab-LX1-project-3.py", "r13alt1_lab3_welford_sd.py",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))",
     "    m, s = 0.0, 0.0\n    for k, value in enumerate(values, 1):\n        delta = value - m\n        m += delta / k\n        s += delta * (value - m)\n    return math.sqrt(s / (n - 1))"),
    ("lab-LX1-project-3.py", "r13alt2_lab3_log1p_change.py",
     "    return [(month, math.log(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]",
     "    return [(month, math.log1p(float((rate - previous) / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]"),
    ("lab-LX1-project-3.py", "r13alt3_lab3_format_not_half_up.py",
     "    return str(Decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))",
     "    return f\"{value:.{places}f}\""),
    ("lab-LX1-project-1.py", "r13alt4_lab1_decimal_exact_division.py",
     "    return Fraction(nominal_cents) / price_level",
     "    from decimal import Decimal, getcontext\n    getcontext().prec = 60\n    return Fraction(Decimal(nominal_cents) / Decimal(price_level.numerator) * Decimal(price_level.denominator))"),
]
for src, name, old, new in ALTS:
    text = (twins / src).read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, text.count(old))
    text = text.replace(old, new, 1)
    (out / name).write_text(text, encoding="utf-8")
    lab = src[:-3]
    wd = tempfile.mkdtemp(prefix="r13alt-")
    try:
        (pathlib.Path(wd) / "data").mkdir()
        shutil.copy(SNAP, pathlib.Path(wd) / "data" / "fx_monthly.csv")
        shutil.copy(out / name, pathlib.Path(wd) / "alt.py")
        p = subprocess.run([PY, "-I", "-W", "error", str(pathlib.Path(wd) / "alt.py")], cwd=wd, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    finally:
        shutil.rmtree(wd)
    ok = p.returncode == 0 and not p.stderr and p.stdout.rstrip() == expected(lab)
    print(f"{name}: rc={p.returncode} stderr={p.stderr.strip()[-200:]!r} matches_{lab}={ok}")
    if not ok:
        print(p.stdout)
