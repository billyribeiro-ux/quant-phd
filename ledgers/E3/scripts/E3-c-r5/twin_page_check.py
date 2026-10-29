import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC5-E3-c")
for lab, page in (("L07", "course/modules/E/E3/L07.html"), ("L08", "course/modules/E/E3/L08.html")):
    twin = (root / f"tests/labs/E3/lab-E3-{lab}-1.py").read_text()
    src = (root / page).read_text()
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S)
    code = html.unescape(code.group(1)) if code else None
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", exp.group(1))) if exp else None
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E3/lab-E3-{lab}-1.py")],
                         capture_output=True, text=True)
    print(lab, "twin exit", out.returncode, "stderr", repr(out.stderr))
    print(lab, "page code == twin (rstrip):", code is not None and code.rstrip("\n") == twin.rstrip("\n"))
    print(lab, "expected == stdout (rstrip):", exp is not None and exp.rstrip("\n") == out.stdout.rstrip("\n"))
    if code and code.rstrip("\n") != twin.rstrip("\n"):
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:40]))
    if exp is not None and exp.rstrip("\n") != out.stdout.rstrip("\n"):
        import difflib
        print("".join(list(difflib.unified_diff(out.stdout.splitlines(True), exp.splitlines(True)))[:40]))
