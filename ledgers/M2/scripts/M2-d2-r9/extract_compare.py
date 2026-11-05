import html, re, subprocess, sys
root = "/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2"
for n in ["L22", "L23", "L24"]:
    page = open(f"{root}/course/modules/M/M2/{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/M2/lab-M2-{n}-1.py", encoding="utf-8").read()
    print(n, "code==twin (strict):", code == twin, "(modulo trailing newline):", code.rstrip("\n") == twin.rstrip("\n"), "code_line_span:", page[:m.start()].count("\n")+1, "-", page[:m.end()].count("\n")+1)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(e.group(1))
    out = subprocess.run([sys.executable if False else "/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/M2/lab-M2-{n}-1.py"], capture_output=True, text=True, cwd="/tmp").stdout
    print(n, "expected==live stdout:", exp.rstrip("\n") == out.rstrip("\n"), "| expected_span:", page[:e.start()].count("\n")+1, "-", page[:e.end()].count("\n")+1, "| attrs:", re.search(r'<pre class="expected"([^>]*)>', page).group(1))
    if exp.rstrip("\n") != out.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm="")))
