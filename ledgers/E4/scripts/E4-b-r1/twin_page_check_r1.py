import html, re, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-E4-b"
O = ROOT + "/ledgers/E4/scripts/E4-b-r1/outputs/"
for lab in ["L04", "L05", "L06"]:
    page = open(f"{ROOT}/course/modules/E/E4/{lab}.html", encoding="utf-8").read()
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin = open(f"{ROOT}/tests/labs/E4/lab-E4-{lab}-1.py", encoding="utf-8").read()
    out = open(O + f"twin_{lab}.out", encoding="utf-8").read()
    print(lab, "code blocks:", len(codes), "expected blocks:", len(exp))
    c = html.unescape(codes[0])
    print(lab, "page code == twin (ignoring final newline):", c.rstrip("\n") == twin.rstrip("\n"), "| exact:", c == twin, "| lines:", c.count("\n"))
    e = html.unescape(exp[0])
    print(lab, "expected == output (rstrip):", e.rstrip("\n") == out.rstrip("\n"), "| len exp", len(e), "len out", len(out))
    if e.rstrip("\n") != out.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(out.rstrip("\n").splitlines(), e.rstrip("\n").splitlines(), lineterm="")))
