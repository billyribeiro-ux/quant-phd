import html, re, sys, subprocess
pages = {"course/modules/CF/CF8/L01.html": "tests/labs/CF8/lab-CF8-L01-1.py", "course/modules/CF/CF8/L02.html": "tests/labs/CF8/lab-CF8-L02-1.py"}
for page, twin in pages.items():
    src = open(page, encoding="utf-8").read()
    import os; out = subprocess.run([sys.executable, "-I", "-W", "error", os.path.abspath(twin)], capture_output=True, text=True, cwd="/tmp").stdout
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    print(page, "expected blocks:", len(exp))
    for e in exp:
        e2 = html.unescape(e)
        print("  expected == output:", e2.strip() == out.strip(), "lines", len(e2.splitlines()))
        if e2.strip() != out.strip():
            import difflib
            print("".join(list(difflib.unified_diff(out.splitlines(True), e2.splitlines(True), n=0))[:40]))
