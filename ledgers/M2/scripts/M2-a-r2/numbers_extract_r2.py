"""Round-2 inventory of numeric tokens in the visible prose of the slice pages (index, L01-L06), with the
prose context. Lab code blocks and expected-output blocks are excluded (they are checked by run_labs).
Run from the checkout root with -I; output is a dump for the numbers rows, re-derived by recompute_r2.py.
"""

from __future__ import annotations

import html
import re

PAGES = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html"]
ROOT = "course/modules/M/M2/"
for name in PAGES:
    t = open(ROOT + name, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<pre[^>]*>.*?</pre>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    s = html.unescape(re.sub(r"\s+", " ", t))
    print(f"== {name}")
    for m in re.finditer(r"(?<![A-Za-z_.])(\d+(?:\.\d+)?|\d+/\d+|10\^\{?-?\d+\}?)(?![A-Za-z])", s):
        tok = m.group(1)
        if tok in {"0", "1", "2"}:
            continue
        print(f"  {tok!r:12} ...{s[max(0, m.start() - 50):m.end() + 30]}...")
