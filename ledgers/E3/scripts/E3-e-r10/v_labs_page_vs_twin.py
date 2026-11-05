"""Verifier r10: compare each project lab's embedded code and expected block on project.html with the twin file."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-e")
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab_id = f"lab-E3-project-{n}"
    sec = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', page, re.S)
    assert sec, lab_id
    body = sec.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / f"tests/labs/E3/{lab_id}.py").read_text(encoding="utf-8")
    print(lab_id, "code==twin:", code.strip() == twin.strip(), "code len", len(code), "twin len", len(twin))
    if code.strip() != twin.strip():
        import difflib
        for line in difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E3/{lab_id}.py")],
                         capture_output=True, text=True, cwd="/tmp/e3e_r10")
    print("  exit", out.returncode, "stderr:", repr(out.stderr[:200]))
    print("  output==expected:", out.stdout.strip() == expected.strip())
    if out.stdout.strip() != expected.strip():
        print("  OUT:\n" + out.stdout)
        print("  EXP:\n" + expected)
