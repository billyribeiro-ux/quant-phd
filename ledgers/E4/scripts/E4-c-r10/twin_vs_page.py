"""Round 10, slice E4-c: the code inside each lab's data-run block on the page equals its twin, line for line."""
import html
import re
import sys
from pathlib import Path

BASE = Path("/Users/billyribeiro/.fanout/wt/verifyE10-E4-c")
ok = True
for lesson in ("L07", "L08", "L09"):
    src = (BASE / "course/modules/E/E4" / (lesson + ".html")).read_text(encoding="utf-8")
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    twin = (BASE / "tests/labs/E4" / ("lab-E4-" + lesson + "-1.py")).read_text(encoding="utf-8")
    code = html.unescape(blocks[0]) if blocks else None
    same = code is not None and code.rstrip("\n") == twin.rstrip("\n")
    ok = ok and same and len(blocks) == 1
    print(lesson, "data-run blocks", len(blocks), "page code lines", (code or "").count("\n"),
          "twin lines", twin.count("\n"), "identical", same)
    if code is not None and not same:
        a, b = code.rstrip("\n").splitlines(), twin.rstrip("\n").splitlines()
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print("  first diff line", i + 1, "page:", x, "| twin:", y)
                break
sys.exit(0 if ok else 1)
