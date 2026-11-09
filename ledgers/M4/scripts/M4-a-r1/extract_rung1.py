import html, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src[src.index("Rung 1 worked example") - 200:], re.S)
open(sys.argv[2], "w", encoding="utf-8").write(html.unescape(m.group(1)))
print("extracted", len(m.group(1)))
