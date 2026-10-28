# Usage: python -I twin_compare.py <checkout> <page> <twin-file-in-tests/labs/AC1>
# Runs the twin under -W error and checks its stdout equals the page's expected block for that lab (HTML-unescaped).
import html, re, subprocess, sys
from pathlib import Path
chk, page, twin = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
out = subprocess.run([sys.executable, "-I", "-W", "error", str(chk / "tests/labs/AC1" / twin)],
                     capture_output=True, text=True, check=False, cwd="/tmp")
text = (chk / "course/modules/AC/AC1" / page).read_text(encoding="utf-8")
lab = twin.removesuffix(".py")
blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, flags=re.S)
hit = [html.unescape(b) for b in blocks if html.unescape(b).strip() == out.stdout.strip()]
print(f"{twin} exit {out.returncode} lines {len(out.stdout.splitlines())} matching expected blocks in {page}: {len(hit)}")
