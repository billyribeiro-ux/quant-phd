"""Round-1 FC1-a scope-word scan: lists every scope word in the prose of L01-L03 (code, expected blocks and math
removed) so that each universal or scope claim can be checked by hand. Run from the checkout root with -I."""

from __future__ import annotations

import html
import pathlib
import re

WORDS = r"\b(every|all|always|never|any|only|exactly|drives|same|across|market structure|clearing and settlement|no other|none|cannot)\b"
for f in ["L01.html", "L02.html", "L03.html"]:
    t = pathlib.Path("course/modules/FC/FC1", f).read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', " ", t, flags=re.S)
    t = re.sub(r'<pre class="expected".*?</pre>', " ", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\s+", " ", t)
    for m in re.finditer(WORDS, t, re.I):
        print(f, "|", t[max(0, m.start() - 90):m.end() + 60])
