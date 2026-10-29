import re, html, subprocess, sys
root = "/tmp/verify18-AC4-a/"
for page, twin in (("L01", "lab-AC4-L01-1.py"), ("L02", "lab-AC4-L02-1.py")):
    s = open(root + "course/modules/AC/AC4/%s.html" % page, encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', s, re.S)
    code = html.unescape(m.group(1))
    t = open(root + "tests/labs/AC4/" + twin, encoding="utf-8").read()
    print(page, "page code identical to twin:", code.rstrip(chr(10)) == t.rstrip(chr(10)), len(code), len(t))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    expected = html.unescape(exp.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", "-c", code], capture_output=True, text=True, cwd="/tmp").stdout
    print(page, "expected block equals run output:", out.rstrip("\n") == expected.rstrip("\n"))
