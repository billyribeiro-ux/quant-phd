"""For each L05-L08 page: compare the lab code block with the twin source, and the expected block with the twin output.

Run: python -I ledgers/E3/scripts/E3-g-r3/page_vs_twin.py  (from the checkout root)
"""
import html
import re
import subprocess
import sys

ROOT = "."
for L in ("L05", "L06", "L07", "L08"):
    page = open(f"{ROOT}/course/modules/E/E3/{L}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin_path = f"{ROOT}/tests/labs/E3/lab-E3-{L}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    out = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True, check=True).stdout
    page_code = html.unescape(code.group(1)) if code else None
    page_out = html.unescape(expected.group(1)) if expected else None
    print(L, "code blocks:", len(re.findall(r'data-run', page)), "expected blocks:", len(re.findall(r'class="expected"', page)))
    print(L, "page code == twin source:", page_code is not None and page_code.strip() == twin.strip())
    print(L, "page expected == twin stdout:", page_out is not None and page_out.strip() == out.strip())
    if page_out is not None and page_out.strip() != out.strip():
        a = page_out.strip().splitlines()
        b = out.strip().splitlines()
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print("  first diff line", i, repr(x), repr(y))
                break
        print("  line counts", len(a), len(b))
