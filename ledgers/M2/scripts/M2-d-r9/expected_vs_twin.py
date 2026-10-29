"""Compare each slice page's <pre class=expected> block with its twin's stdout, both unescaped."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
for L in ["L19", "L20", "L21", "L22", "L23", "L24"]:
    page = open(f"{root}/course/modules/M/M2/{L}.html", encoding="utf-8").read()
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    twin = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/M2/lab-M2-{L}-1.py"],
                          capture_output=True, text=True, check=True).stdout
    expected = [html.unescape(b) for b in blocks]
    print(L, "expected blocks:", len(blocks), "match_any:", any(e.strip() == twin.strip() for e in expected),
          "twin_lines:", len(twin.splitlines()))
