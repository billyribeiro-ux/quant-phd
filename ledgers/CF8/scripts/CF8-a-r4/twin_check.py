"""Compare each CF8 lab block in L01/L02 with its twin and its expected output (run under python -I -W error)."""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
pages = {"L01": "lab-CF8-L01-1", "L02": "lab-CF8-L02-1"}
for page, lab in pages.items():
    text = (ROOT / f"course/modules/CF/CF8/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/CF8/{lab}.py").read_text(encoding="utf-8")
    print(page, "page code == twin:", code.strip() == twin.strip(), "len", len(code), len(twin))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1)).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", "-c", twin], capture_output=True, text=True, cwd="/tmp")
    print(page, "twin exit", out.returncode, "stderr:", out.stderr.strip()[:200])
    got = out.stdout.strip()
    print(page, "expected == output:", expected == got)
    if expected != got:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), got.splitlines(), lineterm="")))
