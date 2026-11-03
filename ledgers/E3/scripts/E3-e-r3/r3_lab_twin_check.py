"""Round 3 verifier check: page code == twin file, twin runs under python -I -W error, output == expected block."""
import html, re, subprocess, sys
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-E3-e")
PY = str(ROOT / ".venv/bin/python")
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-E3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code_html, expected_html in labs:
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin = (ROOT / f"tests/labs/E3/{lab_id.replace('lab-E3-project-', 'lab-E3-project-')}.py").read_text(encoding="utf-8")
    print(lab_id, "page code == twin:", code.strip() == twin.strip())
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
    r = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/E3/{lab_id}.py")], capture_output=True, text=True)
    print(lab_id, "twin exit:", r.returncode, "stderr:", repr(r.stderr[:300]))
    out = r.stdout.strip()
    print(lab_id, "output == expected:", out == expected.strip())
    if out != expected.strip():
        print("OUT:\n" + out + "\nEXP:\n" + expected.strip())
