"""Round 26: compare each lab twin's stdout (python -I -W error) with the page's <pre class="expected"> block."""
import html, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
for lab in ("L01", "L02"):
    page = (root / f"course/modules/AC/AC4/{lab}.html").read_text(encoding="utf-8")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp).rstrip("\n")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{lab}-1.py")],
                         capture_output=True, text=True, timeout=60)
    print(lab, "rc", out.returncode, "stdout == embedded:", out.stdout.rstrip("\n") == exp, "lines", len(exp.splitlines()))
