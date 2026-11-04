"""Run the L04 twin against corrupted copies of fx_monthly.csv (LX1 slice b, round 1). Each must fail loud."""
import csv, subprocess, sys, shutil, os, tempfile
src, twin = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(src, encoding="utf-8", newline="")))
hdr = rows[0]; gi = hdr.index("GBP")
def case(name, mutate):
    d = tempfile.mkdtemp(prefix="lx1b-guard-")  # fresh empty scratch dir
    os.makedirs(os.path.join(d, "data"))
    r = [list(x) for x in rows]
    mutate(r)
    with open(os.path.join(d, "data", "fx_monthly.csv"), "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(r)
    p = subprocess.run([sys.executable, "-I", "-W", "error", twin], cwd=d, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"})
    last = (p.stderr.strip().splitlines() or [""])[-1]
    print(f"{name}: exit {p.returncode}; last stderr line: {last}")
case("blank GBP cell at row 300", lambda r: r[300].__setitem__(gi, ""))
case("non-decimal GBP cell 'NA' at row 500", lambda r: r[500].__setitem__(gi, "NA"))
case("missing GBP column", lambda r: r[0].__setitem__(gi, "GBX"))
case("skipped month (row 200 removed)", lambda r: r.pop(200))
case("EUR blank at row 10 (not read by lab)", lambda r: r[10].__setitem__(hdr.index("EUR"), ""))
