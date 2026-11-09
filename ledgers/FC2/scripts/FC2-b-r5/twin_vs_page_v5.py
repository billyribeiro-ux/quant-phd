# Round-5 check: page code block equals twin file; expected block equals twin stdout (run with -I).
import html, re, subprocess, difflib
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS5-FC2-b"
PY = ROOT + "/.venv/bin/python"
for L in ("L04", "L05", "L06"):
    page = open(f"{ROOT}/course/modules/FC/FC2/{L}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{ROOT}/tests/labs/FC2/lab-FC2-{L}-1.py", encoding="utf-8").read()
    print(L, "page code == twin:", code.strip() == twin.strip(), "len", len(code), len(twin))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([PY, "-I", "-W", "error", f"{ROOT}/tests/labs/FC2/lab-FC2-{L}-1.py"],
                         capture_output=True, text=True, cwd="/tmp").stdout
    print(L, "expected block == twin stdout:", expected.strip() == out.strip(), "lines", len(expected.splitlines()), len(out.splitlines()))
    if expected.strip() != out.strip():
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm="")))
