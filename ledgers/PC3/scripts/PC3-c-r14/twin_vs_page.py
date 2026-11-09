"""Compare each project lab's page code (data-run pre block) with its twin, and its expected block with a fresh run."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/PC/PC3/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-PC3-project-{n}".*?</section>', page, re.S).group(0)
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/PC3/lab-PC3-project-{n}.py").read_text(encoding="utf-8")
    print(f"lab {n}: page code {len(code)} chars, twin {len(twin)} chars, identical={code == twin}")
    if code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    # run the twin alone under python -I -W error from a scratch directory
    scratch = Path(f"/tmp/pc3c-r14-lab{n}")
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / "lab.py").write_text(twin, encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(scratch / "lab.py")], capture_output=True, text=True, cwd=str(scratch))
    print(f"   twin run exit {run.returncode}, stderr bytes {len(run.stderr)}")
    out_block = re.search(r'<pre><code class="language-python" data-run>.*?</code></pre>\s*<pre>(.*?)</pre>', sec, re.S)
    if out_block is None:
        out_block = re.search(r'</code></pre>\s*<pre[^>]*>(.*?)</pre>', sec, re.S)
    expected = html.unescape(out_block.group(1)) if out_block else None
    print(f"   expected block present: {expected is not None}; expected == twin stdout: {expected is not None and expected.strip() == run.stdout.strip()}")
