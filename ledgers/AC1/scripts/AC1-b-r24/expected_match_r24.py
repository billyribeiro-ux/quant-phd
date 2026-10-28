# Compares each lab twin's stdout (python -I -W error) with the pre.expected block of its page. Run from the checkout root.
import html
import re
import subprocess
import sys

PAGES = {"L04": "course/modules/AC/AC1/L04.html", "L05": "course/modules/AC/AC1/L05.html", "L06": "course/modules/AC/AC1/L06.html"}
for lesson, page in PAGES.items():
    twin = f"tests/labs/AC1/lab-AC1-{lesson}-1.py"
    out = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True, check=True).stdout
    html_text = open(page, encoding="utf-8").read()
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, re.S)
    got = [html.unescape(b).strip() == out.strip() for b in blocks]
    print(lesson, "expected blocks", len(blocks), "match", got, "stdout lines", len(out.splitlines()))
