import html, re, sys
out = []
for n in range(19, 25):
    page = open(f"course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    twin = open(f"tests/labs/M2/lab-M2-L{n}-1.py", encoding="utf-8").read()
    codes = re.findall(r'<code class="language-python" data-run>(.*?)</code>', page, flags=re.S)
    expected = re.findall(r'<pre class="expected">(.*?)</pre>', page, flags=re.S)
    code_ok = len(codes) == 1 and html.unescape(codes[0]).rstrip("\n") == twin.rstrip("\n")
    exp_ok = len(expected) >= 1 and html.unescape(expected[-1]).strip() != ""
    out.append((n, len(codes), code_ok, len(expected), exp_ok))
    print(f"L{n}: code blocks {len(codes)} code==twin(rstrip) {code_ok}; expected blocks {len(expected)} nonempty {exp_ok}")
    if not code_ok and codes:
        a = html.unescape(codes[0]).rstrip("\n").splitlines(); b = twin.rstrip("\n").splitlines()
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print("  first diff line", i + 1, repr(x)[:120], "|", repr(y)[:120]); break
        else:
            print("  length differs", len(a), len(b))
