# Round-6: page code block (data-run) and expected block vs twin file and twin stdout, for L01-L03.
import html, re, sys
ROOT = sys.argv[1]
for L in ["L01", "L02", "L03"]:
    page = open(f"{ROOT}/course/modules/FC/FC2/{L}.html", encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{ROOT}/tests/labs/FC2/lab-FC2-{L}-1.py", encoding="utf-8").read()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    out = open(f"{ROOT}/{'ledgers/FC2/scripts/FC2-a-r6'}/r6-twin-{L}.out", encoding="utf-8").read()
    print(L, "code==twin:", code.rstrip("\n") == twin.rstrip("\n"), "| expected==twin stdout:", expected.rstrip("\n") == out.rstrip("\n"), "| lens", len(code), len(twin), len(expected), len(out))
