"""Writes this round's alternative correct implementations of the project labs (valid algorithms, other cutoffs), then runs each alone
under python -I -W error in a scratch dir holding data/fx_monthly.csv and compares its stdout with the matching page expected block."""
import html, pathlib, re, shutil, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1]).resolve()
twins = root / "tests/labs/LX1"
outdir = pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
PY = str(root / ".venv/bin/python")
SNAP = root / "course/assets/data/market/fx_monthly.csv"
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")

def expected(lab):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).rstrip()

ALTS = [
    ("lab-LX1-project-3.py", "r12alt1_lab3_pstdev_rescaled.py",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))",
     "    return statistics.pstdev(values) * math.sqrt(n / (n - 1))"),
    ("lab-LX1-project-3.py", "r12alt2_lab3_log_as_difference_of_logs.py",
     "    return [(month, math.log(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]",
     "    return [(month, math.log(float(rate)) - math.log(float(previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]"),
    ("lab-LX1-project-2.py", "r12alt3_lab2_burden_from_inverse_prices.py",
     "    return ___",
     None),  # replaced below with the completed blanks
    ("lab-LX1-project-1.py", "r12alt4_lab1_round_half_up_via_decimal.py",
     "    magnitude = math.floor(abs(value) + Fraction(1, 2))\n    return magnitude if value >= 0 else -magnitude",
     "    from decimal import ROUND_HALF_UP, Decimal\n    d = (Decimal(value.numerator) / Decimal(value.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP)\n    return int(d)"),
]
LAB2_ALT = [
    ("    return Fraction(nominal_cents) / price_level\n", "    return Fraction(nominal_cents) * Fraction(1) / price_level\n"),
    ("    return 100 * (start_price / end_price - 1)\n", "    return 100 * ((1 / end_price) - (1 / start_price)) / (1 / start_price)\n"),
]
results = []
for src, name, old, new in ALTS:
    text = (twins / src).read_text(encoding="utf-8")
    if name.startswith("r12alt3"):
        for old2, new2 in LAB2_ALT:
            assert text.count(old2) == 1, (name, old2)
            text = text.replace(old2, new2, 1)
    else:
        assert text.count(old) == 1, (name, text.count(old))
        text = text.replace(old, new, 1)
    (outdir / name).write_text(text, encoding="utf-8")
    lab = src[:-3]
    wd = tempfile.mkdtemp(prefix="r12alt-")
    try:
        (pathlib.Path(wd) / "data").mkdir()
        shutil.copy(SNAP, pathlib.Path(wd) / "data" / "fx_monthly.csv")
        shutil.copy(outdir / name, pathlib.Path(wd) / "alt.py")
        p = subprocess.run([PY, "-I", "-W", "error", str(pathlib.Path(wd) / "alt.py")], cwd=wd, capture_output=True, text=True)
    finally:
        shutil.rmtree(wd)
    ok = p.returncode == 0 and not p.stderr and p.stdout.rstrip() == expected(lab.replace("lab-LX1-project-", "lab-LX1-project-"))
    print(f"{name}: rc={p.returncode} stderr_empty={not p.stderr} matches_{lab}={ok}")
