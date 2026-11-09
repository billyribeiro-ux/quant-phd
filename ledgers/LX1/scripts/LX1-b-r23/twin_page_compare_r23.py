"""Compare each LX1 lesson lab (L01, L03, L04) with its twin: page code block vs twin file, and the expected block vs
the twin stdout captured in out/twin_<L>.out (excluding the trailing 'exit' line). Run as: python -I script <root> <outdir>."""
import html
import re
import sys

ROOT, OUT = sys.argv[1], sys.argv[2]
ok = True
for L in ("L01", "L03", "L04"):
    s = open(f"{ROOT}/course/modules/LX/LX1/{L}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', s, flags=re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{ROOT}/tests/labs/LX1/lab-LX1-{L}-1.py", encoding="utf-8").read()
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, flags=re.S).group(1)
    exp = html.unescape(re.sub(r"<[^>]+>", "", exp))
    out = open(f"{OUT}/twin_{L}.out", encoding="utf-8").read()
    out = out.rsplit("exit ", 1)[0]
    same_exp = exp.strip() == out.strip()
    print(L, "code==twin", same_code, "len page", len(code), "len twin", len(twin), "| expected==stdout", same_exp, len(exp), len(out))
    if not same_exp:
        import difflib
        for d in list(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm=""))[:20]:
            print("   ", d)
    if not (same_code and same_exp):
        ok = False
print("ALL", ok)
