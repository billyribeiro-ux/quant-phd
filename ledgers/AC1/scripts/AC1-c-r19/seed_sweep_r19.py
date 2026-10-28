import subprocess, sys, re
from pathlib import Path
root = Path(sys.argv[1])
seeds = list(range(0, 41)) + [999, 123456789, 20260702, 20260701]
for lab in ["L07", "L08"]:
    src = (root / f"tests/labs/AC1/lab-AC1-{lab}-1.py").read_text(encoding="utf-8")
    m = re.search(r"^SEED = (\d+)", src, re.M)
    bad = []
    for s in seeds:
        p = Path(sys.argv[2]) / f"{lab}_{s}.py"
        p.write_text(re.sub(r"^SEED = \d+", f"SEED = {s}", src, count=1, flags=re.M), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(p)], capture_output=True, text=True)
        if r.returncode != 0:
            bad.append(s)
    print(lab, "seed line found:", bool(m), "seeds run:", len(seeds), "failing seeds:", bad)
