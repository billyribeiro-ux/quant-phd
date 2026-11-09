import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
PY = f"{ROOT}/.venv/bin/python"
ok = True
for lab, twin in [("L04", "lab-E4-L04-1.py"), ("L05", "lab-E4-L05-1.py"), ("L06", "lab-E4-L06-1.py")]:
    text = open(f"{ROOT}/course/modules/E/E4/{lab}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1)).rstrip("\n")
    tw = open(f"{ROOT}/tests/labs/E4/{twin}", encoding="utf-8").read().rstrip("\n")
    same = code == tw
    line = text[: m.start()].count("\n") + 1
    end = text[: m.end()].count("\n") + 1
    print(f"{lab}: page code lines {line}-{end} equal twin (newline-normalised): {same} (page len {len(code)}, twin len {len(tw)})")
    ok &= same
    e = re.search(r'<pre class="expected" data-tolerance="1e-6">(.*?)</pre>', text, re.S)
    eline = text[: e.start()].count("\n") + 1
    eend = text[: e.end()].count("\n") + 1
    out = subprocess.run([PY, "-I", "-W", "error", f"{ROOT}/tests/labs/E4/{twin}"], capture_output=True, text=True, cwd="/tmp")
    expected = html.unescape(e.group(1)).rstrip("\n")
    eq = expected == out.stdout.rstrip("\n")
    print(f"{lab}: expected block lines {eline}-{eend} equals twin output: {eq} (exit {out.returncode}, stderr {out.stderr[:200]!r})")
    ok &= eq and out.returncode == 0
print("ALL OK" if ok else "MISMATCH")
