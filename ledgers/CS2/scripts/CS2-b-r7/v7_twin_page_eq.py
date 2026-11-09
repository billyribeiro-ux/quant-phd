"""Round 7 (CS2 slice b): page code block vs twin, and expected block vs twin stdout."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
for n in (5, 6, 7, 8):
    page = open(f"{root}/course/modules/CS/CS2/L0{n}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/CS2/lab-CS2-L0{n}-1.py", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    print(f"L0{n}: code chars {len(code)} twin chars {len(twin)} identical_after_strip={code.strip() == twin.strip()}")
    e_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", e_m.group(1)))
    line_no = page[: e_m.start()].count("\n") + 1
    proc = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/CS2/lab-CS2-L0{n}-1.py"],
                          capture_output=True, text=True, cwd="/tmp")
    out = proc.stdout
    e, o = exp.strip().splitlines(), out.strip().splitlines()
    diffs = [(k, x, y) for k, (x, y) in enumerate(zip(e, o), 1) if x != y]
    print(f"L0{n}: twin exit {proc.returncode} stderr {proc.stderr.strip()[:200]!r}; expected starts line {line_no}, "
          f"exp lines {len(e)}, stdout lines {len(o)}, equal={e == o}, diffs={diffs[:3]}")
