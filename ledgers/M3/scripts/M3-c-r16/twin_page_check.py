import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(sys.argv[2])
pairs = {"L07": "lab-M3-L07-1.py", "L08": "lab-M3-L08-1.py", "L09": "lab-M3-L09-1.py"}
for lesson, twin in pairs.items():
    page = (root / f"course/modules/M/M3/{lesson}.html").read_text(encoding="utf-8")
    tw = (root / f"tests/labs/M3/{twin}").read_text(encoding="utf-8").rstrip("\n")
    code = re.findall(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    got_out = (out_dir / f"twin_lab-M3-{lesson}-1.out").read_text(encoding="utf-8").rstrip("\n")
    print(lesson, "data-run blocks:", len(code), "expected blocks:", len(exp))
    print(lesson, "code equals twin:", html.unescape(code[0]) == tw if code else None)
    print(lesson, "expected equals twin output:", html.unescape(exp[0]).rstrip("\n") == got_out if exp else None)
    if code and html.unescape(code[0]) != tw:
        import difflib
        print("".join(difflib.unified_diff(tw.splitlines(True), html.unescape(code[0]).splitlines(True))))
    if exp and html.unescape(exp[0]).rstrip("\n") != got_out:
        import difflib
        print("".join(difflib.unified_diff(got_out.splitlines(True), html.unescape(exp[0]).splitlines(True))))
