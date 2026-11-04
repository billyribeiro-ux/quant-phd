import csv, shutil, subprocess, sys, pathlib
src = pathlib.Path(sys.argv[1]); twin = sys.argv[2]; base = pathlib.Path(sys.argv[3]); py = sys.argv[4]
rows = list(csv.reader(open(src, newline="", encoding="utf-8")))
hdr = rows[0]; gi = hdr.index("GBP")
def variant(name, mutate):
    d = base / name; (d / "data").mkdir(parents=True, exist_ok=True)
    rr = [list(r) for r in rows]
    h = list(hdr)
    mutate(rr, h)
    with open(d / "data" / "fx_monthly.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(h); w.writerows(rr[1:])
    p = subprocess.run([py, "-I", "-W", "error", twin], cwd=d, capture_output=True, text=True)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    print(f"{name}: exit {p.returncode} | stdout lines {len(p.stdout.splitlines())} | {last[:160]}")
def blank(rr, h): rr[100][gi] = ""
def nondec(rr, h): rr[100][gi] = "1.2.3"
def expo(rr, h): rr[100][gi] = "1.5e2"
def neg(rr, h): rr[100][gi] = "-1.5"
def zero(rr, h): rr[100][gi] = "0.0000"
def gap(rr, h): del rr[101]
def rename(rr, h): h[gi] = "GBX"
def control(rr, h): pass
for n, f in [("control", control), ("blank", blank), ("nondecimal", nondec), ("exponent", expo), ("negative", neg), ("zero", zero), ("deleted_month", gap), ("renamed_column", rename)]:
    variant(n, f)
# GBP cell positivity and blank/non-decimal sweep over the real file
import re
bad = [r for r in rows[1:] if not re.fullmatch(r"\d+(\.\d+)?", r[gi]) or float(r[gi]) <= 0]
print("real file GBP cells not positive decimal:", len(bad), "of", len(rows) - 1)
