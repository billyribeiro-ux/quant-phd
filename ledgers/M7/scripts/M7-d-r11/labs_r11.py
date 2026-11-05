"""For M7 project labs: extract each page's data-run code and expected block, compare with its twin and with twin output."""
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PY = str(ROOT / ".venv/bin/python")
page = (ROOT / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-M7-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (ROOT / f"tests/labs/M7/{lab_id.replace('lab-M7-project-', 'lab-M7-project-')}.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    difflines = [] if same else [l for l in __import__('difflib').unified_diff(twin.splitlines(), code.splitlines(), 'twin', 'page', lineterm='')][:20]
    r = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/M7/{lab_id.replace('lab-', 'lab-')}.py")], capture_output=True, text=True)
    out = r.stdout.strip()
    print(lab_id, "page_code==twin:", same, "rc:", r.returncode, "stderr_len:", len(r.stderr))
    print("  diff:", difflines[:20])
    print("  expected==output:", out == expected.strip(), )
    if out != expected.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.splitlines(), 'expected', 'output', lineterm='')))
