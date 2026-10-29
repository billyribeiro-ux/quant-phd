import re, sys, subprocess, pathlib, html
root = pathlib.Path(sys.argv[1])
for f in ["L05", "L06", "L07"]:
    page = (root / f"course/modules/M/M4/{f}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M4/lab-M4-{f}-1.py").read_text(encoding="utf-8")
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M4/lab-M4-{f}-1.py")], capture_output=True, text=True)
    e = html.unescape(re.sub(r"<[^>]+>", "", exp[0])) if exp else None
    print(f, "expected blocks", len(exp), "expected==stdout:", e is not None and e.strip() == out.stdout.strip(), "lines", out.stdout.count("\n"))
    m = re.search(r'<section class="lab".*?<pre[^>]*>(.*?)</pre>', page, re.S)
    code = re.findall(r"<pre[^>]*>\s*<code[^>]*>(.*?)</code>", page, re.S)
    print(f, "code blocks", len(code), "twin==code:", [html.unescape(c).strip()==twin.strip() for c in code])
