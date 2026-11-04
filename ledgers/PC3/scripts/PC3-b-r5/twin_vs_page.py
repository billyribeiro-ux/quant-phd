import html, re, subprocess, sys, tempfile, os
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE5-PC3-b")
for lid in ["L04", "L05", "L06"]:
    page = (ROOT / f"course/modules/PC/PC3/{lid}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/PC3/lab-PC3-{lid}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    tw_norm = twin.rstrip("\n")
    code_norm = code.rstrip("\n")
    print(lid, "page code == twin:", code_norm == tw_norm, "len", len(code_norm), len(tw_norm))
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/PC3/lab-PC3-{lid}-1.py")],
                           cwd=d, capture_output=True, text=True)
    print(lid, "exit", r.returncode, "stderr bytes", len(r.stderr.encode()))
    out = r.stdout.rstrip("\n")
    print(lid, "expected == stdout:", expected.rstrip("\n") == out)
    Path(f"/Users/billyribeiro/.fanout/wt/verifyE5-PC3-b/ledgers/PC3/scripts/PC3-b-r5/stdout_{lid}.out").write_text(r.stdout)
