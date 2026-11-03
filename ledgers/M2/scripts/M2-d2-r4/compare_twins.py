import html, re, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyD4-M2-d2"
S = ROOT + "/ledgers/M2/scripts/M2-d2-r4"
for P in ("L22", "L23", "L24"):
    page = open(f"{ROOT}/course/modules/M/M2/{P}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{ROOT}/tests/labs/M2/lab-M2-{P}-1.py", encoding="utf-8").read()
    print(P, "code==twin strict:", code == twin, "code==twin modulo final newline:", code.rstrip("\n") == twin.rstrip("\n"),
          "len", len(code), len(twin), "lines", code.count("\n"), twin.count("\n"))
    if code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:20]:
            print("   ", line)
    e = re.search(r'<pre class="expected" data-tolerance="[^"]*">(.*?)</pre>', page, re.S)
    exp = html.unescape(e.group(1))
    out = open(f"{S}/twin_{P}.stdout", encoding="utf-8").read()
    print(P, "expected==stdout strict:", exp == out, "modulo final newline:", exp.rstrip("\n") == out.rstrip("\n"))
    if exp.rstrip("\n") != out.rstrip("\n"):
        import difflib
        for line in list(difflib.unified_diff(out.splitlines(), exp.splitlines(), "stdout", "expected", lineterm=""))[:20]:
            print("   ", line)
