import html, re, sys, subprocess
base = "course/modules/M/M4/"
for n in ["01","02","03","04"]:
    page = open(base + f"L{n}.html", encoding="utf-8").read()
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin = open(f"tests/labs/M4/lab-M4-L{n}-1.py", encoding="utf-8").read()
    code = html.unescape(blocks[0])
    print(n, "blocks", len(blocks), "expected", len(exp), "code==twin", code.strip() == twin.strip(), "len", len(code), len(twin))
    if code.strip() != twin.strip():
        import difflib
        for l in list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:30]:
            print("  ", l)
    out = subprocess.run([".venv/bin/python", "-I", "-W", "error", f"tests/labs/M4/lab-M4-L{n}-1.py"], capture_output=True, text=True).stdout
    e = html.unescape(exp[0]).strip()
    print("  expected==output", e == out.strip())
    if e != out.strip():
        import difflib
        for l in list(difflib.unified_diff(out.strip().splitlines(), e.splitlines(), lineterm=""))[:20]:
            print("  ", l)
