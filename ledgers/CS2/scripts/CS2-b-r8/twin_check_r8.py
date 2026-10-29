"""Compare each CS2 slice-b lab page block with its twin and with its printed expected block; run the twins isolated."""
import html
import os
import re
import subprocess
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-b"
PY = os.path.join(ROOT, ".venv", "bin", "python")
for lesson in ["L05", "L06", "L07", "L08"]:
    page = open(os.path.join(ROOT, f"course/modules/CS/CS2/{lesson}.html"), encoding="utf-8").read()
    twin = open(os.path.join(ROOT, f"tests/labs/CS2/lab-CS2-{lesson}-1.py"), encoding="utf-8").read()
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(blocks[0]) if blocks else ""
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1)) if m else None
    print(f"{lesson} blocks {len(blocks)} page==twin(rstrip) {code.rstrip() == twin.rstrip()}")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "lab.py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(twin)
        r = subprocess.run([PY, "-I", "-W", "error", p], cwd=d, capture_output=True, text=True, timeout=120)
    out = r.stdout
    print(f"{lesson} exit {r.returncode} stderr_bytes {len(r.stderr)} stdout_lines {out.count(chr(10))}")
    print(f"{lesson} expected==output(rstrip) {expected is not None and expected.rstrip() == out.rstrip()}")
    with open(os.path.join(ROOT, f"ledgers/CS2/scripts/CS2-b-r8/out_{lesson}.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    if expected is not None and expected.rstrip() != out.rstrip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.rstrip().splitlines(), out.rstrip().splitlines(), lineterm="")))
