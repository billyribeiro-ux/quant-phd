"""Compare each E3 L01-L04 lab's expected block with its twin's stdout (run from the checkout root, with -I)."""
import difflib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
for t in ("L01", "L02", "L03", "L04"):
    raw = (ROOT / "course/modules/E/E3" / f"{t}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', raw, re.S)
    expected = [line.rstrip() for line in html.unescape(m.group(1)).strip().splitlines()]
    got = [line.rstrip() for line in (HERE / "twins" / f"{t}.out").read_text(encoding="utf-8").strip().splitlines()]
    diff = list(difflib.unified_diff(expected, got, lineterm=""))
    print(t, "IDENTICAL" if not diff else "\n".join(diff))
