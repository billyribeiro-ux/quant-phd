import html, re, subprocess, sys, pathlib
root = pathlib.Path("/tmp/verifyB4-M2-d")
py = str(root / ".venv/bin/python")
for L in ["L19","L20","L21","L22","L23","L24"]:
    page = (root / f"course/modules/M/M2/{L}.html").read_text()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    out = subprocess.run([py, "-I", "-W", "error", str(root / f"tests/labs/M2/lab-M2-{L}-1.py")], capture_output=True, text=True, cwd="/tmp").stdout
    if not m:
        print(L, "no expected block"); continue
    exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    same = exp.strip() == out.strip()
    print(L, "expected==run:", same, "lines", len(out.splitlines()))
    if not same:
        import difflib
        for d in difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm=""):
            print("   ", d[:200])
