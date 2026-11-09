"""Round 18 (BK4 slice c): compare each project lab's page code and expected block with its twin, and run each twin
alone under python -I -W error. Usage: python -I lab_page_twin_check.py <checkout-root>"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
for lab_id in ("lab-BK4-project-1", "lab-BK4-project-2", "lab-BK4-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="' + lab_id + r'".*?</section>', page, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (ROOT / f"tests/labs/BK4/{lab_id}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/BK4/{lab_id}.py")],
                       capture_output=True, text=True, check=False)
    out = r.stdout
    print(f"{lab_id}: page code == twin: {same_code}; twin exit {r.returncode}; stderr {r.stderr!r}")
    print(f"  output == expected block: {out.rstrip() == expected.rstrip()}")
    if out.rstrip() != expected.rstrip():
        print("  OUTPUT:\n" + out + "  EXPECTED:\n" + expected)
    if not same_code:
        print("  first differing line:")
        for i, (a, b) in enumerate(zip(code.splitlines(), twin.splitlines())):
            if a != b:
                print(i + 1, repr(a)[:120], "|", repr(b)[:120])
                break
