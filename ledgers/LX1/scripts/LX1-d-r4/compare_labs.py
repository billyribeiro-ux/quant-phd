"""Compare each lesson's data-run code with its twin, and its expected block with the twin's output."""
import html
import re
import sys

root = sys.argv[1]
for L in ("L01", "L02", "L03", "L04"):
    src = open(f"{root}/course/modules/LX/LX1/{L}.html", encoding="utf-8").read()
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S).group(1)
    code = html.unescape(re.sub(r"<[^>]+>", "", code))
    twin = open(f"{root}/tests/labs/LX1/lab-LX1-{L}-1.py", encoding="utf-8").read()
    same = code.strip() == twin.strip()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    exp = html.unescape(re.sub(r"<[^>]+>", "", exp)).strip()
    out = open(f"{root}/ledgers/LX1/scripts/LX1-d-r4/out/twin_{L}.out", encoding="utf-8").read().strip()
    norm = lambda s: [re.sub(r"\s+", " ", ln).strip() for ln in s.splitlines() if ln.strip()]
    a, b = norm(exp), norm(out)
    print(L, "code==twin:", same, "expected==output lines:", a == b, len(a), len(b))
    if a != b:
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print("  first diff at", i, "\n   exp:", x[:200], "\n   out:", y[:200])
                break
