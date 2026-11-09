"""Extract the data-run code and the expected block from L07/L08 pages; compare with the twins; run twins alone."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
for lid in ("L07", "L08"):
    page = (ROOT / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    twin = (ROOT / f"tests/labs/M7/lab-M7-{lid}-1.py").read_text(encoding="utf-8")
    (OUT / f"{lid}-page-code.py").write_text(code, encoding="utf-8")
    (OUT / f"{lid}-expected.txt").write_text(expected, encoding="utf-8")
    print(lid, "page_code == twin (exact):", code == twin, " rstrip-equal:", code.rstrip("\n") == twin.rstrip("\n"))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/M7/lab-M7-{lid}-1.py")],
                       capture_output=True, text=True)
    print(lid, "twin exit", r.returncode, "stderr bytes", len(r.stderr.encode()))
    (OUT / f"{lid}-twin.stdout").write_text(r.stdout, encoding="utf-8")
    print(lid, "stdout == expected (rstrip):", r.stdout.rstrip("\n") == expected.rstrip("\n"))
    if r.stdout.rstrip("\n") != expected.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), r.stdout.splitlines(), lineterm="")))
    # page code run standalone
    pr = subprocess.run([sys.executable, "-I", "-W", "error", "-c", code], capture_output=True, text=True, cwd=str(OUT))
    print(lid, "page code run exit", pr.returncode, "stdout == twin stdout:", pr.stdout == r.stdout)
