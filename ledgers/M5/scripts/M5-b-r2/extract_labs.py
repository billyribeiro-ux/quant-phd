import html, re, sys
from pathlib import Path
root = Path("/Users/billyribeiro/.fanout/wt/verifyS2-M5-b")
out = Path("/tmp/m5b-r2/out")
for page, twin in [("L05", "lab-M5-L05-1"), ("L06", "lab-M5-L06-1"), ("L07", "lab-M5-L07-1")]:
    text = (root / f"course/modules/M/M5/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code_s = html.unescape(code.group(1))
    exp_s = html.unescape(exp.group(1))
    twin_s = (root / f"tests/labs/M5/{twin}.py").read_text(encoding="utf-8")
    (out / f"{page}_page_code.py").write_text(code_s, encoding="utf-8")
    (out / f"{page}_expected.txt").write_text(exp_s, encoding="utf-8")
    print(page, "page code == twin:", code_s == twin_s, "| len", len(code_s), len(twin_s))
    print(page, "expected == twin stdout:", exp_s.rstrip("\n") == open(out / f"twin_{twin[len('lab-M5-'):]}.out", encoding="utf-8").read().rstrip("\n"))
