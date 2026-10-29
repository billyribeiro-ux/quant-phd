"""Compare the data-run code and expected output embedded in L07/L08 with the lab twins and a fresh run."""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
for page, twin in (("L07", "lab-FC2-L07-1"), ("L08", "lab-FC2-L08-1")):
    text = (root / f"course/modules/FC/FC2/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin_src = (root / f"tests/labs/FC2/{twin}.py").read_text(encoding="utf-8")
    print(page, "embedded code == twin:", code.rstrip("\n") == twin_src.rstrip("\n"), "len", len(code), len(twin_src))
    if code.rstrip("\n") != twin_src.rstrip("\n"):
        import difflib
        print("".join(difflib.unified_diff(twin_src.splitlines(True), code.splitlines(True), "twin", "embedded"))[:3000])
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC2/{twin}.py")],
                         capture_output=True, text=True, check=True).stdout
    print(page, "expected == fresh stdout (exact):", expected.rstrip("\n") == out.rstrip("\n"))
