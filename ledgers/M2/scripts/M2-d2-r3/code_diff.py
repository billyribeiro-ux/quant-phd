import html, re, difflib
from pathlib import Path
ROOT = Path.cwd()
for page, twin in [("L22", "lab-M2-L22-1.py"), ("L23", "lab-M2-L23-1.py"), ("L24", "lab-M2-L24-1.py")]:
    text = (ROOT / "course/modules/M/M2" / f"{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1))
    src = (ROOT / "tests/labs/M2" / twin).read_text(encoding="utf-8")
    print(page, "page ends with newline:", code.endswith("\n"), "twin ends with newline:", src.endswith("\n"))
    diff = list(difflib.unified_diff(src.splitlines(), code.splitlines(), lineterm=""))
    print(page, "line-level diff lines:", len(diff), "| identical after rstrip of trailing newline:", code.rstrip("\n") == src.rstrip("\n"))
    for l in diff[:20]: print("  ", l)
