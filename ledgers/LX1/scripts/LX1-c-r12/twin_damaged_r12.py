"""Runs the committed lab-LX1-project-3 twin on damaged copies of the snapshot (blank GBP cell, non-decimal GBP cell, removed month,
blank EUR cell as a control). Each run must exit nonzero with ValueError naming the cell or month; the EUR control must run and print."""
import pathlib, shutil, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1]).resolve()
PY = str(root / ".venv/bin/python")
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"
snap = (root / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8").splitlines()
head = snap[0].split(",")
gi, ei = head.index("GBP"), head.index("EUR")
def edit(month, col, value):
    out = []
    for line in snap:
        f = line.split(",")
        if f[0] == month:
            f[col] = value
        out.append(",".join(f))
    return "\n".join(out) + "\n"
cases = {
    "blank_gbp_2000_06": edit("2000-06", gi, ""),
    "nondecimal_gbp_2000_06": edit("2000-06", gi, "n/a"),
    "removed_month_1990_06": "\n".join(l for l in snap if not l.startswith("1990-06,")) + "\n",
    "control_blank_eur_2000_06 (should run)": edit("2000-06", ei, ""),
}
for name, text in cases.items():
    wd = tempfile.mkdtemp(prefix="r12dmg-")
    try:
        (pathlib.Path(wd) / "data").mkdir()
        (pathlib.Path(wd) / "data" / "fx_monthly.csv").write_text(text, encoding="utf-8", newline="")
        p = subprocess.run([PY, "-I", "-W", "error", str(twin)], cwd=wd, capture_output=True, text=True)
        last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
        print(f"{name}: rc={p.returncode} stdout_lines={len(p.stdout.splitlines())} last_stderr_line={last!r}")
    finally:
        shutil.rmtree(wd)
