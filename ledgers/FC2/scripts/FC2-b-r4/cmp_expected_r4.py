"""Compare each page's <pre class="expected"> block with the output of its lab twin (run with python -I)."""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
pages = {"L04": ("lab-FC2-L04-1",), "L05": ("lab-FC2-L05-1",), "L06": ("lab-FC2-L06-1",)}
for page, (lab,) in pages.items():
    src = open(f"{ROOT}/course/modules/FC/FC2/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/FC2/{lab}.py"],
                         capture_output=True, text=True, check=True).stdout
    print(page, lab, "EXPECTED==OUTPUT:", expected.strip() == out.strip(), "lines", len(out.splitlines()))
    if expected.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm="")))
