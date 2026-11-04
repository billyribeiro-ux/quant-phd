"""LX1-a r1: prints the context of every scope word in the slice prose (hub, L01, L02), tags stripped, code and expected blocks removed."""
import html
import re

FILES = ["course/modules/LX/LX1/index.html", "course/modules/LX/LX1/L01.html", "course/modules/LX/LX1/L02.html"]
for f in FILES:
    raw = open(f, encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    body = re.sub(r'<pre class="expected".*?</pre>', " ", body, flags=re.S)
    body = re.sub(r'<pre><code class="language-python".*?</code></pre>', " ", body, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
    print("==", f)
    for m in re.finditer(r"\b(every|all|any|only|same|exactly|never|most|usual|the last|the first)\b", t):
        print(" -", t[max(0, m.start() - 110): m.end() + 70])
