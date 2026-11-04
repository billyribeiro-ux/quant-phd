"""Check that each slice lab's page code equals its twin, and its expected block equals the twin's stdout.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r4/embed_check.py  (reads out/twin_*.stdout written by the shell step)
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SC1 = ROOT / "course" / "modules" / "SC" / "SC1"
OUT = ROOT / "ledgers" / "SC1" / "scripts" / "SC1-a-r4" / "out"
PAIRS = {"L01": "lab-SC1-L01-1", "L02": "lab-SC1-L02-1", "L03": "lab-SC1-L03-1"}
ok = True
for page, lab in PAIRS.items():
    raw = (SC1 / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', raw, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', raw, re.S).group(1))
    twin = (ROOT / "tests" / "labs" / "SC1" / f"{lab}.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/SC1" / f"{lab}.py")],
                         capture_output=True, text=True, cwd=str(ROOT))
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    exp_eq = expected.rstrip("\n") == run.stdout.rstrip("\n")
    markers = bool(re.search(r"@@(LAB|OUT):", raw))
    ok = ok and code_eq and exp_eq and run.returncode == 0 and not markers and run.stderr == ""
    print(f"{page} {lab}: code==twin {code_eq}; expected==stdout {exp_eq} ({len(run.stdout.splitlines())} lines); "
          f"exit {run.returncode}; stderr {len(run.stderr)} bytes; markers left {markers}")
print("embed_check SC1-a:", "PASS" if ok else "FAIL")
