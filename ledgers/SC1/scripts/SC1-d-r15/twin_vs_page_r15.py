"""Compare each project lab's page code and expected block with its twin and with a real run (round 15, SC1-d)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
for lab in ("lab-SC1-project-1", "lab-SC1-project-2", "lab-SC1-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S)
    section = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin = (ROOT / f"tests/labs/SC1/{lab}.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/SC1/{lab}.py")],
                         capture_output=True, text=True, cwd="/tmp").stdout
    print(f"{lab}: page_code==twin {code == twin}; expected==run {exp.strip() == run.strip()}; "
          f"page_code_len {len(code)} twin_len {len(twin)}")
    if code != twin:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
            print("   ", line)
    if exp.strip() != run.strip():
        import difflib
        for line in difflib.unified_diff(run.strip().splitlines(), exp.strip().splitlines(), "run", "expected", lineterm="", n=0):
            print("   ", line)
