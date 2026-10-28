"""Re-run the L07 and L08 lab twins with each seed 1..40 substituted and tally the printed counts."""
import re
import subprocess
import sys

root = sys.argv[1]
py = sys.executable
out = {}
for lab, pat in (("L07", r"cases with q <= K and an empty range: (\d+)"),
                 ("L08", r"pairs ranked differently by RI and by OI/C: (\d+) of 28")):
    src = open(f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py", encoding="utf-8").read()
    rows = []
    for seed in range(1, 41):
        s2 = re.sub(r"^SEED = \d+", f"SEED = {seed}", src, count=1, flags=re.M)
        p = subprocess.run([py, "-I", "-c", s2], capture_output=True, text=True, timeout=60)
        txt = p.stdout
        m = re.search(pat, txt)
        extra = ""
        if lab == "L07":
            fits = re.search(r"cases with a feasible range: (\d+)", txt)
            empty = m.group(1) if m else "?"
            rows.append((seed, empty, fits.group(1) if fits else "?"))
        else:
            rows.append((seed, m.group(1) if m else "?", ""))
    out[lab] = rows
for lab, rows in out.items():
    print(lab)
    for r in rows:
        print(" ", *r)
