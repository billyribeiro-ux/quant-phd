"""Lab 1 interpretation check: the bracket width after each halving, and the first halving at which it equals 2^-53.

Run: python3 -I lab1_width_check_r9.py <repo-root>
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
sec = re.search(r'<section[^>]*id="lab-E4-project-1".*?</section>', page, re.S).group(0)
code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1)
code = code.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
ns: dict = {}
# run only the definitions of the twin (not main), then replay the bisection loop with width tracking
src = code.replace("\nmain()", "\n")
exec(compile(src, "lab1", "exec"), ns)
low, high = 0.0, 1.0
first_at_2m53 = None
widths = []
for step in range(1, ns["BISECTION_STEPS"] + 1):
    mid = 0.5 * (low + high)
    if ns["gap"](mid) > 0.0:
        low = mid
    else:
        high = mid
    w = high - low
    widths.append(w)
    if first_at_2m53 is None and w == 2.0 ** -53:
        first_at_2m53 = step
print("widths at halvings 50..56:", [f"{w:.6e}" for w in widths[49:56]])
print("first halving with width exactly 2^-53:", first_at_2m53)
print("widths from that halving to 60 all equal 2^-53:", all(w == 2.0 ** -53 for w in widths[first_at_2m53 - 1:]))
print("width at halving 52:", f"{widths[51]:.6e}", " at 53:", f"{widths[52]:.6e}")
