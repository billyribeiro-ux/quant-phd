import html
import re
import sys

ROOT = sys.argv[1]
for lab in ("L03", "L04", "L05"):
    page = open(f"{ROOT}/course/modules/CF/CF8/{lab}.html", encoding="utf-8").read()
    twin = open(f"{ROOT}/tests/labs/CF8/lab-CF8-{lab}-1.py", encoding="utf-8").read()
    runs = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_ok = len(runs) == 1 and html.unescape(runs[0]).strip() == twin.strip()
    print(lab, "data-run blocks", len(runs), "code equals twin", code_ok, "twin bytes", len(twin))
    if exp:
        out = open(sys.argv[2 + ["L03", "L04", "L05"].index(lab)], encoding="utf-8").read()
        print(lab, "expected blocks", len(exp), "expected equals fresh -I -W error stdout", html.unescape(exp[0]).strip() == out.strip())
