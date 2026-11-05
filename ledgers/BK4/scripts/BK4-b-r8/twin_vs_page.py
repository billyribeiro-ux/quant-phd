import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for page, twin in (("L04", "lab-BK4-L04-1.py"), ("L05", "lab-BK4-L05-1.py")):
    h = (root / f"course/modules/BK/BK4/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', h, re.S).group(1)
    code = html.unescape(code)
    twin_src = (root / "tests/labs/BK4" / twin).read_text(encoding="utf-8")
    print(page, "page code == twin:", code == twin_src, "| len page", len(code), "len twin", len(twin_src), "| trailing-newline-stripped equal:", code.rstrip("\n") == twin_src.rstrip("\n"))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', h, re.S).group(1))
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/BK4" / twin)], cwd="/tmp", capture_output=True, text=True)
    print(page, "exit", p.returncode, "stderr empty", p.stderr == "", "stdout == expected:", p.stdout == exp, "| stripped equal:", p.stdout.strip() == exp.strip())
    if p.stdout.strip() != exp.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), p.stdout.strip().splitlines(), lineterm="")))
