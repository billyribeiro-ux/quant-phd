"""Round-20 independent check of the three E4 project labs: page code == twin, twin output == page expected block.

Usage: python3 -I labs_twin_check_r20.py <checkout-root>. Runs each twin with python -I -W error in a scratch dir.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
for lab_id in ("lab-E4-project-1", "lab-E4-project-2", "lab-E4-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab_id, page, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python"[^>]*>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / "tests/labs/E4" / f"lab-E4-project-{lab_id[-1]}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/E4" / f"lab-E4-project-{lab_id[-1]}.py")],
                           cwd=d, capture_output=True, text=True, timeout=120)
    out_ok = r.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab_id}: page code==twin {same_code}; twin rc {r.returncode}; stderr bytes {len(r.stderr)}; output==expected {out_ok}")
    if not out_ok:
        print("  got:", r.stdout[:800]); print("  expected:", expected[:800])
