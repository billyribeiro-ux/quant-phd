import html, re, subprocess, sys
root = sys.argv[1]
for L, twin in (("L07", "lab-E5-L07-1"), ("L08", "lab-E5-L08-1")):
    page = open(f"{root}/course/modules/E/E5/{L}.html", encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    twin_src = open(f"{root}/tests/labs/E5/{twin}.py", encoding="utf-8").read()
    print(L, "code == twin:", code == twin_src, "| twin lines:", twin_src.count("\n"))
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E5/{twin}.py"], capture_output=True, text=True)
    print(L, "twin exit", run.returncode, "stderr:", run.stderr.strip()[:200])
    print(L, "expected == output:", exp.strip("\n") == run.stdout.strip("\n"))
    if exp.strip("\n") != run.stdout.strip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), run.stdout.strip().splitlines(), lineterm="")))
