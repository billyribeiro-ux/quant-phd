# Round 7 verifier script: compare each lab page's expected block (HTML-unescaped) with the twin's stdout.
# Usage: python3 -I expected_vs_twin.py <repo_root>
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ("L01", "L02", "L03"):
    page = (root / "course/modules/SC/SC1" / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1)).rstrip("\n")
    twin_out = (root / "ledgers/SC1/scripts/SC1-a-r7" / f"twin-{lesson}.out").read_text(encoding="utf-8")
    twin_lines = [ln for ln in twin_out.splitlines() if not ln.startswith("exit=")]
    print(lesson, "expected lines:", len(expected.splitlines()), "twin lines:", len(twin_lines),
          "EQUAL" if expected.splitlines() == twin_lines else "DIFFERENT")
    # also verify the code block in the page equals the twin file
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    src = html.unescape(code.group(1))
    twin_src = (root / f"tests/labs/SC1/lab-SC1-{lesson}-1.py").read_text(encoding="utf-8")
    print(lesson, "page code equals twin:", src.rstrip("\n") == twin_src.rstrip("\n"))

# L03 gap computation from the printed standard errors (rows of the expected block).
page = (root / "course/modules/SC/SC1/L03.html").read_text(encoding="utf-8")
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
rows = html.unescape(m.group(1)).splitlines()
import math
H = None
gaps = []
zs = []
for ln in rows:
    if ln.startswith("H = ") and "mean of the sum" in ln:
        H = float(ln.split()[2].rstrip(":"))
    mm = re.match(r"\s+N =\s*(\d+) steps: mean ([\d.]+), se ([\d.]+), z = (-?[\d.]+)", ln)
    if mm and H is not None:
        N, mean, se, z = int(mm.group(1)), float(mm.group(2)), float(mm.group(3)), float(mm.group(4))
        pop = H * math.sqrt(2 / N) / 20
        gaps.append((abs(se / pop - 1), H, N, se, pop))
        zs.append((abs(z), H, N, z))
        # recompute z from printed mean and se
        zc = (mean - H) / se
        if abs(zc - z) > 0.006:
            print("z mismatch", H, N, z, zc)
gaps.sort(reverse=True)
print("largest gap rows:", [(round(g[0] * 100, 2), g[1], g[2]) for g in gaps[:3]])
zs.sort(reverse=True)
print("largest |z| rows:", [(z[0], z[1], z[2], z[3]) for z in zs[:3]])
print("rows checked:", len(gaps))
