"""Verifier r4: page code blocks and expected blocks vs lab twins, and twin outputs under python -I -W error."""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
page = (ROOT / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks", len(blocks), "expected blocks", len(expected))
twins = ["lab-SC1-project-1.py", "lab-SC1-project-2.py", "lab-SC1-project-3.py"]
for i, name in enumerate(twins):
    twin = (ROOT / "tests/labs/SC1" / name).read_text(encoding="utf-8")
    code = html.unescape(blocks[i])
    same = code.strip("\n") == twin.strip("\n")
    print(name, "page code == twin:", same, "| page len", len(code), "twin len", len(twin))
    if not same:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/SC1" / name)],
                         capture_output=True, text=True, cwd="/tmp")
    out = res.stdout
    print("  exit", res.returncode, "stderr", repr(res.stderr[:200]))
    exp = html.unescape(expected[i])
    print("  expected == output:", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        print("  OUTPUT:\n" + out)
        print("  EXPECTED:\n" + exp)
    else:
        print("  OUTPUT:\n" + out)
