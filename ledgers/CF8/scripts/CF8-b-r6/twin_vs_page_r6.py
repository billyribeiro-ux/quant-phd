"""Compare each embedded lab code and expected output on L03-L05 with its twin and a fresh run of the twin."""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
for lesson in ("L03", "L04", "L05"):
    page = open(f"{ROOT}/course/modules/CF/CF8/{lesson}.html", encoding="utf-8").read()
    twin = open(f"{ROOT}/tests/labs/CF8/lab-CF8-{lesson}-1.py", encoding="utf-8").read()
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    lab_sections = re.findall(r'<section class="lab".*?</section>', page, re.S)
    code_ok = [html.unescape(re.sub(r"<[^>]+>", "", b)).strip() == twin.strip() for b in blocks]
    print(lesson, "pre blocks:", len(blocks), "match twin:", code_ok)
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/CF8/lab-CF8-{lesson}-1.py"],
                         capture_output=True, text=True, cwd="/tmp").stdout
    for s in lab_sections:
        exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
        exp_txt = [html.unescape(re.sub(r"<[^>]+>", "", e)) for e in exp]
        hit = [e.strip() == out.strip() for e in exp_txt]
        print(lesson, "expected blocks:", len(exp_txt), "equal to fresh run:", hit)
