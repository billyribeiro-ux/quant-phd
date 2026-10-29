"""Round 19 lab-twin mutation run for AC4-a (hub, L01, L02).

Re-runs the ten round-18 mutants committed under ledgers/AC4/mutants/AC4-a-r18/ and four new
student-error mutants (written to ledgers/AC4/mutants/AC4-a-r19/). A mutant is KILLED when the
twin's stdout differs from the page's <pre class="expected"> block or the twin exits non-zero.
"""
import html, pathlib, re, subprocess, sys

root = pathlib.Path(sys.argv[1]).resolve()
outdir = root / "ledgers/AC4/mutants/AC4-a-r19"
outdir.mkdir(parents=True, exist_ok=True)


def expected(page: str) -> str:
    s = (root / "course/modules/AC/AC4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).rstrip("\n")


NEW = {
    "L01": [
        ("n01_fixed_from_low_month", "fixed = Fraction(high_cost) - variable * high_hours",
         "fixed = Fraction(low_cost) - variable * high_hours"),
        ("n02_slope_divides_by_hours", "variable = Fraction(high_cost - low_cost, high_hours - low_hours)",
         "variable = Fraction(high_cost - low_cost, high_hours)"),
    ],
    "L02": [
        ("n01_leverage_on_revenue", "leverage = Fraction(contribution, planned)",
         "leverage = Fraction(PRICE_CENTS * PLANNED_UNITS, planned)"),
        ("n02_loss_run_end_inclusive", "runs.append((start, units - 1))", "runs.append((start, units))"),
        ("n03_sensitivity_plus_one_unit", "up_one = operating_income(PLANNED_UNITS + PLANNED_UNITS // 100)",
         "up_one = operating_income(PLANNED_UNITS + 1)"),
    ],
}
R18 = {
    "L01": [
        "L01_m01_high_is_lowest_month", "L01_m02_residual_sign_flipped",
        "L01_m03_largest_signed_not_absolute", "L01_m04_nonzero_count_counts_positive_only",
    ],
    "L02": [
        "L02_m01_first_whole_unit_floor", "L02_m02_scan_limit_2000", "L02_m03_step_applied_from_2000",
        "L02_m04_margin_of_safety_single_formula", "L02_m05_zero_margin_accepted",
        "L02_m06_planned_income_before_step",
    ],
}
TWIN = {"L01": "lab-AC4-L01-1.py", "L02": "lab-AC4-L02-1.py"}


def run(page: str, label: str, path: pathlib.Path) -> None:
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd="/tmp")
    got = r.stdout.rstrip("\n")
    status = "KILLED" if (got != expected(page) or r.returncode != 0) else "SURVIVED"
    print(f"{page} {label} {status} exit={r.returncode}")


for page in ("L01", "L02"):
    src = (root / "tests/labs/AC4" / TWIN[page]).read_text(encoding="utf-8")
    for name in R18[page]:
        p = outdir / f"{name}.py"
        # round-18 mutants are committed in ledgers/AC4/mutants/AC4-a-r18; re-run them as written
        run(page, "r18:" + name, root / "ledgers/AC4/mutants/AC4-a-r18" / f"{name}.py")
    for name, old, new in NEW[page]:
        assert src.count(old) == 1, (name, src.count(old))
        p = outdir / f"{page}_{name}.py"
        p.write_text(src.replace(old, new, 1), encoding="utf-8")
        run(page, "r19:" + name, p)
