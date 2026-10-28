"""Round 20 lab-twin mutation run for AC4-a. Re-runs the r18 and r19 committed mutants and writes 3 new ones
into ledgers/AC4/mutants/AC4-a-r20/. KILLED = stdout differs from the page's expected block or exit != 0."""
import html, pathlib, re, subprocess, sys

root = pathlib.Path(sys.argv[1]).resolve()
outdir = root / "ledgers/AC4/mutants/AC4-a-r20"
outdir.mkdir(parents=True, exist_ok=True)


def expected(page: str) -> str:
    s = (root / "course/modules/AC/AC4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).rstrip("\n")


NEW = {
    "L01": [
        ("n03_count_threshold_5000", 'sum(1 for r in residuals if r != 0)', 'sum(1 for r in residuals if abs(r) > 5000)'),
    ],
    "L02": [
        ("n04_margin_share_over_contribution", "float(safety / PLANNED_UNITS * 100)", "float(safety / planned * 100)"),
        ("n05_growth_base_is_up_one", "Fraction(up_one - planned, planned) * 100", "Fraction(up_one - planned, up_one) * 100"),
    ],
}
R = {
    "L01": ["L01_m01_high_is_lowest_month", "L01_m02_residual_sign_flipped",
            "L01_m03_largest_signed_not_absolute", "L01_m04_nonzero_count_counts_positive_only"],
    "L02": ["L02_m01_first_whole_unit_floor", "L02_m02_scan_limit_2000", "L02_m03_step_applied_from_2000",
            "L02_m04_margin_of_safety_single_formula", "L02_m05_zero_margin_accepted",
            "L02_m06_planned_income_before_step"],
}
R19 = {
    "L01": ["L01_n01_fixed_from_low_month", "L01_n02_slope_divides_by_hours"],
    "L02": ["L02_n01_leverage_on_revenue", "L02_n02_loss_run_end_inclusive", "L02_n03_sensitivity_plus_one_unit"],
}
TWIN = {"L01": "lab-AC4-L01-1.py", "L02": "lab-AC4-L02-1.py"}


def run(page: str, label: str, path: pathlib.Path) -> None:
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd="/tmp")
    got = r.stdout.rstrip("\n")
    status = "KILLED" if (got != expected(page) or r.returncode != 0) else "SURVIVED"
    print(f"{page} {label} {status} exit={r.returncode}")


for page in ("L01", "L02"):
    src = (root / "tests/labs/AC4" / TWIN[page]).read_text(encoding="utf-8")
    for name in R[page]:
        run(page, "r18:" + name, root / "ledgers/AC4/mutants/AC4-a-r18" / f"{name}.py")
    for name in R19[page]:
        run(page, "r19:" + name, root / "ledgers/AC4/mutants/AC4-a-r19" / f"{name}.py")
    for name, old, new in NEW[page]:
        assert src.count(old) == 1, (name, src.count(old))
        p = outdir / f"{page}_{name}.py"
        p.write_text(src.replace(old, new, 1), encoding="utf-8")
        run(page, "r20:" + name, p)
