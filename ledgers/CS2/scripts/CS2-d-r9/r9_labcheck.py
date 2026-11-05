"""Round-9 lab check for project.html labs 1-3: page code vs twin, expected block vs twin output, and
the twin run under python -I -W error (outputs in ledgers/CS2/scripts/CS2-d-r9/twins)."""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
TWIN_DIR = ROOT / "tests/labs/CS2"
OUT_DIR = ROOT / "ledgers/CS2/scripts/CS2-d-r9/twins"
labs = {}
for m in re.finditer(r'<section class="lab[^"]*" id="(lab-CS2-project-\d)"[^>]*>(.*?)</section>', page, flags=re.S):
    lid, body = m.group(1), m.group(2)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, flags=re.S).group(1)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, flags=re.S).group(1)
    labs[lid] = (html.unescape(code), html.unescape(exp))
for lid, (code, exp) in labs.items():
    twin = (TWIN_DIR / f"{lid.replace('lab-', 'lab-')}.py").read_text(encoding="utf-8")
    out_file = OUT_DIR / f"{lid}.out"
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(TWIN_DIR / f"{lid}.py")],
                          capture_output=True, text=True)
    print(f"== {lid}: twin exit {proc.returncode}, stderr {proc.stderr!r}")
    out_file.write_text(proc.stdout, encoding="utf-8")
    code_n = code.rstrip("\n")
    twin_n = twin.rstrip("\n")
    diff = [d for d in difflib.unified_diff(twin_n.splitlines(), code_n.splitlines(), lineterm="", n=0)
            if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))]
    print("  page code vs twin differing lines:", len(diff))
    for d in diff[:12]:
        print("   ", d)
    print("  page code == twin (after trailing newline):", code_n == twin_n)
    exp_n = exp.rstrip()
    out_n = proc.stdout.rstrip()
    print("  expected block == twin output (whitespace-stripped lines):",
          [l.rstrip() for l in exp_n.splitlines()] == [l.rstrip() for l in out_n.splitlines()])
