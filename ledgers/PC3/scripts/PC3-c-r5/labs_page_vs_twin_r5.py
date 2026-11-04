"""Round-5: page code blocks and expected blocks of the three project labs, compared with their twins and with the twins'
own output (python -I -W error, scratch cwd). Writes nothing into the repo. Usage: python3 -I <this> <checkout>."""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/PC/PC3/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-PC3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code).rstrip("\n")
    expected = html.unescape(expected).rstrip("\n")
    twin = (root / f"tests/labs/PC3/{lab_id}.py").read_text(encoding="utf-8").rstrip("\n")
    code_lines, twin_lines = code.split("\n"), twin.split("\n")
    diffs = [(i + 1, a, b) for i, (a, b) in enumerate(zip(code_lines, twin_lines)) if a != b]
    print(f"{lab_id}: page lines {len(code_lines)}, twin lines {len(twin_lines)}, differing lines {len(diffs)}")
    for d in diffs:
        print("   ", d[0], "page:", d[1][:90], "| twin:", d[2][:90])
    with tempfile.TemporaryDirectory(prefix="pc3lab-") as work:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/PC3/{lab_id}.py")],
                           capture_output=True, text=True, cwd=work, env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"})
    out = r.stdout.rstrip("\n")
    print(f"   twin exit {r.returncode}, stderr bytes {len(r.stderr)}; output equals expected block: {out == expected}")
    if out != expected:
        for a, b in zip(out.split("\n"), expected.split("\n")):
            if a != b:
                print("   output:", a, "| expected:", b)
