"""Round-3 PC3 slice a: for each lab on L01-L03, (1) the page's <code data-run> text equals the twin file,
(2) the twin runs alone under python -I -W error in an empty scratch dir with exit 0 and empty stderr,
(3) the page's <pre class="expected"> block equals the twin's stdout. Also saves each twin stdout to outputs/.
Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r3/expected_vs_output.py <checkout-root> <scratch-dir>
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
outdir = root / "ledgers/PC3/scripts/PC3-a-r3/outputs"
py = str(root / ".venv" / "bin" / "python")
for page, lab in (("L01", "lab-PC3-L01-1"), ("L02", "lab-PC3-L02-1"), ("L03", "lab-PC3-L03-1")):
    text = (root / "course/modules/PC/PC3" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="%s".*?</section>' % lab, text, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r"<code[^>]*data-run>(.*?)</code>", sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / "tests/labs/PC3" / f"{lab}.py").read_text(encoding="utf-8")
    print(page, "page code == twin:", code.strip() == twin.strip())
    r = subprocess.run(
        [py, "-I", "-W", "error", str(root / "tests/labs/PC3" / f"{lab}.py")],
        cwd=scratch,
        capture_output=True,
        text=True,
    )
    print(page, "twin exit", r.returncode, "stderr bytes", len(r.stderr), "stdout lines", len(r.stdout.splitlines()))
    print(page, "expected block == stdout:", expected.strip() == r.stdout.strip())
    (outdir / f"twin-{page}.out").write_text(r.stdout, encoding="utf-8")
