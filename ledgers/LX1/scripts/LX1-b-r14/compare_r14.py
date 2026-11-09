"""Round 14: compare page data-run code and expected blocks with the twins and the twins' stdout. Run: python -I compare_r14.py <checkout>"""
import html
import re
import sys

ROOT = sys.argv[1]
O = f"{ROOT}/ledgers/LX1/scripts/LX1-b-r14/out"
pairs = [
    ("L03", f"{ROOT}/course/modules/LX/LX1/L03.html", f"{ROOT}/tests/labs/LX1/lab-LX1-L03-1.py", f"{O}/twin_L03.out"),
    ("L04", f"{ROOT}/course/modules/LX/LX1/L04.html", f"{ROOT}/tests/labs/LX1/lab-LX1-L04-1.py", f"{O}/twin_L04.out"),
]
ok = True
for name, page, twin, out in pairs:
    s = open(page, encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', s, re.S)
    code = html.unescape(m.group(1))
    src = open(twin, encoding="utf-8").read()
    same_code = code.rstrip("\n") == src.rstrip("\n")
    print(name, "page data-run code equals twin:", same_code, "| line span", s[:m.start()].count("\n") + 1, "-", s[:m.end()].count("\n") + 1)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    expected = html.unescape(e.group(1)).rstrip("\n")
    actual = open(out, encoding="utf-8").read().rstrip("\n")
    same_exp = expected == actual
    print(name, "expected block equals twin stdout:", same_exp, "| lines", len(expected.splitlines()), len(actual.splitlines()), "| expected span", s[:e.start()].count("\n") + 1, "-", s[:e.end()].count("\n") + 1)
    if not (same_code and same_exp):
        ok = False
        for i, (a, b) in enumerate(zip(expected.splitlines(), actual.splitlines())):
            if a != b:
                print("  first diff line", i + 1, repr(a), repr(b))
                break
print("ALL EQUAL:", ok)
sys.exit(0 if ok else 1)
