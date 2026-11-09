"""Compare each lab's page code and expected block with its twin and with the twin's actual CPython output (CS2-c r3)."""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
for lab in ("L09", "L10", "L11"):
    page = open(f"{ROOT}/course/modules/CS/CS2/{lab}.html", encoding="utf-8").read()
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(1))
    twin_path = f"{ROOT}/tests/labs/CS2/lab-CS2-{lab}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    print(lab, "code_count", page.count('data-run>'), "expected_count", page.count('class="expected"'))
    print(lab, "page code == twin (rstrip):", code.rstrip() == twin.rstrip(), "len", len(code), len(twin))
    out = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True)
    print(lab, "twin exit", out.returncode, "stderr", repr(out.stderr))
    print(lab, "expected == twin stdout:", expected.rstrip("\n") == out.stdout.rstrip("\n"))
    if expected.rstrip("\n") != out.stdout.rstrip("\n"):
        print("DIFF expected:", repr(expected[:300]))
        print("DIFF stdout:", repr(out.stdout[:300]))
