"""Compare each lab code block on pages L08-L10 with its twin file and the expected output with a real run (verifier, round 1).

Run from the checkout root with the checkout's interpreter: .venv/bin/python -I ledgers/M4/scripts/M4-c-r1/embed_diff.py
"""
import html
import re
import subprocess
import sys

ok = True
for lesson in ("L08", "L09", "L10"):
    src = open(f"course/modules/M/M4/{lesson}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python"[^>]*>(.*?)</code></pre>', src, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    twin = open(f"tests/labs/M4/lab-M4-{lesson}-1.py", encoding="utf-8").read()
    same_code = code.strip() == twin.strip()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(re.sub(r"<[^>]+>", "", exp.group(1))).strip()
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", f"tests/labs/M4/lab-M4-{lesson}-1.py"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    same_out = run == expected
    print(f"{lesson}: page code == twin: {same_code}; expected output == real run: {same_out}; lines={len(run.splitlines())}")
    ok = ok and same_code and same_out
print("ALL EMBEDDED CODE AND OUTPUT MATCH" if ok else "MISMATCH")
