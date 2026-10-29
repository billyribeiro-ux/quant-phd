import re, sys, subprocess, pathlib
root = pathlib.Path(sys.argv[1])
for f in ["L05", "L06", "L07"]:
    page = (root / f"course/modules/M/M4/{f}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M4/lab-M4-{f}-1.py").read_text(encoding="utf-8")
    blocks = re.findall(r"<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>", page, re.S)
    import html
    codes = [html.unescape(b) for b in blocks]
    match = [c for c in codes if c.strip() == twin.strip()]
    print(f, "page code blocks:", len(codes), "twin match:", len(match))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M4/lab-M4-{f}-1.py")], capture_output=True, text=True)
    print(f, "exit", out.returncode, "stderr", repr(out.stderr[:200]))
    exp = re.findall(r"<pre[^>]*expected[^>]*>\s*<code[^>]*>(.*?)</code>", page, re.S)
    print(f, "expected blocks", len(exp), "equal:", [html.unescape(e).strip() == out.stdout.strip() for e in exp])
