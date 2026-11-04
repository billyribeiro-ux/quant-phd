"""Round-3 PC3 slice a: text scans of index.html, L01-L03 (prose only; lab code blocks and expected blocks removed).
Writes nothing; prints (1) scope words with their sentence, (2) dfn terms and their first line, (3) why-it-matters
word counts, (4) process words and banned phrases. Run as: .venv/bin/python -I <this file> <checkout-root>
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pages = ["index", "L01", "L02", "L03"]
scope = re.compile(r"\b(every|all|only|always|never|any|same|exactly|cannot)\b", re.I)
banned = re.compile(
    r"(it is important to note|studies show|experts agree|it is well known|obviously|clearly|for brevity|"
    r"details omitted|beyond the scope|left as an exercise|you can add more|\bTODO\b|\bTBD\b|lorem|build(er)?s?\b|"
    r"\bround\b|verifier|REQUESTS|unit report)",
    re.I,
)
for p in pages:
    raw = (root / "course/modules/PC/PC3" / f"{p}.html").read_text(encoding="utf-8")
    text = re.sub(r'<section class="lab".*?</section>', "", raw, flags=re.S)
    text = re.sub(r'<pre class="expected".*?</pre>', "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    text = re.sub(r'<input[^>]*>|step="any"', "", text)
    text = re.sub(r"<pre><code.*?</code></pre>", "", text, flags=re.S)
    plain = html.unescape(re.sub(r"<[^>]+>", " ", text))
    plain = re.sub(r"\\\((.*?)\\\)", r" \1 ", plain, flags=re.S)
    print(f"== {p}: scope words")
    for sent in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", plain)):
        for m in scope.finditer(sent):
            print(f"  {m.group(0)} :: {sent.strip()[:200]}")
    print(f"== {p}: banned or process words")
    for m in banned.finditer(plain):
        print("  HIT", m.group(0))
    dfns = re.findall(r"<dfn([^>]*)>([^<]*)", raw)
    print(f"== {p}: dfn count {len(dfns)}")
    for attrs, term in dfns:
        print(f"  dfn{attrs.strip()} :: {term}")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    if m is None:
        print(f"== {p}: no why-it-matters paragraph")
        continue
    body = re.sub(r"\\\((.*?)\\\)", " X ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1))), flags=re.S)
    print(f"== {p}: why-it-matters words {len(body.split())} (limit 120)")
