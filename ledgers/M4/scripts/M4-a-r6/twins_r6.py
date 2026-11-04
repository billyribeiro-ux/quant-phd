"""Round-6 M4 slice a: twin vs page code, twin run under python -I -W error, expected block vs stdout."""
from __future__ import annotations
import difflib, html, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PY = ROOT / ".venv" / "bin" / "python"
PAGES = {"L01": "lab-M4-L01-1", "L02": "lab-M4-L02-1", "L03": "lab-M4-L03-1", "L04": "lab-M4-L04-1"}
ok = True
for page_id, twin_id in PAGES.items():
    page = ROOT / "course/modules/M/M4" / f"{page_id}.html"
    twin = ROOT / "tests/labs/M4" / f"{twin_id}.py"
    text = page.read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    run_marks = len(re.findall(r'data-run', text))
    tw = twin.read_text(encoding="utf-8")
    code_ok = [html.unescape(c).strip("\n") == tw.strip("\n") for c in codes]
    with tempfile.TemporaryDirectory() as scratch:
        r = subprocess.run([str(PY), "-I", "-W", "error", str(twin)], cwd=scratch, capture_output=True, text=True, timeout=120)
    exp_ok = [html.unescape(e).rstrip("\n") == r.stdout.rstrip("\n") for e in exps]
    print(f"{page_id}: code_blocks={len(codes)} code_equals_twin={code_ok} expected_blocks={len(exps)} "
          f"expected_equals_stdout={exp_ok} data-run_count={run_marks} exit={r.returncode} stderr_bytes={len(r.stderr)} "
          f"stdout_lines={len(r.stdout.splitlines())}")
    if not (r.returncode == 0 and not r.stderr and all(code_ok) and all(exp_ok) and codes and exps):
        ok = False
        print(r.stderr); print("--- stdout ---"); print(r.stdout)
        for c in codes:
            print("".join(difflib.unified_diff(tw.splitlines(True), html.unescape(c).splitlines(True), "twin", "page")))
    print("STDOUT:\n" + r.stdout)
print("twins PASS" if ok else "twins FAIL")
