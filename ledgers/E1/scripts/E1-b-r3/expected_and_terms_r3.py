"""Round 3: expected block == twin stdout (explicit), page code == twin, and term/banned-word scan of the three pages and twins."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyS3-E1-b/"
PY = "/Users/billyribeiro/dev/quant-phd/.venv/bin/python"
for L in ("L04", "L05", "L06"):
    page = open(ROOT + f"course/modules/E/E1/{L}.html", encoding="utf-8").read()
    twin = open(ROOT + f"tests/labs/E1/lab-E1-{L}-1.py", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    print(L, "page code == twin:", code.strip() == twin.strip())
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp).strip("\n")
    out = subprocess.run([PY, "-I", "-W", "error", "-c", twin], capture_output=True, text=True, cwd="/tmp").stdout.strip("\n")
    print(L, "expected block == twin stdout:", exp.strip() == out.strip(), "lines", len(out.splitlines()))
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm="")))
    print(L, "data-files count:", page.count("data-files"), "svg count:", page.count("<svg"))

visible = []
for L in ("L04", "L05", "L06"):
    raw = open(ROOT + f"course/modules/E/E1/{L}.html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    visible.append((L, re.sub(r"\s+", " ", html.unescape(raw))))
banned = ["TODO", "TBD", "lorem", "clearly", "obviously", "studies show", "experts", "well known", "checked directly", "builder", "verifier", "unit report", "REQUESTS", "Round ", "round ", "...", "…"]
for L, t in visible:
    for b in banned:
        for m in re.finditer(re.escape(b), t):
            print("BANNED?", L, repr(b), t[max(0, m.start() - 60): m.end() + 40])
for L, t in visible:
    for w in ["price elasticity", "elasticity of the equilibrium", "elastic", "only", "every", "all ", "exactly", "always", "any "]:
        hits = [m.start() for m in re.finditer(w, t)]
        print(L, repr(w), len(hits))
