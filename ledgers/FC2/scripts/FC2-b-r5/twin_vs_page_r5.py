"""Compare each L04-L06 page's data-run code block with its lab twin, and expected block with twin output (python -I)."""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
for page in ("L04", "L05", "L06"):
    with open(f"{ROOT}/course/modules/FC/FC2/{page}.html", encoding="utf-8") as fh:
        src = fh.read()
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S).group(1))
    with open(f"{ROOT}/tests/labs/FC2/lab-FC2-{page}-1.py", encoding="utf-8") as fh:
        twin = fh.read()
    print(page, "PAGE_CODE==TWIN:", code.strip() == twin.strip(), "twin_bytes", len(twin))
    if code.strip() != twin.strip():
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:60]))
    with open(f"{ROOT}/tests/labs/FC2/lab-FC2-{page}-1.py", encoding="utf-8") as fh:
        pass
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/FC2/lab-FC2-{page}-1.py"],
                         capture_output=True, text=True, check=True).stdout
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    exp = html.unescape(m.group(1))
    print(page, "EXPECTED==OUTPUT:", exp.strip() == out.strip())
