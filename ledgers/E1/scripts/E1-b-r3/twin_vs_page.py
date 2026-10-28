"""Compare each lab twin with the code block embedded in its page (round 3, slice E1-b)."""
import html, re, sys
root = sys.argv[1]
for L in ("L04", "L05", "L06"):
    page = open(f"{root}/course/modules/E/E1/{L}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/E1/lab-E1-{L}-1.py", encoding="utf-8").read()
    print(L, "identical" if code.strip() == twin.strip() else "DIFFERENT", len(code), len(twin))
