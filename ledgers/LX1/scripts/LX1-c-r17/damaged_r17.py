"""Round-15 verifier: differential test of lab-3 candidates against the twin on damaged snapshots.

Usage: python -I damaged_r16.py <checkout_root> <candidate.py>...
Each damaged copy of fx_monthly.csv is written into a scratch directory under data/. The twin
(tests/labs/LX1/lab-LX1-project-3.py) and each candidate run under python -I -W error on the same copy.
A candidate is KILLED when its (exit code, stdout, last stderr line) differs from the twin's on any copy.
"""
import csv
import io
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1]).resolve()
CANDS = [pathlib.Path(p).resolve() for p in sys.argv[2:]]
SRC = (ROOT / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8")
rows = list(csv.reader(io.StringIO(SRC)))
HEADER, BODY = rows[0], rows[1:]
IDX = {r[0]: i for i, r in enumerate(BODY)}
COL = HEADER.index("GBP")


def variant(edit):
    body = [list(r) for r in BODY]
    edit(body)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(HEADER)
    w.writerows(body)
    return buf.getvalue()


def set_cell(month, value):
    def f(body):
        body[IDX[month]][COL] = value
    return f


def drop(month):
    def f(body):
        del body[IDX[month]]
    return f


def duplicate(month):
    def f(body):
        body.insert(IDX[month] + 1, list(body[IDX[month]]))
    return f


def drop_first(body):
    del body[0]


DAMAGE = {
    "blank_gbp_2000_06": variant(set_cell("2000-06", "")),
    "nondecimal_gbp_2000_06": variant(set_cell("2000-06", "n/a")),
    "scientific_gbp_2000_06": variant(set_cell("2000-06", "1.2e0")),
    "negative_gbp_2000_06": variant(set_cell("2000-06", "-1.2")),
    "month_gap_2000_06_dropped": variant(drop("2000-06")),
    "month_duplicated_2000_06": variant(duplicate("2000-06")),
    "first_row_dropped": variant(drop_first),
    "blank_gbp_1971_01_first_row": variant(set_cell("1971-01", "")),
    "nondecimal_gbp_1971_01_first_row": variant(set_cell("1971-01", "n/a")),
    "blank_gbp_2026_09_last_row": variant(set_cell("2026-09", "")),
    "control_unchanged_snapshot": SRC,
}


def run(lab_path, csv_text):
    with tempfile.TemporaryDirectory(prefix="lx1c_r16_dmg_") as tmp:
        (pathlib.Path(tmp) / "data").mkdir()
        (pathlib.Path(tmp) / "data" / "fx_monthly.csv").write_text(csv_text, encoding="utf-8")
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(lab_path)], cwd=tmp,
                           capture_output=True, text=True, timeout=120)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    return p.returncode, p.stdout, last


TWIN = ROOT / "tests/labs/LX1/lab-LX1-project-3.py"
twin_results = {name: run(TWIN, text) for name, text in DAMAGE.items()}
for name, (rc, out, last) in twin_results.items():
    print(f"TWIN {name}: rc={rc} last_stderr={last[:90]!r} stdout_lines={len(out.splitlines())}")
for c in CANDS:
    diffs = []
    for name, text in DAMAGE.items():
        got = run(c, text)
        if got != twin_results[name]:
            diffs.append(f"{name}: rc={got[0]} last={got[2][:60]!r}")
    verdict = "KILLED" if diffs else "SURVIVED"
    print(f"{verdict} | {c.name} | {'; '.join(diffs)[:400]}")
