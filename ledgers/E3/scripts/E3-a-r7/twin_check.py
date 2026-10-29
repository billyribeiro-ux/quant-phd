"""Check that each E3 slice-a lesson page code block equals its lab twin and its expected block equals the twin's stdout (run under python -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L01": "course/modules/E/E3/L01.html", "L02": "course/modules/E/E3/L02.html", "L03": "course/modules/E/E3/L03.html"}
ok_all = True
for lid, page in PAGES.items():
    text = (ROOT / page).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/E3/lab-E3-{lid}-1.py").read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E3/lab-E3-{lid}-1.py")],
                       capture_output=True, text=True, cwd="/tmp")
    exp_eq = expected.strip() == p.stdout.strip()
    print(lid, "codes", len(re.findall(r'data-run>', text)), "code==twin", code_eq, "expected==stdout", exp_eq, "exit", p.returncode, "stderr_len", len(p.stderr))
    ok_all = ok_all and code_eq and exp_eq and p.returncode == 0 and not p.stderr
print("ALL", ok_all)
