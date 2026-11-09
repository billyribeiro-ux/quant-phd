"""Round 17: run each E4 project lab twin alone under python -I -W error, and compare the page's data-run code
block with the twin byte for byte; compare the page's expected block with the twin's stdout (text, trailing
whitespace stripped). Usage: twins_and_page_code.py <checkout> <outdir>"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
py = root / ".venv" / "bin" / "python"
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    twin = root / f"tests/labs/E4/lab-E4-project-{n}.py"
    proc = subprocess.run([str(py), "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    (out / f"twin_project_{n}.out").write_text(proc.stdout, encoding="utf-8")
    (out / f"twin_project_{n}.err").write_text(proc.stderr, encoding="utf-8")
    print(f"twin project-{n}: exit {proc.returncode} stderr_bytes {len(proc.stderr.encode())}")
    sec = re.search(rf'<section class="lab[^"]*" id="lab-E4-project-{n}".*?</section>', page, flags=re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, flags=re.S).group(1))
    same_code = code.rstrip("\n") == twin.read_text(encoding="utf-8").rstrip("\n")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, flags=re.S).group(1))
    got = [l.rstrip() for l in proc.stdout.rstrip("\n").splitlines()]
    exp = [l.rstrip() for l in expected.rstrip("\n").splitlines()]
    print(f"  page code == twin: {same_code}; expected block == twin stdout: {got == exp} ({len(exp)} lines)")
    if not same_code:
        import difflib
        print("".join(list(difflib.unified_diff(twin.read_text(encoding='utf-8').splitlines(True), code.splitlines(True), 'twin', 'page'))[:60]))
    if got != exp:
        import difflib
        print("\n".join(list(difflib.unified_diff(exp, got, 'page_expected', 'twin_stdout', lineterm=''))[:60]))
