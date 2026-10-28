import re, subprocess, sys
from pathlib import Path
root = Path("/tmp/verify20-AC1-c"); out = Path("/tmp/AC1-v/AC1-c-r20/new")
cases = {
 "m20a": ("L08", "        tax_dep = cost * TAX_PERCENT[index] // 100\n", "        tax_dep = cost * TAX_PERCENT[(index + 1) % LIFE] // 100\n"),
 "m20c": ("L07", "    index = year - grant.grant_year\n", "    index = year - grant.grant_year - 1\n"),
}
for name, (lab, old, new) in cases.items():
    src = (root / f"tests/labs/AC1/lab-AC1-{lab}-1.py").read_text(encoding="utf-8")
    bad = []
    for s in list(range(0, 41)) + [999, 123456789, 20260702, 20260701]:
        t = re.sub(r"^SEED = \d+", f"SEED = {s}", src, count=1, flags=re.M).replace(old, new)
        p = out / f"{name}_seed{s}.py"; p.write_text(t, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True)
        if r.returncode != 0: bad.append(s)
    print(name, "failing seeds of", 45, ":", len(bad), bad[:12])
