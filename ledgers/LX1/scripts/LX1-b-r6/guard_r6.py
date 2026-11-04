# Guard cases for load_column: run the twin's load_column on scratch copies of the CSV (the twin is run as a module import via -I).
import subprocess, sys, shutil, os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b"
src = f"{ROOT}/course/assets/data/market/fx_monthly.csv"
lines = open(src, encoding="utf-8").read().split("\n")
hdr = lines[0]
def run(name, mutated):
    d = f"/tmp/lx1b-r6/guard_{name}"
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d + "/data")
    open(d + "/data/fx_monthly.csv", "w", encoding="utf-8").write("\n".join(mutated))
    p = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", f"{ROOT}/tests/labs/LX1/lab-LX1-L04-1.py"], cwd=d, capture_output=True, text=True)
    last = (p.stderr.strip().splitlines() or [""])[-1]
    print(f"{name}: exit {p.returncode}; last stderr line: {last}")
# row index 300 (line 301 incl header) is 1995-12 region; find the GBP index
cols = hdr.split(",")
gi = cols.index("GBP")
def mut(line_no, newval):
    out = list(lines)
    parts = out[line_no].split(",")
    parts[gi] = newval
    out[line_no] = ",".join(parts)
    return out
target = next(i for i, l in enumerate(lines) if l.startswith("1995-12,"))
print("target line", target, lines[target][:60])
run("blank", mut(target, ""))
run("two_dots", mut(target, "1.2.3"))
run("exponent", mut(target, "1.5e2"))
run("negative", mut(target, "-1.5"))
# skipped month: drop 1996-01
skip = [l for l in lines if not l.startswith("1996-01,")]
run("skipped_month", skip)
# renamed column
run("renamed_column", [hdr.replace("GBP", "GBPX")] + lines[1:])
# unchanged file must exit 0
run("unchanged", lines)
