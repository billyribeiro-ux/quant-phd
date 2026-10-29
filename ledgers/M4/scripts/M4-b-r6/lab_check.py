import html, re, subprocess, sys
root = sys.argv[1]
for L, lab in [("L05", "lab-M4-L05-1"), ("L06", "lab-M4-L06-1"), ("L07", "lab-M4-L07-1")]:
    page = open(f"{root}/course/modules/M/M4/{L}.html", encoding="utf-8").read()
    m = re.search(rf'<section class="lab" id="{lab}".*?</section>', page, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = open(f"{root}/tests/labs/M4/{lab}.py", encoding="utf-8").read()
    print(L, "page code == twin:", code.strip() == twin.strip(), "len", len(code), len(twin))
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:60]))
    r = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/M4/{lab}.py"], capture_output=True, text=True)
    print(L, "exit", r.returncode, "stderr:", r.stderr[:300])
    print(L, "expected == output:", exp.strip() == r.stdout.strip())
    if exp.strip() != r.stdout.strip():
        print("EXPECTED:\n" + exp + "\nOUTPUT:\n" + r.stdout)
    else:
        print(r.stdout)
