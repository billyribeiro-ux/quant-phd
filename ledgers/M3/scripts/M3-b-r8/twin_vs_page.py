import html, re, subprocess, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-M3-b"
PY = ROOT + "/.venv/bin/python"
for lesson in ("L04", "L05", "L06"):
    page = open(f"{ROOT}/course/modules/M/M3/{lesson}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    twin_path = f"{ROOT}/tests/labs/M3/lab-M3-{lesson}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    r = subprocess.run([PY, "-I", "-W", "error", twin_path], capture_output=True, text=True, cwd="/tmp")
    out = r.stdout
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    same_out = out.rstrip("\n") == expected.rstrip("\n")
    print(f"{lesson} code==twin: {same_code} exit: {r.returncode} stderr: {r.stderr!r} out==expected: {same_out} lines {len(out.splitlines())} {len(expected.splitlines())}")
    if not same_out:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
