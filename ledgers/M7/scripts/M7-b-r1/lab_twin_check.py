"""Verifier script (M7-b round 1): page code equals twin, expected block equals twin output, twin runs under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lab in ["L04", "L05", "L06"]:
    page = (ROOT / f"course/modules/M/M7/{lab}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/M7/lab-M7-{lab}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    m_code = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    code = html.unescape(m_code.group(1)) if m_code else None
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m_exp.group(1)) if m_exp else None
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp/m7b_r1")
    out = run.stdout
    print(f"== {lab}: twin exit={run.returncode} stderr_len={len(run.stderr)}")
    print(f"   page code == twin: {code == twin} (page len {len(code or '')}, twin len {len(twin)})")
    print(f"   expected == twin output: {expected == out} (expected len {len(expected or '')}, out len {len(out)})")
    if expected != out:
        import difflib
        for line in difflib.unified_diff((expected or "").splitlines(), out.splitlines(), "page", "twin", lineterm=""):
            print("   " + line)
    print(f"   run labs ids in page: {re.findall(r'<section class=\"lab[^\"]*\" id=\"([^\"]+)\"', page)}")
    print(f"   data-run count: {page.count('data-run')}, class=lab count: {page.count('class=\"lab')}")

print("--- rstrip comparison (trailing newline only) ---")
for lab in ["L04", "L05", "L06"]:
    page = (ROOT / f"course/modules/M/M7/{lab}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/M7/lab-M7-{lab}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp/m7b_r1")
    print(lab, "code==twin (rstrip):", code.rstrip("\n") == twin.rstrip("\n"), "| expected==out (rstrip):", expected.rstrip("\n") == run.stdout.rstrip("\n"), "| twin ends with newline:", twin.endswith("\n"), "| page code ends newline:", code.endswith("\n"))
    for m in re.finditer(r'data-run', page):
        print("   context:", page[max(0, m.start() - 120): m.start() + 30].replace("\n", " ")[:160])
