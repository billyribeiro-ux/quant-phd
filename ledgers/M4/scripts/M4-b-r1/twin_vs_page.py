"""Round 1 (delta closing from pin 329c1d7f) slice b: page code == twin, expected block == twin output (run under python -I -W error)."""
import html
import re
import subprocess
import sys

PAGES = {
    "L05": "course/modules/M/M4/L05.html",
    "L06": "course/modules/M/M4/L06.html",
    "L07": "course/modules/M/M4/L07.html",
}
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF21-M4-b/"
for lesson, page in PAGES.items():
    text = open(ROOT + page, encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin_path = ROOT + f"tests/labs/M4/lab-M4-{lesson}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    print(lesson, "page code == twin:", code.strip() == twin.strip(), "| twin bytes", len(twin))
    if code.strip() != twin.strip():
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]))
    proc = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True)
    print(lesson, "twin exit", proc.returncode, "stderr bytes", len(proc.stderr))
    print(lesson, "output == expected block:", proc.stdout.strip() == expected.strip())
    if proc.stdout.strip() != expected.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), proc.stdout.strip().splitlines(), "expected", "output", lineterm="")))
    open(ROOT + f"ledgers/M4/scripts/M4-b-r1/twin_{lesson}.out", "w").write(proc.stdout)
