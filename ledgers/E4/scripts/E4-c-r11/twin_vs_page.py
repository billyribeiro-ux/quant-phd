"""Compare each E4 slice-c lab page with its twin: code byte-equality and expected block vs twin stdout."""
import html
import re
import sys

ROOT = sys.argv[1]
OUT = sys.argv[2]
PAIRS = [("L07", "lab-E4-L07-1"), ("L08", "lab-E4-L08-1"), ("L09", "lab-E4-L09-1")]
lines = []
for page, lab in PAIRS:
    src = open(f"{ROOT}/course/modules/E/E4/{page}.html", encoding="utf-8").read()
    twin = open(f"{ROOT}/tests/labs/E4/{lab}.py", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(e.group(1)).rstrip("\n")
    twin_out = open(f"{ROOT}/{OUT}/twin_{lab[len('lab-E4-'):]}.out", encoding="utf-8").read().rstrip("\n")
    same_out = expected == twin_out
    lines.append(f"{lab}: page code == twin: {same_code} ({len(code)} vs {len(twin)} chars); expected == twin stdout: {same_out} ({len(expected.splitlines())} lines)")
    if not same_out:
        for a, b in zip(expected.splitlines(), twin_out.splitlines()):
            if a != b:
                lines.append(f"  DIFF page: {a!r}\n  DIFF twin: {b!r}")
        lines.append(f"  line counts page={len(expected.splitlines())} twin={len(twin_out.splitlines())}")
print("\n".join(lines))
