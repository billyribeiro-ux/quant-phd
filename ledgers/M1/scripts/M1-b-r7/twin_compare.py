import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for page, twin in [("L04", "lab-M1-L04-1.py"), ("L05", "lab-M1-L05-1.py")]:
    text = (root / "course/modules/M/M1" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S)
    code = html.unescape(m.group(1))
    tw = (root / "tests/labs/M1" / twin).read_text(encoding="utf-8")
    print(page, "code==twin (modulo final newline):", code.rstrip("\n") == tw.rstrip("\n"), len(code), len(tw))
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    print(page, "expected blocks:", len(exp))
    for e in exp:
        lines = html.unescape(e).strip("\n").splitlines()
        print("  expected lines:", len(lines), "first:", lines[0][:60])
