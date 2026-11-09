"""Compare project.html lab code and expected blocks with tests/labs/CS2 twins; run twins under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-CS2-project-\d)"[^>]*>(.*?)</section>', page, re.S)
for lab_id, body in labs:
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (root / f"tests/labs/CS2/{lab_id}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/CS2/{lab_id}.py")],
                         capture_output=True, text=True, cwd="/tmp")
    out_ok = run.stdout.rstrip("\n") == expected.rstrip("\n")
    blanks = code.count("___")
    print(f"{lab_id}: page_code_eq_twin={same_code} expected_eq_output={out_ok} rc={run.returncode} blanks={blanks} "
          f"twin_lines={twin.count(chr(10))} expected_lines={expected.count(chr(10))}")
    if not same_code:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0):
            print("   ", line)
    if not out_ok or run.returncode:
        print(run.stderr[-800:])
