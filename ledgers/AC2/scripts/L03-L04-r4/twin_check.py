"""Round-4 check: each page's data-run code equals its lab twin; the page's expected block equals the twin's stdout."""
import html, re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])
for page, twin in (("L03", "lab-AC2-L03-1.py"), ("L04", "lab-AC2-L04-1.py")):
    text = (root / "course/modules/AC/AC2" / f"{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    src = (root / "tests/labs/AC2" / twin).read_text(encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/AC2" / twin)],
                         capture_output=True, text=True, check=True).stdout
    print(f"{page}: code_equals_twin={code.rstrip(chr(10)) == src.rstrip(chr(10))} "
          f"expected_equals_twin_stdout={expected.rstrip(chr(10)) == out.rstrip(chr(10))} expected_lines={expected.count(chr(10)) + 1}")
