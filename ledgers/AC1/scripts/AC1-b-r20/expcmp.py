import html, re, subprocess, sys
root = "/tmp/verify20-AC1-b"
for L in ("L04", "L05", "L06"):
    page = open(f"{root}/course/modules/AC/AC1/{L}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*><code>(.*?)</code></pre>', page, re.S) or re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(m.group(1)).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/AC1/lab-AC1-{L}-1.py"], capture_output=True, text=True).stdout.strip()
    print(L, "expected==run", exp == out, len(exp.splitlines()), len(out.splitlines()))
