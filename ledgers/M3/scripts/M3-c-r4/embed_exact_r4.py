"""Round-4 check for slice M3-c: each lab twin's source equals the page's data-run block,
and each page's expected block equals the twin's stdout, line for line (no tag stripping)."""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".").resolve()
py = str(root / ".venv/bin/python")
ok = True
for lab, page in [("L07-1", "L07"), ("L08-1", "L08"), ("L09-1", "L09")]:
    twin = (root / f"tests/labs/M3/lab-M3-{lab}.py").read_text()
    stdout = subprocess.run([py, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lab}.py")],
                            capture_output=True, text=True, check=True).stdout
    src = (root / f"course/modules/M/M3/{page}.html").read_text()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    code_txt = html.unescape(code.group(1))
    exp_txt = html.unescape(exp.group(1))
    same_code = code_txt.strip("\n") == twin.strip("\n")
    same_out = exp_txt.strip("\n") == stdout.strip("\n")
    print(f"{page}: twin source == page code block: {same_code}; expected block == twin stdout: {same_out}; "
          f"stdout lines: {len(stdout.splitlines())}")
    if not (same_code and same_out):
        ok = False
        if not same_code:
            import difflib
            print("".join(list(difflib.unified_diff(twin.splitlines(True), code_txt.splitlines(True), 'twin', 'page'))[:60]))
        if not same_out:
            import difflib
            print("".join(list(difflib.unified_diff(stdout.splitlines(True), exp_txt.splitlines(True), 'run', 'page'))[:60]))
print("ALL EXACT" if ok else "MISMATCH")
