"""Compare each project lab's page code and expected block with its twin (run with python -I)."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
for lab in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    sec = re.search(r'<section[^>]*id="%s".*?</section>' % lab, page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / "tests/labs/E3" / (lab + ".py")).read_text(encoding="utf-8")
    p_lines, t_lines = code.rstrip("\n").split("\n"), twin.rstrip("\n").split("\n")
    diffs = []
    if len(p_lines) != len(t_lines):
        diffs.append(("length", len(p_lines), len(t_lines)))
    for i, (a, b) in enumerate(zip(p_lines, t_lines)):
        if a != b and "___" not in a:
            diffs.append((i + 1, a, b))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/E3" / (lab + ".py"))],
                         capture_output=True, text=True)
    print(lab, "code-diff-lines:", diffs[:5], "| twin exit:", out.returncode, "| stderr:", repr(out.stderr[:200]))
    print("  expected == twin output:", exp.strip() == out.stdout.strip())
    if exp.strip() != out.stdout.strip():
        print("  expected:", exp.strip()[:400]); print("  output:", out.stdout.strip()[:400])
