import html, re, subprocess, sys
root = sys.argv[1]
for n in ("01","02","03","04"):
    page = open(f"{root}/course/modules/CS/CS2/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1)); exp = html.unescape(m.group(2))
    open(f"/tmp/CS2-v/a/extracted-L{n}.py","w").write(code)
    r = subprocess.run([f"{root}/.venv/bin/python","-I","-W","error",f"/tmp/CS2-v/a/extracted-L{n}.py"],capture_output=True,text=True)
    out = r.stdout
    print(f"L{n}: rc={r.returncode} stderr={r.stderr.strip()[:200]!r} exact_match={out.strip()==exp.strip()}")
    if out.strip()!=exp.strip():
        import difflib
        for l in difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm=""):
            print("   ", l)
    # twin
    t = subprocess.run([f"{root}/.venv/bin/python","-I","-W","error",f"{root}/tests/labs/CS2/lab-CS2-L{n}-1.py"],capture_output=True,text=True)
    print(f"  twin rc={t.returncode} stdout==printed: {t.stdout==out} twin_stderr={t.stderr.strip()[:200]!r}")
    print(f"  code==twin: {code.strip()==open(f'{root}/tests/labs/CS2/lab-CS2-L{n}-1.py').read().strip()}")
