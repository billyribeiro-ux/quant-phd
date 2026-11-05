"""Round 8: run each project lab twin alone under python -I -W error, compare with the page's code and expected block."""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
PAGE = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
ok = True
for lab in ("lab-BK4-project-1", "lab-BK4-project-2", "lab-BK4-project-3"):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, PAGE, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (ROOT / f"tests/labs/BK4/{lab}.py").read_text(encoding="utf-8")
    same_code = code.strip("\n") == twin.strip("\n")
    with tempfile.TemporaryDirectory(prefix="bk4lab8_") as d:
        proc = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/BK4/{lab}.py")], cwd=d,
                              capture_output=True, text=True, check=False)
    out = proc.stdout
    same_out = out.strip() == expected.strip()
    print(f"{lab}: exit {proc.returncode} | stderr {len(proc.stderr)} bytes | page code == twin: {same_code} | expected == output: {same_out}")
    if not same_out:
        print("--- output\n" + out + "--- expected\n" + expected)
    ok = ok and proc.returncode == 0 and same_code and same_out and not proc.stderr
print("ALL OK" if ok else "MISMATCH")
